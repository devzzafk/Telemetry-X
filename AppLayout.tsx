// ─── Node & Connection Types ──────────────────────────────────────────────────

export type NodeStatus = 'online' | 'warning' | 'error' | 'offline' | 'unknown'
export type NodeType =
  | 'esp32'
  | 'raspberry-pi'
  | 'backend'
  | 'frontend'
  | 'database'
  | 'cache'
  | 'gateway'
  | 'broker'
  | 'sensor'
  | 'api'
  | 'service'
  | 'generic'

export interface NodeMetrics {
  cpu: number             // 0-100%
  memory: number          // 0-100%
  latency: number         // ms
  packetCount: number
  packetRate: number      // packets/sec
  temperature?: number    // °C
  voltage?: number        // V
  errorCount: number
  networkIn: number       // bytes/sec
  networkOut: number      // bytes/sec
  uptime: number          // seconds
  fps?: number
  connectedClients?: number
  customMetrics?: Record<string, number>
}

export interface TelemetryNode {
  id: string
  label: string
  type: NodeType
  status: NodeStatus
  metrics: NodeMetrics
  position: { x: number; y: number }
  group?: string
  tags?: string[]
  lastSeen: string        // ISO timestamp
  createdAt: string
  meta?: Record<string, unknown>
}

export interface TelemetryEdge {
  id: string
  source: string
  target: string
  status: 'active' | 'inactive' | 'error'
  packetRate: number
  latency: number
  label?: string
  protocol?: string
}

// ─── Event & Log Types ────────────────────────────────────────────────────────

export type LogLevel = 'debug' | 'info' | 'warning' | 'error' | 'fatal'

export interface LogEntry {
  id: string
  nodeId: string
  nodeName: string
  level: LogLevel
  message: string
  timestamp: string
  data?: Record<string, unknown>
  traceId?: string
  spanId?: string
}

export interface TelemetryEvent {
  id: string
  type:
    | 'metric_update'
    | 'status_change'
    | 'connection_change'
    | 'log'
    | 'crash'
    | 'alert'
    | 'custom'
  nodeId: string
  timestamp: string
  payload: Record<string, unknown>
  severity?: 'low' | 'medium' | 'high' | 'critical'
}

// ─── Replay Types ─────────────────────────────────────────────────────────────

export interface ReplayFrame {
  timestamp: string
  nodes: TelemetryNode[]
  edges: TelemetryEdge[]
  logs: LogEntry[]
  events: TelemetryEvent[]
}

export interface ReplaySession {
  id: string
  name: string
  startTime: string
  endTime: string
  duration: number        // seconds
  frames: ReplayFrame[]
  crashAt?: string        // ISO timestamp
  projectId: string
}

export type ReplayStatus = 'idle' | 'playing' | 'paused' | 'ended'

export interface ReplayState {
  status: ReplayStatus
  currentTime: number     // seconds from start
  speed: number           // 0.25, 0.5, 1, 2, 4
  session: ReplaySession | null
  currentFrame: ReplayFrame | null
}

// ─── Alert Types ──────────────────────────────────────────────────────────────

export type AlertSeverity = 'low' | 'medium' | 'high' | 'critical'
export type AlertStatus = 'active' | 'acknowledged' | 'resolved'
export type AlertTrigger = 'threshold' | 'anomaly' | 'disconnect' | 'crash' | 'custom'

export interface AlertRule {
  id: string
  name: string
  nodeId?: string         // null = applies to all nodes
  metric: string
  operator: '>' | '<' | '>=' | '<=' | '==' | '!='
  threshold: number
  severity: AlertSeverity
  trigger: AlertTrigger
  cooldown: number        // seconds between triggers
  enabled: boolean
  createdAt: string
}

export interface Alert {
  id: string
  ruleId: string
  ruleName: string
  nodeId: string
  nodeName: string
  severity: AlertSeverity
  status: AlertStatus
  message: string
  value: number
  threshold: number
  triggeredAt: string
  acknowledgedAt?: string
  resolvedAt?: string
}

// ─── Project Types ────────────────────────────────────────────────────────────

export interface Project {
  id: string
  name: string
  slug: string
  description?: string
  nodeCount: number
  status: 'active' | 'inactive' | 'degraded'
  createdAt: string
  updatedAt: string
  tags?: string[]
}

// ─── Analytics Types ──────────────────────────────────────────────────────────

export interface MetricDataPoint {
  timestamp: string
  value: number
}

export interface MetricSeries {
  nodeId: string
  nodeName: string
  metric: string
  data: MetricDataPoint[]
}

export interface AnalyticsSummary {
  totalEvents: number
  totalErrors: number
  avgLatency: number
  uptimePercent: number
  peakPacketRate: number
  activeAlerts: number
  period: {
    from: string
    to: string
  }
}

// ─── WebSocket Message Types ──────────────────────────────────────────────────

export type WsMessageType =
  | 'node_update'
  | 'node_added'
  | 'node_removed'
  | 'edge_update'
  | 'log'
  | 'event'
  | 'alert'
  | 'crash'
  | 'ping'
  | 'pong'
  | 'error'

export interface WsMessage {
  type: WsMessageType
  payload: unknown
  timestamp: string
}

// ─── UI / App State Types ─────────────────────────────────────────────────────

export interface SidebarItem {
  id: string
  label: string
  href: string
  icon: string
  badge?: number | string
  children?: SidebarItem[]
}

export type ThemeMode = 'light' | 'dark' | 'system'

export interface AppSettings {
  theme: ThemeMode
  sidebarCollapsed: boolean
  inspectorOpen: boolean
  selectedNodeId: string | null
  autoScrollLogs: boolean
  showMinimap: boolean
  animationsEnabled: boolean
}
