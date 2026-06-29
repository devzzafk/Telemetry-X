'use client'

import { Topbar } from './Topbar'
import { Sidebar } from './Sidebar'
import { useMockTelemetry } from '@/hooks/useMockTelemetry'
import { useAppSettingsStore } from '@/store'
import { cn } from '@/utils'

interface AppLayoutProps {
  children: React.ReactNode
}

export function AppLayout({ children }: AppLayoutProps) {
  useMockTelemetry(true)
  const { sidebarCollapsed } = useAppSettingsStore()

  return (
    <div className="flex h-screen overflow-hidden bg-[#FAFAFA]">
      <Sidebar />
      <div
        className={cn(
          'flex flex-col flex-1 min-w-0 transition-all duration-200',
          sidebarCollapsed ? 'ml-14' : 'ml-[220px]'
        )}
      >
        <Topbar />
        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  )
}
