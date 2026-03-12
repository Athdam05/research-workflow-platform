import React, { useState } from 'react';
import { createPaper } from '../services/useApi';

export default function PaperUpload({ projectId }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Send paper details to the Flask backend
      // The backend will communicate with the AI service and return the enriched data
      const response = await createPaper({
        project_id: projectId,
        title,
        content
      });
      
      setResult(response.data);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Failed to process paper");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md max-w-2xl mx-auto mt-8 border border-gray-100">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Upload Research Paper</h2>
      
      <form onSubmit={handleUpload} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Paper Title</label>
          <input 
            type="text" 
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            placeholder="e.g. Attention Is All You Need"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Paper Content (Text)</label>
          <textarea 
            required
            rows="5"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            value={content} 
            onChange={(e) => setContent(e.target.value)} 
            placeholder="Paste paper text here..."
          />
        </div>
        
        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300 transition-colors"
        >
          {isLoading ? 'Processing with AI...' : 'Upload & Analyze'}
        </button>
      </form>

      {/* AI Results Display */}
      {result && (
        <div className="mt-8 p-4 bg-blue-50 rounded-md border border-blue-200 animate-fade-in-up">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">AI Analysis Results</h3>
          <div className="mb-3">
            <span className="font-medium text-blue-800">Summary:</span>
            <p className="text-sm text-blue-900 mt-1">{result.summary}</p>
          </div>
          <div>
            <span className="font-medium text-blue-800">Keywords:</span>
            <div className="flex flex-wrap gap-2 mt-2">
              {(Array.isArray(result.keywords) ? result.keywords : String(result.keywords || '').split(',')).map((kw, idx) => (
                <span key={idx} className="px-2 py-1 bg-blue-200 text-blue-800 text-xs rounded-full shadow-sm">
                  {String(kw).trim()}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
