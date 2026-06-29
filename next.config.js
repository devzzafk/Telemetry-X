'use client'

import { memo } from 'react'
import { Handle, Position, type NodeProps } from 'reactflow'
import {
  Cpu, Wifi, Database, Server, Monitor,
  HardDrive, Radio, GitBranch, Microchip,
  AlertTriangle, WifiOff, Activity,
} from 'lucide-react'
import { cn, formatPercent, formatLatency } from '@/utils'
import { useAppSettingsStore } from '@/store'
import type { TelemetryNode, NodeType } from '@/types'

const NODE_ICONS: Record<NodeType, React.ElementType> = {
  'esp32': Microchip,
  'raspberry-pi': Cpu,
  'backend': Server,
  'frontend': Monitor,
  'database': Database,
  'cache': HardDrive,
  'gateway': GitBranch,
  'broker': Radio,
  'sensor': Activity,
  'api': Wifi,
  'service': Server,
  'generic': Server,
}

const STATUS_STYLES = {
  online: {
    border: 'border-[#E5E7EB]',
    dot: 'bg-green-500',
    badge: 'text-green-700 bg-green-50',
    ring: '',
  },
  warning: {
    border: 'border-orange-200',
    dot: 'bg-orange-500',
    badge: 'text-orange-700 bg-orange-50',
    ring: 'ring-2 ring-orange-200',
  },
  error: {
    border: 'border-red-200',
    dot: 'bg-red-500',
    badge: 'text-red-700 bg-red-50',
    ring: 'ring-2 ring-red-200',
  },
  offline: {
    border: 'border-gray-200',
    dot: 'bg-gray-400',
    badge: 'text-gray-500 bg-gray-50',
    ring: '',
  },
  unknown: {
    border: 'border-gray-200',
    dot: 'bg-gray-300',
    badge: 'text-gray-400 bg-gray-50',
    ring: '',
  },
}

function CPUBar({ value }: { value: number }) {
  const color = value > 90 ? 'bg-red-500' : value > 70 ? 'bg-orange-500' : 'bg-[#2563EB]'
  return (
    <div className="w-full h-1 bg-[#F3F4F6] rounded-full overflow-hidden">
      <div
        className={cn('h-full rounded-full transition-all duration-700', color)}
        style={{ width: `${Math.min(value, 100)}%` }}
      />
    </div>
  )
}

export const TelemetryNodeComponent = memo(function TelemetryNodeComponent({
  data,
  selected,
}: NodeProps<TelemetryNode>) {
  const Icon = NODE_ICONS[data.type] ?? Server
  const style = STATUS_STYLES[data.status] ?? STATUS_STYLES.unknown
  const { selectedNodeId } = useAppSettingsStore()
  const isSelected = selected || selectedNodeId === data.id

  return (
    <div
      className={cn(
        'bg-white border rounded-xl shadow-sm min-w-[180px] cursor-pointer select-none transition-all duration-150',
        style.border,
        style.ring,
        isSelected && 'shadow-md ring-2 ring-[#2563EB] ring-offset-1 border-[#2563EB]'
      )}
    >
      {/* Handles */}
      <Handle type="target" position={Position.Left} className="!w-2 !h-2 !border-[#CBD5E1] !bg-white" />
      <Handle type="source" position={Position.Right} className="!w-2 !h-2 !border-[#CBD5E1] !bg-white" />

      {/* Header */}
      <div className="flex items-center gap-2 px-3 pt-3 pb-2 border-b border-[#F3F4F6]">
        <div
          className={cn(
            'w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0',
            data.status === 'error' ? 'bg-red-50' :
            data.status === 'warning' ? 'bg-orange-50' :
            data.status === 'offline' ? 'bg-gray-50' : 'bg-blue-50'
          )}
        >
          <Icon
            className={cn(
              'w-4 h-4',
              data.status === 'error' ? 'text-red-500' :
              data.status === 'warning' ? 'text-orange-500' :
              data.status === 'offline' ? 'text-gray-400' : 'text-[#2563EB]'
            )}
          />
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-xs font-semibold text-[#111827] truncate">{data.label}</div>
          <div className="text-[10px] text-[#9CA3AF] capitalize">{data.type.replace('-', ' ')}</div>
        </div>
        <div className="flex items-center gap-1">
          {data.status === 'offline' ? (
            <WifiOff className="w-3 h-3 text-gray-400" />
          ) : data.status === 'error' ? (
            <AlertTriangle className="w-3 h-3 text-red-500" />
          ) : (
            <span className={cn('w-2 h-2 rounded-full', style.dot)} />
          )}
        </div>
      </div>

      {/* Metrics */}
      <div className="px-3 py-2 space-y-2">
        <div>
          <div className="flex justify-between items-center mb-1">
            <span className="text-[10px] text-[#9CA3AF]">CPU</span>
            <span className="text-[10px] font-medium text-[#374151] font-tabular-nums">
              {formatPercent(data.metrics.cpu, 0)}
            </span>
          </div>
          <CPUBar value={data.metrics.cpu} />
        </div>

        <div className="flex gap-3">
          <div className="flex-1">
            <div className="text-[10px] text-[#9CA3AF]">Memory</div>
            <div className="text-xs font-medium text-[#374151] font-tabular-nums">
              {formatPercent(data.metrics.memory, 0)}
            </div>
          </div>
          <div className="flex-1">
            <div className="text-[10px] text-[#9CA3AF]">Latency</div>
            <div className="text-xs font-medium text-[#374151] font-tabular-nums">
              {formatLatency(data.metrics.latency)}
            </div>
          </div>
          <div className="flex-1">
            <div className="text-[10px] text-[#9CA3AF]">Packets/s</div>
            <div className="text-xs font-medium text-[#374151] font-tabular-nums">
              {Math.round(data.metrics.packetRate)}
            </div>
          </div>
        </div>

        {data.metrics.errorCount > 0 && (
          <div className="flex items-center gap-1 text-[10px] text-red-600 bg-red-50 px-2 py-1 rounded-md">
            <AlertTriangle className="w-2.5 h-2.5" />
            <span>{data.metrics.errorCount} error{data.metrics.errorCount !== 1 ? 's' : ''}</span>
          </div>
        )}
      </div>
    </div>
  )
})
