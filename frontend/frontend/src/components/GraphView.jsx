import React, { useEffect, useState, useCallback } from 'react';
import ReactFlow, { Background, Controls, applyNodeChanges, applyEdgeChanges } from 'reactflow';
import 'reactflow/dist/style.css';
import { getGraph } from '../services/useApi';

export default function GraphView({ projectId }) {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    async function fetchGraphData() {
      try {
        // Expected backend response format: 
        // { nodes: [{ id: '1', data: { label: 'Node 1' } }], 
        //   edges: [{ id: 'e1-2', source: '1', target: '2' }] }
        const { data } = await getGraph(projectId);
        
        // Ensure nodes have positions if your backend doesn't provide layouts natively
        const initializedNodes = data.nodes.map((node, i) => ({
          ...node,
          data: { label: node.label || (node.data && node.data.label) || node.id },
          position: node.position || { x: 50 + (i * 100), y: 50 + (i * 50) }
        }));
        
        // Ensure edges map to the exact node IDs (e.g. 'paper_1')
        const initializedEdges = data.edges.map((edge) => ({
          ...edge,
          id: String(edge.id || `e${edge.source_type}_${edge.source_id}-${edge.target_type}_${edge.target_id}`),
          source: edge.source || `${edge.source_type}_${edge.source_id}`,
          target: edge.target || `${edge.target_type}_${edge.target_id}`,
          label: edge.label || edge.relationship_type || edge.type || 'related'
        }));
        
        console.log("Graph Nodes:", initializedNodes);
        console.log("Graph Edges:", initializedEdges);
        setNodes(initializedNodes);
        setEdges(initializedEdges);
      } catch (error) {
        console.error("Failed to load graph data", error);
      }
    }
    fetchGraphData();
  }, [projectId]);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [setNodes]
  );
  
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [setEdges]
  );

  return (
    <div style={{ height: '600px', width: '100%' }} className="border rounded-lg shadow-sm bg-gray-50 mt-4">
      <ReactFlow 
        nodes={nodes} 
        edges={edges} 
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
      >
        <Background gap={16} size={1} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
