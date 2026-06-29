import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'
import { Toaster } from '@/components/ui/toaster'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export const metadata: Metadata = {
  title: {
    default: 'Telemetry-X — Mission Control for Modern Software',
    template: '%s | Telemetry-X',
  },
  description:
    "Don't read logs. Watch your system. Telemetry-X is an interactive telemetry visualization platform for backend developers, IoT engineers, and distributed systems teams.",
  keywords: ['telemetry', 'monitoring', 'observability', 'IoT', 'distributed systems', 'real-time', 'visualization'],
  authors: [{ name: 'Telemetry-X' }],
  openGraph: {
    title: 'Telemetry-X — Mission Control for Modern Software',
    description: "Don't read logs. Watch your system.",
    type: 'website',
  },
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#FAFAFA' },
    { media: '(prefers-color-scheme: dark)', color: '#0A0A0F' },
  ],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body className={`${inter.variable} font-sans antialiased`}>
        <Providers>
          {children}
          <Toaster />
        </Providers>
      </body>
    </html>
  )
}
