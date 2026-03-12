import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getProjects, createProject, deleteProject } from '../services/useApi'

export default function Dashboard() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState('')
  const [name, setName]         = useState('')
  const [description, setDescription] = useState('')
  const [creating, setCreating] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    getProjects()
      .then(r => setProjects(r.data || []))
      .catch(() => setError('Could not connect to backend. Is Flask running on port 5000?'))
      .finally(() => setLoading(false))
  }, [])

  const handleCreate = async e => {
    e.preventDefault()
    if (!name.trim()) return
    setCreating(true)
    try {
      const r = await createProject({ name: name.trim(), description })
      setProjects(p => [r.data, ...p])
      setName('')
      setDescription('')
    } catch { alert('Failed to create project.') }
    finally { setCreating(false) }
  }

  const handleDelete = async (e, id) => {
    e.stopPropagation()
    if (!confirm('Delete this project?')) return
    try {
      await deleteProject(id)
      setProjects(p => p.filter(x => x.id !== id))
    } catch { alert('Failed to delete project.') }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Research Projects</h1>

      <form onSubmit={handleCreate} className="bg-white border border-gray-200 rounded-lg p-4 mb-8">
        <h2 className="font-semibold mb-3">New Project</h2>
        <div className="flex gap-3">
          <input
            className="border border-gray-300 rounded px-3 py-2 flex-1 text-sm focus:outline-none focus:border-blue-500"
            placeholder="Project name *"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
          <input
            className="border border-gray-300 rounded px-3 py-2 flex-1 text-sm focus:outline-none focus:border-blue-500"
            placeholder="Description (optional)"
            value={description}
            onChange={e => setDescription(e.target.value)}
          />
          <button
            type="submit"
            disabled={creating || !name.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm font-medium disabled:opacity-50"
          >
            {creating ? 'Creating...' : '+ Create'}
          </button>
        </div>
      </form>

      {loading && <p className="text-gray-500">Loading...</p>}
      {error   && <p className="text-red-600 bg-red-50 border border-red-200 rounded p-3 text-sm">{error}</p>}
      {!loading && !error && projects.length === 0 && (
        <p className="text-gray-400 text-center py-12">No projects yet. Create one above.</p>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {projects.map(p => (
          <div
            key={p.id}
            onClick={() => navigate(`/project/${p.id}`)}
            className="bg-white border border-gray-200 rounded-lg p-4 cursor-pointer hover:border-blue-400 hover:shadow-sm transition-all group"
          >
            <div className="flex items-start justify-between">
              <h3 className="font-semibold text-gray-900 text-sm mb-1">{p.name}</h3>
              <button
                onClick={e => handleDelete(e, p.id)}
                className="text-gray-300 hover:text-red-500 text-xs opacity-0 group-hover:opacity-100 transition-opacity ml-2"
              >✕</button>
            </div>
            {p.description && <p className="text-gray-500 text-xs leading-relaxed">{p.description}</p>}
            <p className="text-blue-500 text-xs mt-3">Open workspace →</p>
          </div>
        ))}
      </div>
    </div>
  )
}