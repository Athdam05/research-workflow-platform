const delay = (ms = 300) => new Promise(res => setTimeout(res, ms))
const ok = (data) => ({ data })

const store = {
  projects: [
    { id: 1, name: 'Transformer Attention Mechanisms', description: 'Investigating multi-head attention patterns in large language models.', created_at: '2024-11-01T09:00:00Z' },
    { id: 2, name: 'Protein Folding via Diffusion', description: 'Applying score-based generative models to protein structure prediction.', created_at: '2024-12-15T14:30:00Z' },
    { id: 3, name: 'Federated Learning on Edge Devices', description: 'Privacy-preserving ML training across heterogeneous IoT hardware.', created_at: '2025-01-20T11:00:00Z' },
  ],
  papers: [
    { id: 1, project_id: 1, title: 'Attention Is All You Need', authors: 'Vaswani, A.; Shazeer, N.; Parmar, N.', year: 2017, venue: 'NeurIPS', url: 'https://arxiv.org/abs/1706.03762', abstract: 'We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.', ai_summary: 'Foundational paper introducing the Transformer. Key insight: self-attention replaces RNNs, enabling parallelisation and better long-range dependency modelling.', tags: ['attention', 'transformers', 'NLP'] },
    { id: 2, project_id: 1, title: 'BERT: Pre-training of Deep Bidirectional Transformers', authors: 'Devlin, J.; Chang, M.; Lee, K.', year: 2019, venue: 'NAACL', url: 'https://arxiv.org/abs/1810.04805', abstract: 'We introduce BERT, a method of pre-training language representations using a masked language model objective.', ai_summary: 'BERT demonstrates that bidirectional pre-training significantly outperforms left-to-right models on 11 NLP tasks.', tags: ['BERT', 'pre-training', 'NLP'] },
    { id: 3, project_id: 1, title: 'Flash Attention: Fast and Memory-Efficient Exact Attention', authors: 'Dao, T.; Fu, D.; Ermon, S.', year: 2022, venue: 'NeurIPS', url: 'https://arxiv.org/abs/2205.14135', abstract: 'We propose FlashAttention, an IO-aware exact attention algorithm that uses tiling to reduce the number of memory reads/writes.', ai_summary: 'Achieves 2-4× speedup and 5-20× memory reduction vs standard attention by fusing operations and minimising HBM access.', tags: ['efficiency', 'attention', 'hardware'] },
    { id: 4, project_id: 2, title: 'AlphaFold 2: Highly Accurate Protein Structure Prediction', authors: 'Jumper, J.; Evans, R.; Pritzel, A.', year: 2021, venue: 'Nature', url: 'https://www.nature.com/articles/s41586-021-03819-2', abstract: 'We present AlphaFold 2, a novel machine learning approach that achieves atomic-level accuracy in predicting protein 3D structure.', ai_summary: 'Landmark result solving the 50-year protein folding problem. Uses evoformer blocks and structure module with invariant point attention.', tags: ['protein folding', 'structure prediction', 'biology'] },
  ],
  experiments: [
    { id: 1, project_id: 1, name: 'Ablation: Number of Attention Heads', status: 'completed', hypothesis: 'Increasing the number of attention heads beyond 8 yields diminishing returns on GLUE benchmark tasks.', methodology: 'Train BERT-base variants with 1, 2, 4, 8, 16, and 32 attention heads. Keep parameter count constant by adjusting head dimension. Evaluate on GLUE dev set after 3 epochs.', results: '8 heads: 84.2 GLUE avg. 16 heads: 84.5. 32 heads: 84.3. Differences within noise threshold. Training time scales linearly with head count.', notes: 'Replicate with larger model (BERT-large) to confirm trend.' },
    { id: 2, project_id: 1, name: 'FlashAttention vs Standard Attention — Throughput', status: 'completed', hypothesis: 'FlashAttention will achieve ≥2× throughput on sequence lengths ≥2048 on A100 GPU.', methodology: 'Benchmark forward + backward pass for sequences of length 512, 1024, 2048, 4096, 8192. Use PyTorch 2.0, fp16, batch size 8.', results: 'At seq_len=2048: 2.3× speedup. At seq_len=4096: 3.8× speedup. Memory reduced by 5.2× at seq_len=4096. Hypothesis confirmed.', notes: 'Flash Attention 2 shows further 15% improvement on the same hardware.' },
    { id: 3, project_id: 1, name: 'Attention Pattern Visualisation — Layer Analysis', status: 'running', hypothesis: 'Early layers capture syntactic patterns; later layers capture semantic relationships.', methodology: 'Extract attention weights from all 12 layers of BERT-base. Visualise via BertViz on 500 sentences from CoNLL-2003.', results: '', notes: 'In progress — partial results suggest layers 0-3 are syntax-heavy as expected.' },
    { id: 4, project_id: 2, name: 'Diffusion Steps vs Structure Quality', status: 'planned', hypothesis: 'Reducing diffusion timesteps from 200 to 50 degrades TM-score by less than 5% while halving inference time.', methodology: 'Sample 100 proteins from CATH S20 test set. Run inference at T=200, 100, 50, 25. Evaluate TM-score and GDT-TS vs AlphaFold 2 predictions.', results: '', notes: 'Awaiting access to H100 cluster.' },
  ],
  insights: [
    { id: 1, project_id: 1, title: 'Head count has minimal impact above 8 heads', content: 'Across 6 ablation runs, increasing attention heads beyond 8 yields <0.3 GLUE improvement — within noise. This suggests the representational bottleneck is elsewhere (likely FFN width).', type: 'finding', priority: 'high', paper_id: null, experiment_id: 1 },
    { id: 2, project_id: 1, title: 'FlashAttention makes long-context training practical', content: 'At seq_len=4096, memory drops from 38GB to 7GB, making it feasible to train on consumer A6000 cards. This unblocks our planned 8k-context experiments.', type: 'conclusion', priority: 'high', paper_id: 3, experiment_id: 2 },
    { id: 3, project_id: 1, title: 'Layers 0–3 appear syntactically specialised', content: 'Preliminary BertViz analysis shows consistent subject-verb and modifier-head attention in early layers. Aligns with Clark et al. 2019 findings.', type: 'observation', priority: 'medium', paper_id: 2, experiment_id: 3 },
    { id: 4, project_id: 2, title: 'Evoformer may be adaptable for small-molecule docking', content: 'The pairwise representation in Evoformer captures residue-residue geometry. Hypothesis: with ligand atom tokens, it could model protein-ligand interactions directly.', type: 'hypothesis', priority: 'medium', paper_id: 4, experiment_id: null },
  ],
  relationships: [
    { id: 1, project_id: 1, source_type: 'paper',      source_id: 3, target_type: 'experiment', target_id: 2, relationship_type: 'benchmarked_by' },
    { id: 2, project_id: 1, source_type: 'experiment', source_id: 2, target_type: 'insight',    target_id: 2, relationship_type: 'produced'       },
    { id: 3, project_id: 1, source_type: 'experiment', source_id: 1, target_type: 'insight',    target_id: 1, relationship_type: 'produced'       },
    { id: 4, project_id: 1, source_type: 'paper',      source_id: 2, target_type: 'insight',    target_id: 3, relationship_type: 'supports'       },
    { id: 5, project_id: 1, source_type: 'paper',      source_id: 1, target_type: 'paper',      target_id: 2, relationship_type: 'inspired'       },
  ],
  _nextId: { projects: 4, papers: 5, experiments: 5, insights: 5, relationships: 6 },
}

