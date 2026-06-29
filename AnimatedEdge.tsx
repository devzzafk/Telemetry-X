import { useEffect, useRef } from 'react'
import { useTelemetryStore } from '@/store'
import type { TelemetryNode, TelemetryEdge, LogEntry } from '@/types'

const LOG_MESSAGES = {
  info: [
    'Request processed successfully in 42ms',
    'Cache hit for key user:session:abc123',
    'WebSocket connection established from 192.168.1.45',
    'Database query executed: SELECT * FROM metrics LIMIT 100',
    'Packet received from ESP32 node [device-001]',
    'Health check passed — all services nominal',
    'Config reloaded from environment variables',
    'Event published to Redis channel telemetry:updates',
  ],
  warning: [
    'Memory usage at 78% — approaching threshold',
    'Response time degraded: 450ms (threshold: 300ms)',
    'Queue depth at 8500 — consumer may be lagging',
    'Rate limit warning: 85% of quota consumed',
    'Retry attempt 2/3 for failed upstream request',
    'Temperature reading elevated: 67°C',
  ],
  error: [
    'Connection timeout to postgres://db:5432',
    'Failed to parse telemetry payload: unexpected EOF',
    'WebSocket disconnected unexpectedly — reconnecting',
    'Redis SETEX failed: connection refused',
    'Sensor read error on GPIO pin 17',
  ],
  debug: [
    'Heartbeat sent to gateway',
    'Buffer flushed: 128 events written',
    'Scheduler tick — no pending jobs',
    'DNS resolved api.service.internal → 10.0.0.45',
  ],
}

function randomBetween(min: number, max: number) {
  return Math.random() * (max - min) + min
}

function pickRandom<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)]
}

