import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Workspace from './pages/Workspace'

export const isMock = import.meta.env.VITE_USE_MOCK === 'true'

export default function App() {
  return (
    <BrowserRouter>
      <nav className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-3">
        <Link to="/" className="font-semibold text-blue-600 hover:text-blue-800">
          🔬 ResearchFlow
        </Link>
        <span className="text-gray-300">|</span>
        <span className="text-sm text-gray-500">Workflow & Insight Platform</span>
        {isMock && (
          <span className="ml-auto text-xs bg-amber-100 text-amber-700 border border-amber-300 px-2 py-0.5 rounded-full font-medium">
            ⚡ Mock Data
          </span>
        )}
      </nav>
      <div className="max-w-5xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/"            element={<Dashboard />} />
          <Route path="/project/:id" element={<Workspace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}