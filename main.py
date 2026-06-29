'use client'

import { useCallback, useEffect, useState } from 'react'
import ReactFlow, {
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
  type NodeMouseHandler,
  MiniMap,
  BackgroundVariant,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { useTelemetryStore, useAppSettingsStore } from '@/store'
import { TelemetryNodeComponent } from './TelemetryNodeComponent'
import { AnimatedEdge } from './AnimatedEdge'
import type { TelemetryNode } from '@/types'

const nodeTypes = {
  telemetry: TelemetryNodeComponent,
}

const edgeTypes = {
  animated: AnimatedEdge,
}

function toFlowNode(node: TelemetryNode): Node {
  return {
    id: node.id,
    type: 'telemetry',
    position: node.position,
    data: node,
    draggable: true,
  }
}

export function TelemetryGraph() {
  const { nodes: telemetryNodes, edges: telemetryEdges } = useTelemetryStore()
  const { setSelectedNode, showMinimap } = useAppSettingsStore()

  const [flowNodes, setFlowNodes, onNodesChange] = useNodesState([])
  const [flowEdges, setFlowEdges, onEdgesChange] = useEdgesState([])

  // Sync telemetry state → React Flow
  useEffect(() => {
    setFlowNodes(telemetryNodes.map(toFlowNode))
  }, [telemetryNodes, setFlowNodes])

  useEffect(() => {
    setFlowEdges(
      telemetryEdges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: 'animated',
        data: edge,
        style: {
          stroke: edge.status === 'error' ? '#DC2626' : edge.status === 'inactive' ? '#D1D5DB' : '#94A3B8',
          strokeWidth: 1.5,
        },
      }))
    )
  }, [telemetryEdges, setFlowEdges])

  const onNodeClick: NodeMouseHandler = useCallback(
    (_, node) => {
      setSelectedNode(node.id)
    },
    [setSelectedNode]
  )

  const onPaneClick = useCallback(() => {
    setSelectedNode(null)
  }, [setSelectedNode])

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={flowNodes}
        edges={flowEdges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        minZoom={0.3}
        maxZoom={2}
        className="bg-[#FAFAFA]"
        proOptions={{ hideAttribution: true }}
      >
        <Background
          variant={BackgroundVariant.Dots}
          gap={24}
          size={1}
          color="#E5E7EB"
        />
        <Controls
          showInteractive={false}
          className="shadow-none"
        />
        {showMinimap && (
          <MiniMap
            zoomable
            pannable
            className="border border-[#E5E7EB] rounded-lg"
            nodeColor={(n) => {
              const status = n.data?.status
              if (status === 'online') return '#16A34A'
              if (status === 'warning') return '#D97706'
              if (status === 'error') return '#DC2626'
              return '#9CA3AF'
            }}
          />
        )}
      </ReactFlow>
    </div>
  )
}