export function useMockTelemetry(enabled = true) {
  const { setNodes, setEdges, addLog, setConnectionStatus, updateNode } = useTelemetryStore()
  const intervalRef = useRef<ReturnType<typeof setInterval>>()

  useEffect(() => {
    if (!enabled) return

    const initialNodes: TelemetryNode[] = [
      {
        id: 'esp32-001',
        label: 'ESP32 Sensor',
        type: 'esp32',
        status: 'online',
        position: { x: 80, y: 200 },
        metrics: {
          cpu: 12, memory: 34, latency: 8, packetCount: 4521, packetRate: 12,
          temperature: 52, voltage: 3.3, errorCount: 0,
          networkIn: 1200, networkOut: 800, uptime: 86400,
        },
        lastSeen: new Date().toISOString(),
        createdAt: new Date(Date.now() - 86400000).toISOString(),
        tags: ['iot', 'sensor'],
      },
      {
        id: 'gateway-001',
        label: 'API Gateway',
        type: 'gateway',
        status: 'online',
        position: { x: 320, y: 100 },
        metrics: {
          cpu: 28, memory: 45, latency: 22, packetCount: 18920, packetRate: 85,
          errorCount: 2, networkIn: 45000, networkOut: 52000, uptime: 259200,
          connectedClients: 14,
        },
        lastSeen: new Date().toISOString(),
        createdAt: new Date(Date.now() - 259200000).toISOString(),
        tags: ['gateway', 'production'],
      },
      {
        id: 'backend-001',
        label: 'FastAPI Backend',
        type: 'backend',
        status: 'online',
        position: { x: 560, y: 200 },
        metrics: {
          cpu: 41, memory: 62, latency: 45, packetCount: 92100, packetRate: 230,
          errorCount: 7, networkIn: 125000, networkOut: 98000, uptime: 604800,
          fps: 60,
        },
        lastSeen: new Date().toISOString(),
        createdAt: new Date(Date.now() - 604800000).toISOString(),
        tags: ['backend', 'production'],
      },
      {
        id: 'redis-001',
        label: 'Redis Cache',
        type: 'cache',
        status: 'online',
        position: { x: 560, y: 380 },
        metrics: {
          cpu: 8, memory: 71, latency: 3, packetCount: 215400, packetRate: 520,
          errorCount: 0, networkIn: 85000, networkOut: 92000, uptime: 1209600,
        },
        lastSeen: new Date().toISOString(),
        createdAt: new Date(Date.now() - 1209600000).toISOString(),
        tags: ['cache', 'production'],
      },
      {
        id: 'postgres-001',
        label: 'PostgreSQL',
        type: 'database',
        status: 'online',
        position: { x: 800, y: 280 },
        metrics: {
          cpu: 15, memory: 58, latency: 12, packetCount: 44800, packetRate: 95,
          errorCount: 0, networkIn: 28000, networkOut: 35000, uptime: 2592000,
        },
        lastSeen: new Date().toISOString(),
        createdAt: new Date(Date.now() - 2592000000).toISOString(),
        tags: ['database', 'production'],
      },
      {
        id: 'frontend-001',
        label: 'Next.js App',
        type: 'frontend',
        status: 'online',
        position: { x: 1040, y: 180 },
        metrics: {
          cpu: 5, memory: 22, latency: 85, packetCount: 8200, packetRate: 18,
          errorCount: 1, networkIn: 12000, networkOut: 95000, uptime: 3600,
          connectedClients: 128,
        },
        lastSeen: new Date().toISOString(),
        createdAt: new Date(Date.now() - 3600000).toISOString(),
        tags: ['frontend', 'production'],
      },
      {
        id: 'pi-001',
        label: 'Raspberry Pi',
        type: 'raspberry-pi',
        status: 'warning',
        position: { x: 80, y: 380 },
        metrics: {
          cpu: 78, memory: 82, latency: 35, packetCount: 9100, packetRate: 22,
          temperature: 72, voltage: 5.0, errorCount: 3,
          networkIn: 5000, networkOut: 4500, uptime: 43200,
        },
        lastSeen: new Date().toISOString(),
        createdAt: new Date(Date.now() - 43200000).toISOString(),
        tags: ['iot', 'edge'],
      },
    ]

    const initialEdges: TelemetryEdge[] = [
      { id: 'e1', source: 'esp32-001', target: 'gateway-001', status: 'active', packetRate: 12, latency: 30, protocol: 'MQTT' },
      { id: 'e2', source: 'pi-001', target: 'gateway-001', status: 'active', packetRate: 22, latency: 45, protocol: 'HTTP' },
      { id: 'e3', source: 'gateway-001', target: 'backend-001', status: 'active', packetRate: 85, latency: 22, protocol: 'REST' },
      { id: 'e4', source: 'backend-001', target: 'redis-001', status: 'active', packetRate: 520, latency: 3, protocol: 'Redis' },
      { id: 'e5', source: 'backend-001', target: 'postgres-001', status: 'active', packetRate: 95, latency: 12, protocol: 'SQL' },
      { id: 'e6', source: 'backend-001', target: 'frontend-001', status: 'active', packetRate: 18, latency: 85, protocol: 'WS' },
    ]

    setNodes(initialNodes)
    setEdges(initialEdges)
    setConnectionStatus('connected')

    let tick = 0

    intervalRef.current = setInterval(() => {
      tick++

      // Fluctuate node metrics
      initialNodes.forEach((node) => {
        const cpu = Math.min(100, Math.max(0, node.metrics.cpu + randomBetween(-5, 5)))
        const memory = Math.min(100, Math.max(0, node.metrics.memory + randomBetween(-2, 2)))
        const latency = Math.max(1, node.metrics.latency + randomBetween(-10, 10))
        const packetRate = Math.max(0, node.metrics.packetRate + randomBetween(-5, 5))

        const status = cpu > 90 ? 'error' : cpu > 75 ? 'warning' : node.status

        updateNode(node.id, {
          status,
          metrics: {
            ...node.metrics,
            cpu,
            memory,
            latency,
            packetRate,
            packetCount: node.metrics.packetCount + Math.floor(packetRate),
            uptime: node.metrics.uptime + 1,
          },
          lastSeen: new Date().toISOString(),
        })
      })

      // Add log entries
      if (tick % 2 === 0) {
        const levelRoll = Math.random()
        const level = levelRoll > 0.92 ? 'error' : levelRoll > 0.8 ? 'warning' : levelRoll > 0.4 ? 'info' : 'debug'
        const node = pickRandom(initialNodes)
        const messages = LOG_MESSAGES[level as keyof typeof LOG_MESSAGES]

        const log: LogEntry = {
          id: `log-${Date.now()}-${Math.random()}`,
          nodeId: node.id,
          nodeName: node.label,
          level: level as LogEntry['level'],
          message: pickRandom(messages),
          timestamp: new Date().toISOString(),
        }

        addLog(log)
      }
    }, 1000)

    return () => {
      clearInterval(intervalRef.current)
    }
  }, [enabled, setNodes, setEdges, addLog, setConnectionStatus, updateNode])
}
