'use client'

import { useMemo } from 'react'
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts'
import { Card, SectionHeader, MetricCard } from '@/components/ui'
import { useTelemetryStore } from '@/store'
import { formatPercent, formatLatency, formatNumber } from '@/utils'
import { Activity, TrendingUp, AlertTriangle, Cpu } from 'lucide-react'

function generateTimeSeriesData(points = 30, baseValue = 50, variance = 15) {
  return Array.from({ length: points }, (_, i) => ({
    time: `${String(Math.floor((i * 2) / 60)).padStart(2, '0')}:${String((i * 2) % 60).padStart(2, '0')}`,
    value: Math.max(0, Math.min(100, baseValue + (Math.random() - 0.5) * variance * 2)),
  }))
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-white border border-[#E5E7EB] rounded-lg shadow-lg px-3 py-2 text-xs">
      <p className="text-[#6B7280] mb-1">{label}</p>
      {payload.map((p: any) => (
        <p key={p.name} style={{ color: p.color }} className="font-medium">
          {p.name}: {p.value.toFixed(1)}{p.unit ?? ''}
        </p>
      ))}
    </div>
  )
}

export function AnalyticsView() {
  const { nodes } = useTelemetryStore()

  const cpuData = useMemo(() => generateTimeSeriesData(30, 42, 15), [])
  const memoryData = useMemo(() => generateTimeSeriesData(30, 60, 10), [])
  const latencyData = useMemo(() => generateTimeSeriesData(30, 85, 30), [])
  const packetData = useMemo(() => generateTimeSeriesData(30, 350, 120), [])

  const totalPackets = nodes.reduce((s, n) => s + n.metrics.packetCount, 0)
  const avgCpu = nodes.length
    ? nodes.reduce((s, n) => s + n.metrics.cpu, 0) / nodes.length
    : 0
  const totalErrors = nodes.reduce((s, n) => s + n.metrics.errorCount, 0)
  const avgLatency = nodes.length
    ? nodes.reduce((s, n) => s + n.metrics.latency, 0) / nodes.length
    : 0

  return (
    <div className="p-6 space-y-6">
      <SectionHeader
        title="Analytics"
        description="System-wide performance trends and historical data"
      />

      {/* Summary metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          label="Avg CPU"
          value={avgCpu.toFixed(1)}
          unit="%"
          icon={<Cpu className="w-4 h-4" />}
          trend={avgCpu > 70 ? 'up' : 'neutral'}
          trendValue={avgCpu > 70 ? 'Above threshold' : 'Normal'}
        />
        <MetricCard
          label="Avg Latency"
          value={avgLatency.toFixed(0)}
          unit="ms"
          icon={<Activity className="w-4 h-4" />}
        />
        <MetricCard
          label="Total Packets"
          value={formatNumber(totalPackets)}
          icon={<TrendingUp className="w-4 h-4" />}
        />
        <MetricCard
          label="Total Errors"
          value={String(totalErrors)}
          icon={<AlertTriangle className="w-4 h-4" />}
          trend={totalErrors > 0 ? 'up' : 'neutral'}
          trendValue={totalErrors > 0 ? `${totalErrors} errors` : 'No errors'}
        />
      </div>

      {/* Charts grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CPU over time */}
        <Card>
          <h3 className="text-sm font-semibold text-[#111827] mb-4">CPU Usage</h3>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={cpuData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
              <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#9CA3AF' }} tickLine={false} axisLine={false} />
              <YAxis tick={{ fontSize: 10, fill: '#9CA3AF' }} tickLine={false} axisLine={false} domain={[0, 100]} unit="%" />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="value"
                name="CPU"
                stroke="#2563EB"
                fill="#EFF6FF"
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        </Card>

        {/* Memory over time */}
        <Card>
          <h3 className="text-sm font-semibold text-[#111827] mb-4">Memory Usage</h3>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={memoryData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
              <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#9CA3AF' }} tickLine={false} axisLine={false} />
              <YAxis tick={{ fontSize: 10, fill: '#9CA3AF' }} tickLine={false} axisLine={false} domain={[0, 100]} unit="%" />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="value"
                name="Memory"
                stroke="#16A34A"
                fill="#F0FDF4"
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        </Card>

        {/* Latency */}
        <Card>
          <h3 className="text-sm font-semibold text-[#111827] mb-4">Latency (ms)</h3>
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={latencyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
              <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#9CA3AF' }} tickLine={false} axisLine={false} />
              <YAxis tick={{ fontSize: 10, fill: '#9CA3AF' }} tickLine={false} axisLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone"
                dataKey="value"
                name="Latency"
                stroke="#D97706"
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Packet rate */}
        <Card>
          <h3 className="text-sm font-semibold text-[#111827] mb-4">Packet Rate (/s)</h3>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={packetData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
              <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#9CA3AF' }} tickLine={false} axisLine={false} />
              <YAxis tick={{ fontSize: 10, fill: '#9CA3AF' }} tickLine={false} axisLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" name="Packets" fill="#2563EB" radius={[2, 2, 0, 0]} isAnimationActive={false} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Per-node table */}
      <Card padding="none">
        <div className="px-4 py-3 border-b border-[#E5E7EB]">
          <h3 className="text-sm font-semibold text-[#111827]">Node Performance</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[#F3F4F6]">
                <th className="text-left text-xs text-[#6B7280] font-medium px-4 py-2">Node</th>
                <th className="text-right text-xs text-[#6B7280] font-medium px-4 py-2">CPU</th>
                <th className="text-right text-xs text-[#6B7280] font-medium px-4 py-2">Memory</th>
                <th className="text-right text-xs text-[#6B7280] font-medium px-4 py-2">Latency</th>
                <th className="text-right text-xs text-[#6B7280] font-medium px-4 py-2">Packets/s</th>
                <th className="text-right text-xs text-[#6B7280] font-medium px-4 py-2">Errors</th>
              </tr>
            </thead>
            <tbody>
              {nodes.map((node) => (
                <tr key={node.id} className="border-b border-[#F9FAFB] hover:bg-[#F9FAFB]">
                  <td className="px-4 py-2.5 font-medium text-[#111827]">{node.label}</td>
                  <td className="px-4 py-2.5 text-right font-tabular-nums text-[#374151]">
                    {formatPercent(node.metrics.cpu, 1)}
                  </td>
                  <td className="px-4 py-2.5 text-right font-tabular-nums text-[#374151]">
                    {formatPercent(node.metrics.memory, 1)}
                  </td>
                  <td className="px-4 py-2.5 text-right font-tabular-nums text-[#374151]">
                    {formatLatency(node.metrics.latency)}
                  </td>
                  <td className="px-4 py-2.5 text-right font-tabular-nums text-[#374151]">
                    {Math.round(node.metrics.packetRate)}
                  </td>
                  <td className="px-4 py-2.5 text-right font-tabular-nums">
                    <span className={node.metrics.errorCount > 0 ? 'text-red-600 font-semibold' : 'text-[#374151]'}>
                      {node.metrics.errorCount}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
