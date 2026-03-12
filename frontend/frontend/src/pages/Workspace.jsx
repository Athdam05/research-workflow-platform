import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  getProjects,
  getPapers, createPaper,
  getExperiments, createExperiment,
  getInsights, createInsight,
  getGraph, createRelationship,
} from '../services/useApi'
import PaperUpload from '../components/PaperUpload'
import GraphView from '../components/GraphView'

// ─── Shared micro-components ────────────────────────────────────────────────

function Btn({ children, onClick, type = 'button', variant = 'primary', disabled }) {
  const base = 'px-3 py-1.5 rounded text-sm font-medium disabled:opacity-50 transition-colors'
  const styles = {
    primary:   'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-300',
  }
  return <button type={type} onClick={onClick} disabled={disabled} className={`${base} ${styles[variant]}`}>{children}</button>
}

function Field({ label, children }) {
  return <div><label className="block text-xs font-medium text-gray-600 mb-1">{label}</label>{children}</div>
}

const inputCls = 'w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500'
function Input(props)              { return <input    {...props} className={inputCls} /> }
function Textarea(props)           { return <textarea {...props} rows={props.rows || 3} className={`${inputCls} resize-none`} /> }
function Select({ children, ...p}) { return <select  {...p} className={`${inputCls} bg-white`}>{children}</select> }
function Card({ children, className = '' }) { return <div className={`bg-white border border-gray-200 rounded-lg p-4 ${className}`}>{children}</div> }
function EmptyMsg({ text })        { return <p className="text-center text-gray-400 py-10 text-sm">{text}</p> }

