import { AppLayout } from '@/components/layout/AppLayout'
import { DashboardView } from '@/features/telemetry/DashboardView'

export const metadata = { title: 'Dashboard' }

export default function DashboardPage() {
  return (
    <AppLayout>
      <DashboardView />
    </AppLayout>
  )
}
