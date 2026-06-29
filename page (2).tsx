'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  LayoutDashboard,
  GitBranch,
  Monitor,
  Radio,
  History,
  Bell,
  BarChart2,
  Settings,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react'
import { useAppSettingsStore, useTelemetryStore } from '@/store'
import { cn } from '@/utils'

interface NavItem {
  href: string
  label: string
  icon: React.ElementType
  badgeKey?: 'alerts'
}

const NAV_ITEMS: NavItem[] = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/dashboard', label: 'Projects', icon: GitBranch },
  { href: '/devices', label: 'Devices', icon: Monitor },
  { href: '/dashboard', label: 'Telemetry', icon: Radio },
  { href: '/replay', label: 'Replay', icon: History },
  { href: '/alerts', label: 'Alerts', icon: Bell, badgeKey: 'alerts' },
  { href: '/analytics', label: 'Analytics', icon: BarChart2 },
]

export function Sidebar() {
  const pathname = usePathname()
  const { sidebarCollapsed, toggleSidebar } = useAppSettingsStore()
  const { alerts } = useTelemetryStore()

  const activeAlertCount = alerts.filter((a) => a.status === 'active').length

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-full flex flex-col bg-white border-r border-[#E5E7EB] z-40 transition-all duration-200',
        sidebarCollapsed ? 'w-14' : 'w-[220px]'
      )}
    >
      {/* Logo space — matches topbar height */}
      <div className="h-[52px] flex items-center justify-between px-3 border-b border-[#E5E7EB] flex-shrink-0">
        {!sidebarCollapsed && (
          <span className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider">Navigation</span>
        )}
        <button
          onClick={toggleSidebar}
          className={cn(
            'w-6 h-6 rounded-md hover:bg-[#F3F4F6] flex items-center justify-center transition-colors text-[#6B7280]',
            sidebarCollapsed && 'mx-auto'
          )}
          title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {sidebarCollapsed ? (
            <ChevronRight className="w-3.5 h-3.5" />
          ) : (
            <ChevronLeft className="w-3.5 h-3.5" />
          )}
        </button>
      </div>

      {/* Nav */}
      <nav className="flex-1 py-3 px-2 space-y-0.5 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          const badge = item.badgeKey === 'alerts' ? activeAlertCount : null

          return (
            <Link
              key={item.label}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-2 py-2 rounded-md text-sm font-medium transition-colors group relative',
                isActive
                  ? 'bg-[#EFF6FF] text-[#2563EB]'
                  : 'text-[#374151] hover:bg-[#F9FAFB] hover:text-[#111827]',
                sidebarCollapsed && 'justify-center px-2'
              )}
              title={sidebarCollapsed ? item.label : undefined}
            >
              <Icon
                className={cn(
                  'w-4 h-4 flex-shrink-0',
                  isActive ? 'text-[#2563EB]' : 'text-[#9CA3AF] group-hover:text-[#6B7280]'
                )}
              />

              {!sidebarCollapsed && (
                <>
                  <span className="flex-1 leading-none">{item.label}</span>
                  {badge && badge > 0 && (
                    <span className="w-5 h-5 rounded-full bg-red-100 text-red-600 text-[10px] font-semibold flex items-center justify-center">
                      {badge > 9 ? '9+' : badge}
                    </span>
                  )}
                </>
              )}

              {sidebarCollapsed && badge && badge > 0 && (
                <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500" />
              )}
            </Link>
          )
        })}
      </nav>

      {/* Settings at bottom */}
      <div className="px-2 py-3 border-t border-[#E5E7EB]">
        <Link
          href="/dashboard"
          className={cn(
            'flex items-center gap-3 px-2 py-2 rounded-md text-sm font-medium text-[#374151] hover:bg-[#F9FAFB] transition-colors',
            sidebarCollapsed && 'justify-center'
          )}
        >
          <Settings className="w-4 h-4 text-[#9CA3AF] flex-shrink-0" />
          {!sidebarCollapsed && <span>Settings</span>}
        </Link>
      </div>
    </aside>
  )
}