function Badge({ text, color = 'gray' }) {
  const c = { gray: 'bg-gray-100 text-gray-600', blue: 'bg-blue-100 text-blue-700', green: 'bg-green-100 text-green-700', yellow: 'bg-yellow-100 text-yellow-700', red: 'bg-red-100 text-red-700', purple: 'bg-purple-100 text-purple-700' }
  return <span className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium ${c[color] || c.gray}`}>{text}</span>
}

// ─── Papers ─────────────────────────────────────────────────────────────────

function PapersTab({ projectId }) {
  const [papers, setPapers]       = useState([])
  const [loading, setLoading]     = useState(true)
  const [showForm, setShowForm]   = useState(false)
  const [saving, setSaving]       = useState(false)
  const [form, setForm]           = useState({ title: '', authors: '', year: '', venue: '', abstract: '', url: '', ai_summary: '' })

  useEffect(() => { getPapers(projectId).then(r => setPapers(r.data || [])).finally(() => setLoading(false)) }, [projectId])

  const f = key => e => setForm(p => ({ ...p, [key]: e.target.value }))
  const submit = async e => {
    e.preventDefault(); setSaving(true)
    try {
      const r = await createPaper({ ...form, project_id: parseInt(projectId), year: form.year ? +form.year : null })
      setPapers(p => [r.data, ...p])
      setForm({ title: '', authors: '', year: '', venue: '', abstract: '', url: '', ai_summary: '' })
      setShowForm(false)
    } catch { alert('Failed to save paper.') } finally { setSaving(false) }
  }

  if (loading) return <p className="text-gray-400 text-sm">Loading...</p>
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold">Papers <span className="text-gray-400 font-normal text-sm">({papers.length})</span></h2>
        <Btn onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ Upload with AI'}</Btn>
      </div>
      {showForm && (
        <div className="mb-6 relative">
          <div className="absolute right-4 top-4 z-10">
            <Btn variant="secondary" onClick={() => {
              setShowForm(false);
              getPapers(projectId).then(r => setPapers(r.data || []));
            }}>Close & Refresh</Btn>
          </div>
          <PaperUpload projectId={projectId} />
        </div>
      )}
      {papers.length === 0 ? <EmptyMsg text="No papers yet." /> : (
        <div className="space-y-3">
          {papers.map(p => (
            <Card key={p.id}>
              <div className="flex items-center gap-2 flex-wrap mb-0.5">
                <h3 className="font-medium text-sm">{p.title}</h3>
                {p.url && <a href={p.url} target="_blank" rel="noreferrer" className="text-blue-500 text-xs hover:underline">↗ link</a>}
              </div>
              <p className="text-gray-500 text-xs">{[p.authors, p.year, p.venue].filter(Boolean).join(' · ')}</p>
              {p.abstract   && <p className="text-gray-600 text-xs mt-2 leading-relaxed">{p.abstract}</p>}
              {p.summary && <div className="mt-2 bg-amber-50 border border-amber-200 rounded p-2"><span className="text-xs font-semibold text-amber-700">AI Summary: </span><span className="text-xs text-amber-800">{p.summary}</span></div>}
              {p.keywords && <div className="mt-2 flex flex-wrap gap-1 items-center"><span className="text-xs font-semibold text-gray-500">Keywords:</span>{(Array.isArray(p.keywords) ? p.keywords : String(p.keywords).split(',')).map((k, i) => <span key={i} className="text-[10px] bg-gray-100 border border-gray-200 text-gray-700 px-1.5 py-0.5 rounded">{String(k).trim()}</span>)}</div>}
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── Experiments ─────────────────────────────────────────────────────────────

const STATUS_COLORS = { completed: 'green', running: 'blue', failed: 'red', planned: 'gray' }

function ExperimentsTab({ projectId }) {
  const [experiments, setExperiments] = useState([])
  const [loading, setLoading]         = useState(true)
  const [showForm, setShowForm]       = useState(false)
  const [saving, setSaving]           = useState(false)
  const [expanded, setExpanded]       = useState(null)
  const [form, setForm]               = useState({ name: '', status: 'planned', hypothesis: '', methodology: '', results: '', notes: '' })

  useEffect(() => { getExperiments(projectId).then(r => setExperiments(r.data || [])).finally(() => setLoading(false)) }, [projectId])

  const f = key => e => setForm(p => ({ ...p, [key]: e.target.value }))
  const submit = async e => {
    e.preventDefault(); setSaving(true)
    try {
      const payload = {
        title: form.name.trim(),
        hypothesis: form.hypothesis,
        method: form.methodology,
        result: form.results,
        status: form.status,
        notes: form.notes,
        project_id: parseInt(projectId)
      }
      const r = await createExperiment(payload)
      setExperiments(p => [r.data, ...p])
      setForm({ name: '', status: 'planned', hypothesis: '', methodology: '', results: '', notes: '' })
      setShowForm(false)
    } catch { alert('Failed to save experiment.') } finally { setSaving(false) }
  }

  if (loading) return <p className="text-gray-400 text-sm">Loading...</p>
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold">Experiments <span className="text-gray-400 font-normal text-sm">({experiments.length})</span></h2>
        <Btn onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ Add Experiment'}</Btn>
      </div>
      {showForm && (
        <Card className="mb-6">
          <form onSubmit={submit} className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <Field label="Name *"><Input placeholder="Experiment name" value={form.name} onChange={f('name')} required autoFocus /></Field>
              <Field label="Status"><Select value={form.status} onChange={f('status')}><option value="planned">Planned</option><option value="running">Running</option><option value="completed">Completed</option><option value="failed">Failed</option></Select></Field>
            </div>
            <Field label="Hypothesis"><Textarea rows={2} placeholder="What do you expect?" value={form.hypothesis} onChange={f('hypothesis')} /></Field>
            <Field label="Methodology"><Textarea placeholder="How will you run it?" value={form.methodology} onChange={f('methodology')} /></Field>
            <Field label="Results"><Textarea rows={2} placeholder="What did you find?" value={form.results} onChange={f('results')} /></Field>
            <Field label="Notes"><Textarea rows={2} placeholder="Additional notes…" value={form.notes} onChange={f('notes')} /></Field>
            <div className="flex gap-2 justify-end">
              <Btn variant="secondary" onClick={() => setShowForm(false)}>Cancel</Btn>
              <Btn type="submit" disabled={saving}>{saving ? 'Saving…' : 'Save'}</Btn>
            </div>
          </form>
        </Card>
      )}
      {experiments.length === 0 ? <EmptyMsg text="No experiments yet." /> : (
        <div className="space-y-2">
          {experiments.map(exp => (
            <Card key={exp.id} className="cursor-pointer">
              <div className="flex items-center justify-between" onClick={() => setExpanded(expanded === exp.id ? null : exp.id)}>
                <div className="flex items-center gap-2">
                  <span className="font-medium text-sm">{exp.title || exp.name}</span>
                  <Badge text={exp.status || 'planned'} color={STATUS_COLORS[exp.status] || 'gray'} />
                </div>
                <span className="text-gray-400 text-xs">{expanded === exp.id ? '▲' : '▼'}</span>
              </div>
              {expanded === exp.id && (
                <div className="mt-3 space-y-2 border-t border-gray-100 pt-3">
                  {exp.hypothesis  && <p className="text-xs"><span className="font-semibold text-purple-600">Hypothesis: </span>{exp.hypothesis}</p>}
                  {(exp.method || exp.methodology) && <p className="text-xs"><span className="font-semibold text-blue-600">Methodology: </span>{exp.method || exp.methodology}</p>}
                  {(exp.result || exp.results)     && <p className="text-xs"><span className="font-semibold text-green-600">Results: </span>{exp.result || exp.results}</p>}
                  {exp.notes       && <p className="text-xs"><span className="font-semibold text-gray-500">Notes: </span>{exp.notes}</p>}
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── Insights ────────────────────────────────────────────────────────────────

const INSIGHT_COLORS = { finding: 'green', hypothesis: 'purple', observation: 'blue', conclusion: 'yellow' }

function InsightsTab({ projectId }) {
  const [insights, setInsights]       = useState([])
  const [papers, setPapers]           = useState([])
  const [experiments, setExperiments] = useState([])
  const [loading, setLoading]         = useState(true)
  const [showForm, setShowForm]       = useState(false)
  const [saving, setSaving]           = useState(false)
  const [form, setForm]               = useState({ title: '', content: '', type: 'finding', priority: 'medium', paper_id: '', experiment_id: '' })

  useEffect(() => {
    Promise.all([getInsights(projectId), getPapers(projectId), getExperiments(projectId)])
      .then(([ins, pap, exp]) => { setInsights(ins.data || []); setPapers(pap.data || []); setExperiments(exp.data || []) })
      .finally(() => setLoading(false))
  }, [projectId])

  const f = key => e => setForm(p => ({ ...p, [key]: e.target.value }))
  const submit = async e => {
    e.preventDefault(); setSaving(true)
    try {
      const payload = {
        title: form.title,
        content: form.content,
        type: form.type,
        priority: form.priority,
        project_id: parseInt(projectId),
        related_paper_id: form.paper_id ? parseInt(form.paper_id) : null,
        related_experiment_id: form.experiment_id ? parseInt(form.experiment_id) : null
      }
      const r = await createInsight(payload)
      setInsights(p => [r.data, ...p])
      setForm({ title: '', content: '', type: 'finding', priority: 'medium', paper_id: '', experiment_id: '' })
      setShowForm(false)
    } catch { alert('Failed to save insight.') } finally { setSaving(false) }
  }

  if (loading) return <p className="text-gray-400 text-sm">Loading...</p>
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold">Insights <span className="text-gray-400 font-normal text-sm">({insights.length})</span></h2>
        <Btn onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ Add Insight'}</Btn>
      </div>
      {showForm && (
        <Card className="mb-6">
          <form onSubmit={submit} className="space-y-3">
            <Field label="Title *"><Input placeholder="Insight title" value={form.title} onChange={f('title')} required autoFocus /></Field>
            <div className="grid grid-cols-2 gap-3">
              <Field label="Type"><Select value={form.type} onChange={f('type')}><option value="finding">Finding</option><option value="hypothesis">Hypothesis</option><option value="observation">Observation</option><option value="conclusion">Conclusion</option></Select></Field>
              <Field label="Priority"><Select value={form.priority} onChange={f('priority')}><option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option></Select></Field>
            </div>
            <Field label="Content"><Textarea placeholder="Describe the insight…" value={form.content} onChange={f('content')} /></Field>
            <div className="grid grid-cols-2 gap-3">
              <Field label="Link to Paper"><Select value={form.paper_id} onChange={f('paper_id')}><option value="">— None —</option>{papers.map(p => <option key={p.id} value={p.id}>{p.title?.slice(0, 45)}</option>)}</Select></Field>
              <Field label="Link to Experiment"><Select value={form.experiment_id} onChange={f('experiment_id')}><option value="">— None —</option>{experiments.map(e => <option key={e.id} value={e.id}>{(e.name || e.title)?.slice(0, 45)}</option>)}</Select></Field>
            </div>
            <div className="flex gap-2 justify-end">
              <Btn variant="secondary" onClick={() => setShowForm(false)}>Cancel</Btn>
              <Btn type="submit" disabled={saving}>{saving ? 'Saving…' : 'Save Insight'}</Btn>
            </div>
          </form>
        </Card>
      )}
      {insights.length === 0 ? <EmptyMsg text="No insights yet." /> : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {insights.map(ins => {
            const paper = papers.find(p => p.id === ins.related_paper_id || p.id === ins.paper_id)
            const exp   = experiments.find(e => e.id === ins.related_experiment_id || e.id === ins.experiment_id)
            return (
              <Card key={ins.id}>
                <div className="flex items-start justify-between gap-2 mb-1">
                  <span className="font-medium text-sm">{ins.title}</span>
                  <div className="flex gap-1 shrink-0">
                    <Badge text={ins.type || 'finding'} color={INSIGHT_COLORS[ins.type] || 'gray'} />
                    {ins.priority === 'high' && <Badge text="high" color="red" />}
                  </div>
                </div>
                {ins.content && <p className="text-xs text-gray-600 leading-relaxed mb-2">{ins.content}</p>}
                <div className="flex flex-wrap gap-1">
                  {paper && <span className="text-xs text-blue-600 bg-blue-50 rounded px-1.5 py-0.5">📄 {paper.title?.slice(0, 30)}…</span>}
                  {exp   && <span className="text-xs text-purple-600 bg-purple-50 rounded px-1.5 py-0.5">🧪 {(exp.name || exp.title)?.slice(0, 30)}…</span>}
                </div>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}

// ─── Graph ───────────────────────────────────────────────────────────────────

function GraphTab({ projectId }) {
  const [graph, setGraph]             = useState({ nodes: [], edges: [] })
  const [papers, setPapers]           = useState([])
  const [experiments, setExperiments] = useState([])
  const [insights, setInsights]       = useState([])
  const [loading, setLoading]         = useState(true)
  const [showForm, setShowForm]       = useState(false)
  const [saving, setSaving]           = useState(false)
  const [form, setForm]               = useState({ source_type: 'paper', source_id: '', target_type: 'experiment', target_id: '', relationship_type: 'related_to' })

  const load = () => {
    setLoading(true)
    Promise.all([getGraph(projectId), getPapers(projectId), getExperiments(projectId), getInsights(projectId)])
      .then(([g, p, e, i]) => { setGraph(g.data || { nodes: [], edges: [] }); setPapers(p.data || []); setExperiments(e.data || []); setInsights(i.data || []) })
      .finally(() => setLoading(false))
  }
  useEffect(load, [projectId])

  const f      = key => e => setForm(p => ({ ...p, [key]: e.target.value }))
  const opts   = type => type === 'paper' ? papers.map(p => ({ id: p.id, label: p.title })) : type === 'experiment' ? experiments.map(e => ({ id: e.id, label: e.name || e.title })) : insights.map(i => ({ id: i.id, label: i.title }))
  const NODE_C = { paper: 'bg-teal-100 text-teal-800 border-teal-300', experiment: 'bg-purple-100 text-purple-800 border-purple-300', insight: 'bg-amber-100 text-amber-800 border-amber-300' }

  const submit = async e => {
    e.preventDefault(); setSaving(true)
    try {
      await createRelationship({ ...form, source_id: parseInt(form.source_id), target_id: parseInt(form.target_id), project_id: parseInt(projectId) })
      setForm({ source_type: 'paper', source_id: '', target_type: 'experiment', target_id: '', relationship_type: 'related_to' })
      setShowForm(false); load()
    } catch { alert('Failed to create relationship.') } finally { setSaving(false) }
  }

  if (loading) return <p className="text-gray-400 text-sm">Loading...</p>
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold">Relationship Graph <span className="text-gray-400 font-normal text-sm">({graph.nodes?.length || 0} nodes, {graph.edges?.length || 0} edges)</span></h2>
        <div className="flex gap-2">
          <Btn variant="secondary" onClick={load}>↻ Refresh</Btn>
          <Btn onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ Add Relationship'}</Btn>
        </div>
      </div>
      {showForm && (
        <Card className="mb-6">
          <form onSubmit={submit} className="space-y-3">
            <Field label="Relationship Type"><Input placeholder="e.g. supports, contradicts, uses" value={form.relationship_type} onChange={f('relationship_type')} required autoFocus /></Field>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <p className="text-xs font-semibold text-gray-500 uppercase">Source</p>
                <Field label="Type"><Select value={form.source_type} onChange={e => setForm(p => ({ ...p, source_type: e.target.value, source_id: '' }))}><option value="paper">Paper</option><option value="experiment">Experiment</option><option value="insight">Insight</option></Select></Field>
                <Field label="Item"><Select value={form.source_id} onChange={f('source_id')} required><option value="">— select —</option>{opts(form.source_type).map(o => <option key={o.id} value={o.id}>{o.label?.slice(0, 50)}</option>)}</Select></Field>
              </div>
              <div className="space-y-2">
                <p className="text-xs font-semibold text-gray-500 uppercase">Target</p>
                <Field label="Type"><Select value={form.target_type} onChange={e => setForm(p => ({ ...p, target_type: e.target.value, target_id: '' }))}><option value="paper">Paper</option><option value="experiment">Experiment</option><option value="insight">Insight</option></Select></Field>
                <Field label="Item"><Select value={form.target_id} onChange={f('target_id')} required><option value="">— select —</option>{opts(form.target_type).map(o => <option key={o.id} value={o.id}>{o.label?.slice(0, 50)}</option>)}</Select></Field>
              </div>
            </div>
            <div className="flex gap-2 justify-end">
              <Btn variant="secondary" onClick={() => setShowForm(false)}>Cancel</Btn>
              <Btn type="submit" disabled={saving}>{saving ? 'Linking…' : 'Create Relationship'}</Btn>
            </div>
          </form>
        </Card>
      )}
      {graph.nodes?.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-600 mb-2">Nodes</h3>
          <div className="flex flex-wrap gap-2">
            {graph.nodes.map((n, i) => <span key={i} className={`text-xs px-2.5 py-1 rounded-full border font-medium ${NODE_C[n.type] || 'bg-gray-100 text-gray-700 border-gray-300'}`}>{n.type}: {n.label || `#${n.id}`}</span>)}
          </div>
        </div>
      )}
      {graph.edges?.length > 0 ? (
        <div>
          <h3 className="text-sm font-semibold text-gray-600 mb-2">Relationships List</h3>
          <div className="border border-gray-200 rounded-lg overflow-hidden mb-8">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-4 py-2 text-xs font-semibold text-gray-500 uppercase">Source</th>
                  <th className="text-left px-4 py-2 text-xs font-semibold text-gray-500 uppercase">Relationship</th>
                  <th className="text-left px-4 py-2 text-xs font-semibold text-gray-500 uppercase">Target</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {graph.edges.map((edge, i) => {
                  const sLabel = graph.nodes?.find(n => n.id === `${edge.source_type}_${edge.source_id}`)?.label || `${edge.source_type} #${edge.source_id}`
                  const tLabel = graph.nodes?.find(n => n.id === `${edge.target_type}_${edge.target_id}`)?.label || `${edge.target_type} #${edge.target_id}`
                  return (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="px-4 py-2 text-xs text-gray-700">{sLabel}</td>
                    <td className="px-4 py-2"><span className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded font-mono">{edge.label || edge.type || edge.relationship_type || '—'}</span></td>
                    <td className="px-4 py-2 text-xs text-gray-700">{tLabel}</td>
                  </tr>
                )})}
              </tbody>
            </table>
          </div>
          <h3 className="text-sm font-semibold text-gray-600 mb-2">Interactive AI Graph</h3>
          <div className="mt-4">
            <GraphView projectId={projectId} />
          </div>
        </div>
      ) : (
        <div>
          <EmptyMsg text="No relationships yet. Add one above to connect papers, experiments, and insights." />
          <h3 className="text-sm font-semibold text-gray-600 mb-2 mt-8">Interactive AI Graph</h3>
          <GraphView projectId={projectId} />
        </div>
      )}
    </div>
  )
}