const nextId = (type) => store._nextId[type]++

function buildGraph(projectId) {
  const pid = parseInt(projectId)
  const rels = store.relationships.filter(r => r.project_id === pid)
  const nodeSet = {}
  const addNode = (type, id) => {
    const key = `${type}-${id}`
    if (nodeSet[key]) return
    let label = `${type} #${id}`
    if (type === 'paper')      { const p = store.papers.find(x => x.id === id);      label = p?.title ?? label }
    if (type === 'experiment') { const e = store.experiments.find(x => x.id === id); label = e?.name  ?? label }
    if (type === 'insight')    { const i = store.insights.find(x => x.id === id);    label = i?.title ?? label }
    nodeSet[key] = { id: key, type, label }
  }
  rels.forEach(r => { addNode(r.source_type, r.source_id); addNode(r.target_type, r.target_id) })
  const edges = rels.map(r => ({
    source: `${r.source_type}-${r.source_id}`,
    target: `${r.target_type}-${r.target_id}`,
    source_label: nodeSet[`${r.source_type}-${r.source_id}`]?.label,
    target_label: nodeSet[`${r.target_type}-${r.target_id}`]?.label,
    type: r.relationship_type,
    relationship_type: r.relationship_type,
  }))
  return { nodes: Object.values(nodeSet), edges }
}

export const getProjects        = async ()     => { await delay();      return ok([...store.projects]) }
export const createProject      = async (data) => { await delay(400);   const p = { id: nextId('projects'),      created_at: new Date().toISOString(), ...data };                              store.projects.unshift(p);      return ok(p) }
export const deleteProject      = async (id)   => { await delay(300);   store.projects    = store.projects.filter(p => p.id !== parseInt(id));                                                                              return ok({ deleted: true }) }
export const getPapers          = async (pid)  => { await delay();      return ok(store.papers.filter(p => p.project_id === parseInt(pid))) }
export const createPaper        = async (data) => { await delay(400);   const p = { id: nextId('papers'),        ...data, project_id: parseInt(data.project_id) };                            store.papers.unshift(p);        return ok(p) }
export const getExperiments     = async (pid)  => { await delay();      return ok(store.experiments.filter(e => e.project_id === parseInt(pid))) }
export const createExperiment   = async (data) => { await delay(400);   const e = { id: nextId('experiments'),   ...data, project_id: parseInt(data.project_id) };                            store.experiments.unshift(e);   return ok(e) }
export const getInsights        = async (pid)  => { await delay();      return ok(store.insights.filter(i => i.project_id === parseInt(pid))) }
export const createInsight      = async (data) => { await delay(400);   const i = { id: nextId('insights'),      ...data, project_id: parseInt(data.project_id) };                            store.insights.unshift(i);      return ok(i) }
export const getRelationships   = async ()     => { await delay();      return ok([...store.relationships]) }
export const createRelationship = async (data) => { await delay(400);   const r = { id: nextId('relationships'), ...data };                                                                    store.relationships.push(r);    return ok(r) }
export const getGraph           = async (pid)  => { await delay();      return ok(buildGraph(pid)) }