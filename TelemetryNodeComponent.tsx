import { useEffect, useRef, useCallback } from 'react'
import { useTelemetryStore } from '@/store'
import type { WsMessage, TelemetryNode, TelemetryEdge, LogEntry, Alert, TelemetryEvent } from '@/types'

const WS_URL = process.env.NEXT_PUBLIC_WS_URL ?? 'ws://localhost:8000/ws/telemetry'
const RECONNECT_DELAY = 3000
const MAX_RECONNECT_ATTEMPTS = 10

export function useTelemetryWebSocket(projectId?: string) {
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectAttempts = useRef(0)
  const reconnectTimer = useRef<ReturnType<typeof setTimeout>>()
  const mounted = useRef(true)

  const {
    setNodes,
    updateNode,
    addNode,
    removeNode,
    setEdges,
    updateEdge,
    addLog,
    addEvent,
    addAlert,
    setConnectionStatus,
  } = useTelemetryStore()

  const handleMessage = useCallback(
    (msg: WsMessage) => {
      switch (msg.type) {
        case 'node_update': {
          const data = msg.payload as { id: string } & Partial<TelemetryNode>
          updateNode(data.id, data)
          break
        }
        case 'node_added': {
          addNode(msg.payload as TelemetryNode)
          break
        }
        case 'node_removed': {
          removeNode((msg.payload as { id: string }).id)
          break
        }
        case 'edge_update': {
          const edge = msg.payload as { id: string } & Partial<TelemetryEdge>
          updateEdge(edge.id, edge)
          break
        }
        case 'log': {
          addLog(msg.payload as LogEntry)
          break
        }
        case 'event': {
          addEvent(msg.payload as TelemetryEvent)
          break
        }
        case 'alert': {
          addAlert(msg.payload as Alert)
          break
        }
        case 'crash': {
          addEvent({
            id: Math.random().toString(36).slice(2),
            type: 'crash',
            nodeId: (msg.payload as { nodeId: string }).nodeId,
            timestamp: msg.timestamp,
            payload: msg.payload as Record<string, unknown>,
            severity: 'critical',
          })
          break
        }
        case 'ping': {
          wsRef.current?.send(JSON.stringify({ type: 'pong', timestamp: new Date().toISOString() }))
          break
        }
      }
    },
    [updateNode, addNode, removeNode, updateEdge, addLog, addEvent, addAlert]
  )

  const connect = useCallback(() => {
    if (!mounted.current) return

    setConnectionStatus('connecting')

    const url = projectId ? `${WS_URL}/${projectId}` : WS_URL
    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onopen = () => {
      if (!mounted.current) return
      reconnectAttempts.current = 0
      setConnectionStatus('connected')
    }

    ws.onmessage = (event) => {
      try {
        const msg: WsMessage = JSON.parse(event.data)
        handleMessage(msg)
      } catch (err) {
        console.error('[WS] Failed to parse message:', err)
      }
    }

    ws.onerror = () => {
      setConnectionStatus('error')
    }

    ws.onclose = () => {
      if (!mounted.current) return
      setConnectionStatus('disconnected')

      if (reconnectAttempts.current < MAX_RECONNECT_ATTEMPTS) {
        reconnectAttempts.current++
        reconnectTimer.current = setTimeout(connect, RECONNECT_DELAY)
      }
    }
  }, [projectId, handleMessage, setConnectionStatus])

  const disconnect = useCallback(() => {
    clearTimeout(reconnectTimer.current)
    wsRef.current?.close()
    wsRef.current = null
    setConnectionStatus('disconnected')
  }, [setConnectionStatus])

  const send = useCallback((message: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
    }
  }, [])

  useEffect(() => {
    mounted.current = true
    connect()
    return () => {
      mounted.current = false
      clearTimeout(reconnectTimer.current)
      wsRef.current?.close()
    }
  }, [connect])

  return { send, disconnect, reconnect: connect }
}
