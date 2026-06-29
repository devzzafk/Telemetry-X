'use client'

import { Search, Bell, Settings, ChevronDown, Circle } from 'lucide-react'
import { useTelemetryStore, useProjectStore } from '@/store'
import { cn } from '@/utils'
import Link from 'next/link'

export function Topbar() {
  const { connectionStatus, alerts } = useTelemetryStore()
  const { activeProject, projects } = useProjectStore()

  const activeAlerts = alerts.filter((a) => a.status === 'active')
  const isConnected = connectionStatus === 'connected'

  return (
    <header className="h-[52px] border-b border-[#E5E7EB] bg-white flex items-center px-4 gap-4 flex-shrink-0 z-30">
      {/* Logo */}
      <Link href="/" className="flex items-center gap-2 mr-2 flex-shrink-0">
        <div className="w-6 h-6 rounded bg-[#2563EB] flex items-center justify-center">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <circle cx="7" cy="7" r="5" stroke="white" strokeWidth="1.5" />
            <circle cx="7" cy="7" r="2" fill="white" />
          </svg>
        </div>
        <span className="font-semibold text-sm text-[#111827] tracking-tight">Telemetry-X</span>
      </Link>

      {/* Project switcher */}
      <button className="flex items-center gap-1.5 h-7 px-2.5 rounded-md text-sm text-[#111827] hover:bg-[#F3F4F6] transition-colors border border-transparent hover:border-[#E5E7EB]">
        <span className="font-medium">{activeProject?.name ?? 'My Project'}</span>
        <ChevronDown className="w-3.5 h-3.5 text-[#6B7280]" />
      </button>

      {/* Divider */}
      <div className="h-5 w-px bg-[#E5E7EB]" />

      {/* Search */}
      <div className="flex-1 max-w-md">
        <label className="flex items-center gap-2 h-8 px-3 bg-[#F9FAFB] border border-[#E5E7EB] rounded-md cursor-text">
          <Search className="w-3.5 h-3.5 text-[#9CA3AF] flex-shrink-0" />
          <span className="text-sm text-[#9CA3AF]">Search nodes, logs, events...</span>
          <kbd className="ml-auto text-[11px] text-[#9CA3AF] border border-[#E5E7EB] rounded px-1 py-0.5 bg-white font-mono">⌘K</kbd>
        </label>
      </div>

      {/* Right section */}
      <div className="ml-auto flex items-center gap-2">
        {/* Connection status */}
        <div
          className={cn(
            'flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full font-medium',
            isConnected ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-500'
          )}
        >
          <Circle
            className={cn(
              'w-1.5 h-1.5 fill-current',
              isConnected ? 'text-green-500' : 'text-gray-400'
            )}
          />
          <span>{isConnected ? 'Live' : connectionStatus}</span>
        </div>

        {/* Alerts bell */}
        <button className="relative w-8 h-8 flex items-center justify-center rounded-md hover:bg-[#F3F4F6] transition-colors">
          <Bell className="w-4 h-4 text-[#6B7280]" />
          {activeAlerts.length > 0 && (
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
          )}
        </button>

        {/* Settings */}
        <button className="w-8 h-8 flex items-center justify-center rounded-md hover:bg-[#F3F4F6] transition-colors">
          <Settings className="w-4 h-4 text-[#6B7280]" />
        </button>

        {/* Avatar */}
        <div className="w-7 h-7 rounded-full bg-[#2563EB] flex items-center justify-center text-white text-xs font-semibold">
          TX
        </div>
      </div>
    </header>
  )
}
