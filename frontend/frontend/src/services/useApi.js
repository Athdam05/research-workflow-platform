// Gateway: all pages import from here.
// Switch between real and mock via VITE_USE_MOCK in .env.local

import * as realApi from './api.js'
import * as mockApi from './mockApi.js'

const chosen = import.meta.env.VITE_USE_MOCK === 'true' ? mockApi : realApi

export const getProjects        = (...a) => chosen.getProjects(...a)
export const createProject      = (...a) => chosen.createProject(...a)
export const deleteProject      = (...a) => chosen.deleteProject(...a)
export const getPapers          = (...a) => chosen.getPapers(...a)
export const createPaper        = (...a) => chosen.createPaper(...a)
export const getExperiments     = (...a) => chosen.getExperiments(...a)
export const createExperiment   = (...a) => chosen.createExperiment(...a)
export const getInsights        = (...a) => chosen.getInsights(...a)
export const createInsight      = (...a) => chosen.createInsight(...a)
export const getRelationships   = (...a) => chosen.getRelationships(...a)
export const createRelationship = (...a) => chosen.createRelationship(...a)
export const getGraph           = (...a) => chosen.getGraph(...a)