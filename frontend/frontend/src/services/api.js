import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getProjects        = ()     => api.get('/projects')
export const createProject      = (data) => api.post('/projects', data)
export const deleteProject      = (id)   => api.delete(`/projects/${id}`)

export const getPapers          = (pid)  => api.get('/papers',      { params: { project_id: pid } })
export const createPaper        = (data) => api.post('/papers',     data)

export const getExperiments     = (pid)  => api.get('/experiments', { params: { project_id: pid } })
export const createExperiment   = (data) => api.post('/experiments', data)

export const getInsights        = (pid)  => api.get('/insights',    { params: { project_id: pid } })
export const createInsight      = (data) => api.post('/insights',   data)

export const getRelationships   = ()     => api.get('/relationships')
export const createRelationship = (data) => api.post('/relationships', data)
export const getGraph           = (pid)  => api.get('/relationships/graph', { params: { project_id: pid } })