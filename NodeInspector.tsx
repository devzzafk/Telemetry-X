import { AppLayout } from '@/components/layout/AppLayout'
import { ReplayView } from '@/features/replay/ReplayView'

export const metadata = { title: 'Replay' }

export default function ReplayPage() {
  return (
    <AppLayout>
      <ReplayView />
    </AppLayout>
  )
}
