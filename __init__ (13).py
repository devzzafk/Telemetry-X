'use client'

import { Bell, CheckCircle, AlertTriangle, AlertCircle, Plus } from 'lucide-react'
import { Card, SectionHeader, Badge, Button, StatusDot } from '@/components/ui'
import { useTelemetryStore } from '@/store'
import { formatRelativeTime, getSeverityColor, cn } from '@/utils'
import type { AlertSeverity } from '@/types'

const SEVERITY_BADGE: Record<AlertSeverity, 'info' | 'warning' | 'error' | 'default'> = {
  low: 'info',
  medium: 'warning',
  high: 'error',
  critical: 'error',
}

// Mock alert rules
const ALERT_RULES = [
  { id: 'r1', name: 'CPU > 90%', metric: 'cpu', threshold: 90, severity: 'high', enabled: true },
  { id: 'r2', name: 'Memory > 95%', metric: 'memory', threshold: 95, severity: 'critical', enabled: true },
  { id: 'r3', name: 'Latency > 500ms', metric: 'latency', threshold: 500, severity: 'medium', enabled: true },
  { id: 'r4', name: 'Error Count > 10', metric: 'errorCount', threshold: 10, severity: 'high', enabled: false },
]

export function AlertsView() {
  const { alerts, acknowledgeAlert, resolveAlert } = useTelemetryStore()

  const active = alerts.filter((a) => a.status === 'active')
  const acknowledged = alerts.filter((a) => a.status === 'acknowledged')
  const resolved = alerts.filter((a) => a.status === 'resolved')

  return (
    <div className="p-6 space-y-8">
      {/* Header */}
      <SectionHeader
        title="Alerts"
        description={`${active.length} active, ${acknowledged.length} acknowledged`}
        action={
          <Button variant="primary" size="sm">
            <Plus className="w-3.5 h-3.5" />
            New Rule
          </Button>
        }
      />

      {/* Active alerts */}
      {active.length > 0 && (
        <section>
          <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-3">
            Active — {active.length}
          </h3>
          <div className="space-y-2">
            {active.map((alert) => (
              <Card key={alert.id} className="flex items-start gap-4 border-l-4 border-l-red-500">
                <AlertTriangle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-semibold text-[#111827]">{alert.ruleName}</span>
                    <Badge variant={SEVERITY_BADGE[alert.severity]}>{alert.severity}</Badge>
                  </div>
                  <p className="text-sm text-[#6B7280] mb-1">{alert.message}</p>
                  <span className="text-xs text-[#9CA3AF]">{formatRelativeTime(alert.triggeredAt)}</span>
                </div>
                <div className="flex gap-2 flex-shrink-0">
                  <Button size="sm" variant="secondary" onClick={() => acknowledgeAlert(alert.id)}>
                    Acknowledge
                  </Button>
                  <Button size="sm" variant="ghost" onClick={() => resolveAlert(alert.id)}>
                    Resolve
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </section>
      )}

      {/* Alert rules */}
      <section>
        <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-3">
          Alert Rules
        </h3>
        <div className="space-y-2">
          {ALERT_RULES.map((rule) => (
            <Card key={rule.id} className="flex items-center gap-4">
              <div
                className={cn(
                  'w-2 h-2 rounded-full flex-shrink-0',
                  rule.enabled ? 'bg-green-500' : 'bg-gray-300'
                )}
              />
              <div className="flex-1 min-w-0">
                <span className="text-sm font-medium text-[#111827]">{rule.name}</span>
                <div className="text-xs text-[#6B7280] mt-0.5">
                  {rule.metric} {rule.metric === 'latency' ? `> ${rule.threshold}ms` : `> ${rule.threshold}`}
                </div>
              </div>
              <Badge variant={SEVERITY_BADGE[rule.severity as AlertSeverity]}>{rule.severity}</Badge>
              <button className="text-xs text-[#2563EB] hover:underline">
                {rule.enabled ? 'Disable' : 'Enable'}
              </button>
            </Card>
          ))}
        </div>
      </section>

      {/* Resolved */}
      {resolved.length > 0 && (
        <section>
          <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-3">
            Resolved — {resolved.length}
          </h3>
          <div className="space-y-2">
            {resolved.slice(0, 5).map((alert) => (
              <Card key={alert.id} className="flex items-center gap-3 opacity-60">
                <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                <span className="text-sm text-[#374151]">{alert.ruleName}</span>
                <span className="text-xs text-[#9CA3AF] ml-auto">
                  {alert.resolvedAt ? formatRelativeTime(alert.resolvedAt) : '—'}
                </span>
              </Card>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
