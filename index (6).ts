import { AppLayout } from '@/components/layout/AppLayout'
import { DevicesView } from '@/features/devices/DevicesView'

export const metadata = { title: 'Devices' }

export default function DevicesPage() {
  return (
    <AppLayout>
      <DevicesView />
    </AppLayout>
  )
}