// ─── Workspace shell ─────────────────────────────────────────────────────────

const TABS = ['papers', 'experiments', 'insights', 'graph']

export default function Workspace() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [tab, setTab]       = useState('papers')
  const [project, setProject] = useState(null)

    useEffect(() => {
  getProjects().then(r => {
    const found = (r.data || []).find(p => String(p.id) === String(id))
    setProject(found || { id, title: `Project #${id}` })
  })
}, [id])

  return (
    <div>
      <div className="flex items-center gap-3 mb-6">
        <button onClick={() => navigate('/')} className="text-sm text-gray-500 hover:text-gray-800">← Back</button>
        <span className="text-gray-300">|</span>
        <h1 className="text-xl font-bold">{project?.title || project?.name || `Project #${id}`}</h1>
        {project?.description && <span className="text-sm text-gray-500">{project.description}</span>}
      </div>
      <div className="flex border-b border-gray-200 mb-6">
        {TABS.map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium capitalize border-b-2 -mb-px transition-colors ${tab === t ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-800'}`}>
            {t}
          </button>
        ))}
      </div>
      {tab === 'papers'      && <PapersTab      projectId={id} />}
      {tab === 'experiments' && <ExperimentsTab projectId={id} />}
      {tab === 'insights'    && <InsightsTab    projectId={id} />}
      {tab === 'graph'       && <GraphTab       projectId={id} />}
    </div>
  )
}