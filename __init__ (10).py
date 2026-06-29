'use client'

import { useRef, useEffect, useState, useMemo } from 'react'
import { Search, Filter, Trash2 } from 'lucide-react'
import { useTelemetryStore, useAppSettingsStore } from '@/store'
import { formatTimestamp, getLogLevelColor, cn } from '@/utils'
import type { LogLevel } from '@/types'

const LEVEL_LABELS: Record<LogLevel, string> = {
  debug: 'DBG',
  info: 'INF',
  warning: 'WRN',
  error: 'ERR',
  fatal: 'FTL',
}

const LEVEL_BG: Record<LogLevel, string> = {
  debug: 'bg-gray-100 text-gray-600',
  info: 'bg-blue-50 text-blue-700',
  warning: 'bg-orange-50 text-orange-700',
  error: 'bg-red-50 text-red-700',
  fatal: 'bg-purple-50 text-purple-700',
}

interface LogPanelProps {
  height: number
}

export function LogPanel({ height }: LogPanelProps) {
  const { logs, clearLogs } = useTelemetryStore()
  const { autoScrollLogs } = useAppSettingsStore()
  const scrollRef = useRef<HTMLDivElement>(null)
  const [search, setSearch] = useState('')
  const [levelFilter, setLevelFilter] = useState<LogLevel | 'all'>('all')
  const [nodeFilter, setNodeFilter] = useState<string>('all')

  const filteredLogs = useMemo(() => {
    return logs.filter((log) => {
      if (levelFilter !== 'all' && log.level !== levelFilter) return false
      if (nodeFilter !== 'all' && log.nodeId !== nodeFilter) return false
      if (search && !log.message.toLowerCase().includes(search.toLowerCase())) return false
      return true
    })
  }, [logs, levelFilter, nodeFilter, search])

  const uniqueNodes = useMemo(() => {
    const seen = new Set<string>()
    return logs.filter((l) => {
      if (seen.has(l.nodeId)) return false
      seen.add(l.nodeId)
      return true
    })
  }, [logs])

  useEffect(() => {
    if (autoScrollLogs && scrollRef.current) {
      scrollRef.current.scrollTop = 0
    }
  }, [filteredLogs.length, autoScrollLogs])

  return (
    <div className="flex flex-col h-full">
      {/* Toolbar */}
      <div className="flex items-center gap-2 px-3 py-1.5 border-b border-[#F3F4F6]">
        <div className="flex items-center gap-1.5 bg-[#F9FAFB] border border-[#E5E7EB] rounded-md px-2 h-6 flex-1 max-w-[200px]">
          <Search className="w-3 h-3 text-[#9CA3AF] flex-shrink-0" />
          <input
            type="text"
            placeholder="Filter logs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-transparent text-xs text-[#374151] outline-none w-full placeholder:text-[#9CA3AF]"
          />
        </div>

        {/* Level filter */}
        <div className="flex gap-0.5">
          {(['all', 'debug', 'info', 'warning', 'error'] as const).map((level) => (
            <button
              key={level}
              onClick={() => setLevelFilter(level)}
              className={cn(
                'h-6 px-2 rounded text-[10px] font-medium transition-colors',
                levelFilter === level
                  ? 'bg-[#111827] text-white'
                  : 'text-[#6B7280] hover:bg-[#F3F4F6]'
              )}
            >
              {level === 'all' ? 'All' : level.toUpperCase().slice(0, 3)}
            </button>
          ))}
        </div>

        <div className="ml-auto flex items-center gap-1">
          <span className="text-[10px] text-[#9CA3AF]">{filteredLogs.length} entries</span>
          <button
            onClick={clearLogs}
            className="w-6 h-6 rounded flex items-center justify-center hover:bg-[#F3F4F6] text-[#9CA3AF] transition-colors"
            title="Clear logs"
          >
            <Trash2 className="w-3 h-3" />
          </button>
        </div>
      </div>

      {/* Log entries */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto font-mono text-[11px]"
        style={{ height: height - 36 }}
      >
        {filteredLogs.length === 0 ? (
          <div className="flex items-center justify-center h-full text-[#9CA3AF] text-xs">
            No log entries
          </div>
        ) : (
          filteredLogs.map((log) => (
            <div
              key={log.id}
              className="flex items-start gap-2 px-3 py-1 hover:bg-[#F9FAFB] group border-b border-[#F9FAFB]"
            >
              {/* Timestamp */}
              <span className="text-[#9CA3AF] flex-shrink-0 pt-px">
                {formatTimestamp(log.timestamp)}
              </span>

              {/* Level badge */}
              <span
                className={cn(
                  'flex-shrink-0 px-1 rounded text-[9px] font-bold tracking-wider leading-4',
                  LEVEL_BG[log.level]
                )}
              >
                {LEVEL_LABELS[log.level]}
              </span>

              {/* Node name */}
              <span className="text-[#6B7280] flex-shrink-0 truncate max-w-[80px]" title={log.nodeName}>
                {log.nodeName}
              </span>

              {/* Message */}
              <span
                className={cn('flex-1 break-words leading-4', {
                  'text-[#6B7280]': log.level === 'debug',
                  'text-[#374151]': log.level === 'info',
                  'text-orange-700': log.level === 'warning',
                  'text-red-700': log.level === 'error',
                  'text-purple-700': log.level === 'fatal',
                })}
              >
                {log.message}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
