'use client'

import { useMemo } from 'react'
import {
  X, Cpu, MemoryStick, Wifi, Activity,
  Thermometer, Zap, AlertTriangle, Clock,
  CheckCircle, WifiOff, AlertCircle,
} from 'lucide-react'
import {
  LineChart, Line, ResponsiveContainer, Tooltip, YAxis,
} from 'recharts'
import { useTelemetryStore, useAppSettingsStore } from '@/store'
import {
  formatPercent, formatLatency, formatUptime,
  formatBytes, formatRelativeTime, cn,
} from '@/utils'

interface MetricRowProps {
  label: string
  value: string
  icon: React.ElementType
  status?: 'ok' | 'warning' | 'error'
  subValue?: string
}

function MetricRow({ label, value, icon: Icon, status = 'ok', subValue }: MetricRowProps) {
  return (
    <div className="flex items-center gap-3 py-2.5 border-b border-[#F3F4F6] last:border-b-0">
      <div
        className={cn(
          'w-7 h-7 rounded-md flex items-center justify-center flex-shrink-0',
          status === 'error' ? 'bg-red-50' : status === 'warning' ? 'bg-orange-50' : 'bg-[#F9FAFB]'
        )}
      >
        <Icon
          className={cn(
            'w-3.5 h-3.5',
            status === 'error' ? 'text-red-600' : status === 'warning' ? 'text-orange-600' : 'text-[#6B7280]'
          )}
        />
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-[11px] text-[#9CA3AF]">{label}</div>
        <div className="text-sm font-semibold text-[#111827] font-tabular-nums">{value}</div>
      </div>
      {subValue && <div className="text-xs text-[#9CA3AF]">{subValue}</div>}
    </div>
  )
}

function SparklineChart({ value, color }: { value: number; color: string }) {
  const data = useMemo(() => {
    // Simulate sparkline history
    return Array.from({ length: 20 }, (_, i) => ({
      v: Math.max(0, Math.min(100, value + (Math.random() - 0.5) * 20)),
    }))
  }, [value])

  return (
    <ResponsiveContainer width="100%" height={40}>
      <LineChart data={data}>
        <Line
          type="monotone"
          dataKey="v"
          stroke={color}
          strokeWidth={1.5}
          dot={false}
          isAnimationActive={false}
        />
        <YAxis domain={[0, 100]} hide />
      </LineChart>
    </ResponsiveContainer>
  )
}

interface NodeInspectorProps {
  nodeId: string
}

export function NodeInspector({ nodeId }: NodeInspectorProps) {
  const { nodes } = useTelemetryStore()
  const { setSelectedNode } = useAppSettingsStore()

  const node = nodes.find((n) => n.id === nodeId)

  if (!node) return null

  const m = node.metrics

  const statusIcon = {
    online: <CheckCircle className="w-3.5 h-3.5 text-green-500" />,
    warning: <AlertCircle className="w-3.5 h-3.5 text-orange-500" />,
    error: <AlertTriangle className="w-3.5 h-3.5 text-red-500" />,
    offline: <WifiOff className="w-3.5 h-3.5 text-gray-400" />,
    unknown: <AlertCircle className="w-3.5 h-3.5 text-gray-400" />,
  }[node.status]

  const statusLabel = {
    online: 'Online',
    warning: 'Warning',
    error: 'Error',
    offline: 'Offline',
    unknown: 'Unknown',
  }[node.status]

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-3 px-4 py-3 border-b border-[#E5E7EB]">
        <div className="flex-1 min-w-0">
          <div className="text-sm font-semibold text-[#111827] truncate">{node.label}</div>
          <div className="flex items-center gap-1.5 mt-0.5">
            {statusIcon}
            <span className="text-xs text-[#6B7280]">{statusLabel}</span>
            <span className="text-[#D1D5DB]">·</span>
            <span className="text-xs text-[#9CA3AF] capitalize">{node.type.replace('-', ' ')}</span>
          </div>
        </div>
        <button
          onClick={() => setSelectedNode(null)}
          className="w-7 h-7 rounded-md hover:bg-[#F3F4F6] flex items-center justify-center text-[#6B7280] transition-colors"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {/* CPU sparkline */}
        <div className="px-4 pt-4 pb-2">
          <div className="flex justify-between items-center mb-1">
            <span className="text-xs font-medium text-[#374151]">CPU Usage</span>
            <span className="text-xs font-semibold text-[#111827] font-tabular-nums">
              {formatPercent(m.cpu, 1)}
            </span>
          </div>
          <SparklineChart value={m.cpu} color={m.cpu > 80 ? '#DC2626' : '#2563EB'} />
          <div className="w-full h-1.5 bg-[#F3F4F6] rounded-full overflow-hidden mt-1">
            <div
              className={cn(
                'h-full rounded-full transition-all duration-500',
                m.cpu > 90 ? 'bg-red-500' : m.cpu > 70 ? 'bg-orange-500' : 'bg-[#2563EB]'
              )}
              style={{ width: `${Math.min(m.cpu, 100)}%` }}
            />
          </div>
        </div>

        {/* Memory sparkline */}
        <div className="px-4 pb-2">
          <div className="flex justify-between items-center mb-1">
            <span className="text-xs font-medium text-[#374151]">Memory</span>
            <span className="text-xs font-semibold text-[#111827] font-tabular-nums">
              {formatPercent(m.memory, 1)}
            </span>
          </div>
          <SparklineChart value={m.memory} color={m.memory > 85 ? '#D97706' : '#16A34A'} />
          <div className="w-full h-1.5 bg-[#F3F4F6] rounded-full overflow-hidden mt-1">
            <div
              className={cn(
                'h-full rounded-full transition-all duration-500',
                m.memory > 95 ? 'bg-red-500' : m.memory > 80 ? 'bg-orange-500' : 'bg-green-500'
              )}
              style={{ width: `${Math.min(m.memory, 100)}%` }}
            />
          </div>
        </div>

        <div className="border-t border-[#F3F4F6] mx-4" />

        {/* Metric rows */}
        <div className="px-4 py-1">
          <MetricRow
            label="Latency"
            value={formatLatency(m.latency)}
            icon={Zap}
            status={m.latency > 500 ? 'error' : m.latency > 200 ? 'warning' : 'ok'}
          />
          <MetricRow
            label="Packet Rate"
            value={`${Math.round(m.packetRate)}/s`}
            icon={Activity}
            subValue={`${m.packetCount.toLocaleString()} total`}
          />
          <MetricRow
            label="Network In"
            value={`${formatBytes(m.networkIn)}/s`}
            icon={Wifi}
          />
          <MetricRow
            label="Network Out"
            value={`${formatBytes(m.networkOut)}/s`}
            icon={Wifi}
          />
          <MetricRow
            label="Uptime"
            value={formatUptime(m.uptime)}
            icon={Clock}
          />
          {m.errorCount > 0 && (
            <MetricRow
              label="Errors"
              value={String(m.errorCount)}
              icon={AlertTriangle}
              status="error"
            />
          )}
          {m.temperature !== undefined && (
            <MetricRow
              label="Temperature"
              value={`${m.temperature.toFixed(1)}°C`}
              icon={Thermometer}
              status={m.temperature > 80 ? 'error' : m.temperature > 70 ? 'warning' : 'ok'}
            />
          )}
          {m.voltage !== undefined && (
            <MetricRow
              label="Voltage"
              value={`${m.voltage.toFixed(1)}V`}
              icon={Zap}
            />
          )}
          {m.connectedClients !== undefined && (
            <MetricRow
              label="Connected Clients"
              value={String(m.connectedClients)}
              icon={Wifi}
            />
          )}
          {m.fps !== undefined && (
            <MetricRow
              label="FPS"
              value={`${m.fps.toFixed(0)} fps`}
              icon={Activity}
            />
          )}
        </div>

        {/* Tags */}
        {node.tags && node.tags.length > 0 && (
          <div className="px-4 pb-4">
            <div className="border-t border-[#F3F4F6] pt-3 mb-2">
              <span className="text-[11px] text-[#9CA3AF] uppercase tracking-wide">Tags</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {node.tags.map((tag) => (
                <span
                  key={tag}
                  className="text-[11px] px-2 py-0.5 bg-[#F3F4F6] text-[#6B7280] rounded-md font-medium"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Last seen */}
        <div className="px-4 pb-4 text-[11px] text-[#9CA3AF]">
          Last seen {formatRelativeTime(node.lastSeen)}
        </div>
      </div>
    </div>
  )
}
