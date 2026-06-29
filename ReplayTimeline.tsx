import { AppLayout } from '@/components/layout/AppLayout'
import { AlertsView } from '@/features/alerts/AlertsView'

export const metadata = { title: 'Alerts' }

export default function AlertsPage() {
  return (
    <AppLayout>
      <AlertsView />
    </AppLayout>
  )
}
