'use client'

import { History, Play, AlertTriangle, Clock, Calendar } from 'lucide-react'
import { Card, SectionHeader, Badge, Button, EmptyState } from '@/components/ui'
import { useReplayStore } from '@/store'

const MOCK_SESSIONS = [
  {
    id: 'replay-001',
    name: 'Production Crash – API Gateway',
    startTime: new Date(Date.now() - 3600000 * 2).toISOString(),
    duration: 420,
    hasCrash: true,
    nodeCount: 6,
  },
  {
    id: 'replay-002',
    name: 'Memory Spike – Backend Service',
    startTime: new Date(Date.now() - 3600000 * 8).toISOString(),
    duration: 180,
    hasCrash: false,
    nodeCount: 4,
  },
  {
    id: 'replay-003',
    name: 'ESP32 Disconnect Event',
    startTime: new Date(Date.now() - 3600000 * 24).toISOString(),
    duration: 90,
    hasCrash: true,
    nodeCount: 3,
  },
]

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatDuration(secs: number) {
  const m = Math.floor(secs / 60)
  const s = secs % 60
  return `${m}m ${s}s`
}

export function ReplayView() {
  const { setStatus } = useReplayStore()

  return (
    <div className="p-6 space-y-6">
      <SectionHeader
        title="Replay Sessions"
        description="Review recorded telemetry sessions. Jump to any point in time and inspect what happened."
        action={
          <Button variant="primary" size="sm">
            <History className="w-3.5 h-3.5" />
            New Recording
          </Button>
        }
      />

      {/* Sessions list */}
      <div className="space-y-2">
        {MOCK_SESSIONS.map((session) => (
          <Card key={session.id} className="flex items-center gap-4 hover:border-[#D1D5DB] transition-colors cursor-pointer">
            <div
              className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                session.hasCrash ? 'bg-red-50' : 'bg-blue-50'
              }`}
            >
              {session.hasCrash ? (
                <AlertTriangle className="w-4 h-4 text-red-500" />
              ) : (
                <History className="w-4 h-4 text-blue-500" />
              )}
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold text-[#111827]">{session.name}</span>
                {session.hasCrash && (
                  <Badge variant="error">Crash</Badge>
                )}
              </div>
              <div className="flex items-center gap-4 text-xs text-[#6B7280]">
                <span className="flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  {formatDate(session.startTime)}
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {formatDuration(session.duration)}
                </span>
                <span>{session.nodeCount} nodes</span>
              </div>
            </div>

            <Button
              variant="secondary"
              size="sm"
              onClick={() => setStatus('playing')}
            >
              <Play className="w-3 h-3" />
              Replay
            </Button>
          </Card>
        ))}
      </div>

      {MOCK_SESSIONS.length === 0 && (
        <EmptyState
          icon={<History className="w-8 h-8" />}
          title="No replay sessions"
          description="Sessions are automatically recorded when telemetry is streaming. Start a project to begin."
        />
      )}
    </div>
  )
}
