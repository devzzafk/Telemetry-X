'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { ArrowRight, Activity, History, Eye, Zap, Server, Cpu, MemoryStick, Wifi } from 'lucide-react'
import { cn } from '@/utils'

// ─── Mini demo node ───────────────────────────────────────────────────────────

function DemoNode({
  label, type, cpu, latency, status = 'online', delay = 0
}: {
  label: string; type: string; cpu: number; latency: number
  status?: 'online' | 'warning' | 'error'; delay?: number
}) {
  const [animCpu, setAnimCpu] = useState(cpu)

  useEffect(() => {
    const id = setInterval(() => {
      setAnimCpu((v) => Math.max(0, Math.min(100, v + (Math.random() - 0.5) * 10)))
    }, 1200 + delay)
    return () => clearInterval(id)
  }, [delay])

  const statusColor = status === 'online' ? '#16A34A' : status === 'warning' ? '#D97706' : '#DC2626'
  const barColor = animCpu > 80 ? '#DC2626' : animCpu > 60 ? '#D97706' : '#2563EB'

  return (
    <div className="bg-white border border-[#E5E7EB] rounded-xl p-3 min-w-[160px] shadow-sm">
      <div className="flex items-center gap-2 mb-2.5">
        <div className="w-6 h-6 bg-blue-50 rounded-md flex items-center justify-center">
          <Server className="w-3.5 h-3.5 text-[#2563EB]" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-[11px] font-semibold text-[#111827] truncate">{label}</div>
          <div className="text-[9px] text-[#9CA3AF]">{type}</div>
        </div>
        <div className="w-1.5 h-1.5 rounded-full" style={{ background: statusColor }} />
      </div>
      <div className="space-y-1.5">
        <div>
          <div className="flex justify-between mb-0.5">
            <span className="text-[9px] text-[#9CA3AF]">CPU</span>
            <span className="text-[9px] font-medium text-[#374151] font-mono">{animCpu.toFixed(0)}%</span>
          </div>
          <div className="h-1 bg-[#F3F4F6] rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-700"
              style={{ width: `${animCpu}%`, background: barColor }}
            />
          </div>
        </div>
        <div className="flex gap-3">
          <div>
            <div className="text-[9px] text-[#9CA3AF]">Latency</div>
            <div className="text-[10px] font-semibold text-[#374151] font-mono">{latency}ms</div>
          </div>
        </div>
      </div>
    </div>
  )
}

function DemoEdge() {
  return (
    <div className="flex items-center">
      <div className="w-12 h-px bg-[#E5E7EB] relative overflow-visible">
        <div
          className="absolute top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full bg-[#2563EB] opacity-80"
          style={{ animation: 'slideRight 1.8s linear infinite' }}
        />
      </div>
      <style>{`
        @keyframes slideRight {
          0% { left: -6px; opacity: 0 }
          10% { opacity: 1 }
          90% { opacity: 1 }
          100% { left: 100%; opacity: 0 }
        }
      `}</style>
    </div>
  )
}

// ─── Live demo preview ────────────────────────────────────────────────────────

function LiveDemoPreview() {
  const [logLines, setLogLines] = useState([
    { id: 1, level: 'info', msg: 'Gateway connected — 14 clients', node: 'gateway' },
    { id: 2, level: 'debug', msg: 'Cache hit for session:abc123', node: 'redis' },
    { id: 3, level: 'warning', msg: 'Memory at 78% — watching', node: 'backend' },
  ])

  useEffect(() => {
    const msgs = [
      { level: 'info', msg: 'Packet received from ESP32 [device-001]', node: 'gateway' },
      { level: 'debug', msg: 'DB query: SELECT metrics LIMIT 100', node: 'postgres' },
      { level: 'info', msg: 'Request processed in 38ms', node: 'backend' },
      { level: 'warning', msg: 'CPU spike detected: 84%', node: 'backend' },
      { level: 'info', msg: 'WebSocket frame sent to 128 clients', node: 'frontend' },
      { level: 'debug', msg: 'Heartbeat OK — uptime 7d 4h', node: 'esp32' },
    ]
    let i = 0
    const id = setInterval(() => {
      const m = msgs[i % msgs.length]
      setLogLines((prev) => [{ id: Date.now(), ...m }, ...prev].slice(0, 6))
      i++
    }, 1400)
    return () => clearInterval(id)
  }, [])

  const levelColor: Record<string, string> = {
    info: 'text-[#2563EB]',
    warning: 'text-[#D97706]',
    error: 'text-[#DC2626]',
    debug: 'text-[#9CA3AF]',
  }
  const levelLabel: Record<string, string> = {
    info: 'INF', warning: 'WRN', error: 'ERR', debug: 'DBG',
  }

  return (
    <div className="bg-white border border-[#E5E7EB] rounded-2xl overflow-hidden shadow-lg">
      {/* Fake topbar */}
      <div className="h-10 bg-white border-b border-[#E5E7EB] flex items-center px-4 gap-3">
        <div className="w-4 h-4 rounded bg-[#2563EB] flex items-center justify-center">
          <div className="w-2 h-2 rounded-full border border-white" />
        </div>
        <span className="text-xs font-semibold text-[#111827]">Telemetry-X</span>
        <span className="ml-2 text-[10px] px-2 py-0.5 bg-green-50 text-green-700 rounded-full font-medium">● Live</span>
      </div>

      {/* Graph area */}
      <div className="bg-[#FAFAFA] p-6">
        <div className="flex items-center gap-0">
          <DemoNode label="ESP32 Sensor" type="IoT Device" cpu={18} latency={9} delay={0} />
          <DemoEdge />
          <DemoNode label="API Gateway" type="Gateway" cpu={35} latency={22} delay={200} />
          <DemoEdge />
          <DemoNode label="FastAPI" type="Backend" cpu={52} latency={44} delay={400} />
          <DemoEdge />
          <DemoNode label="PostgreSQL" type="Database" cpu={14} latency={11} delay={600} />
        </div>
      </div>

      {/* Log panel */}
      <div className="border-t border-[#E5E7EB]">
        <div className="flex items-center gap-2 px-3 py-1.5 border-b border-[#F3F4F6]">
          <span className="text-[10px] font-semibold text-[#374151]">Live Logs</span>
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
        </div>
        <div className="font-mono text-[10px] px-3 py-2 space-y-1 h-[110px] overflow-hidden">
          {logLines.map((line, i) => (
            <div
              key={line.id}
              className="flex items-start gap-2 transition-opacity"
              style={{ opacity: Math.max(0.3, 1 - i * 0.15) }}
            >
              <span className="text-[#9CA3AF] flex-shrink-0">
                {new Date().toTimeString().slice(0, 8)}
              </span>
              <span className={cn('font-bold flex-shrink-0', levelColor[line.level])}>
                {levelLabel[line.level]}
              </span>
              <span className="text-[#9CA3AF] flex-shrink-0">{line.node}</span>
              <span className="text-[#374151]">{line.msg}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Timeline */}
      <div className="h-10 border-t border-[#E5E7EB] flex items-center px-3 gap-3 bg-white">
        <div className="w-5 h-5 rounded bg-[#2563EB] flex items-center justify-center">
          <div className="w-0 h-0 border-l-[5px] border-l-white border-t-[4px] border-t-transparent border-b-[4px] border-b-transparent ml-0.5" />
        </div>
        <div className="flex-1 h-1.5 bg-[#F3F4F6] rounded-full overflow-hidden">
          <div className="h-full w-[60%] bg-[#2563EB] rounded-full" />
        </div>
        <span className="text-[10px] font-mono text-[#6B7280]">2:58 / 5:00</span>
        <span className="text-[10px] font-semibold text-[#2563EB]">LIVE</span>
      </div>
    </div>
  )
}

// ─── Feature card ─────────────────────────────────────────────────────────────

function FeatureCard({ icon: Icon, title, description }: {
  icon: React.ElementType; title: string; description: string
}) {
  return (
    <div className="bg-white border border-[#E5E7EB] rounded-xl p-5 hover:border-[#D1D5DB] hover:shadow-sm transition-all">
      <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center mb-3">
        <Icon className="w-4 h-4 text-[#2563EB]" />
      </div>
      <h3 className="text-sm font-semibold text-[#111827] mb-1.5">{title}</h3>
      <p className="text-sm text-[#6B7280] leading-relaxed">{description}</p>
    </div>
  )
}

// ─── Main landing page ────────────────────────────────────────────────────────

export function LandingPage() {
  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      {/* Nav */}
      <nav className="h-14 border-b border-[#E5E7EB] bg-white/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto h-full flex items-center px-6 gap-6">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-[#2563EB] rounded flex items-center justify-center">
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <circle cx="6" cy="6" r="4" stroke="white" strokeWidth="1.5" />
                <circle cx="6" cy="6" r="1.5" fill="white" />
              </svg>
            </div>
            <span className="font-semibold text-sm text-[#111827]">Telemetry-X</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-[#6B7280] ml-4">
            <a href="#features" className="hover:text-[#111827] transition-colors">Features</a>
            <a href="#sdk" className="hover:text-[#111827] transition-colors">SDK</a>
            <a href="#" className="hover:text-[#111827] transition-colors">Docs</a>
          </div>
          <div className="ml-auto flex items-center gap-3">
            <Link href="/dashboard" className="text-sm text-[#374151] hover:text-[#111827] transition-colors">
              Sign in
            </Link>
            <Link
              href="/dashboard"
              className="h-8 px-4 bg-[#111827] text-white text-sm font-medium rounded-lg hover:bg-[#374151] transition-colors flex items-center"
            >
              Start free
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 text-xs font-medium text-[#2563EB] bg-blue-50 border border-blue-100 px-3 py-1.5 rounded-full mb-6">
          <span className="w-1.5 h-1.5 bg-[#2563EB] rounded-full" />
          Now in beta — connect your first node in 60 seconds
        </div>

        <h1 className="text-5xl font-bold text-[#111827] leading-tight tracking-tight mb-4 max-w-3xl mx-auto">
          Don't read logs.
          <br />
          <span className="text-[#2563EB]">Watch your system.</span>
        </h1>

        <p className="text-lg text-[#6B7280] max-w-xl mx-auto mb-8 leading-relaxed">
          Telemetry-X turns your system's events into a live, interactive graph.
          Monitor, replay, and debug without ever scrolling through a terminal.
        </p>

        <div className="flex items-center justify-center gap-3 mb-16">
          <Link
            href="/dashboard"
            className="h-10 px-5 bg-[#2563EB] text-white text-sm font-medium rounded-lg hover:bg-[#1D4ED8] transition-colors flex items-center gap-2"
          >
            Start monitoring
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/dashboard"
            className="h-10 px-5 bg-white border border-[#E5E7EB] text-[#374151] text-sm font-medium rounded-lg hover:bg-[#F9FAFB] transition-colors flex items-center gap-2"
          >
            Live demo
          </Link>
        </div>

        {/* Interactive demo */}
        <LiveDemoPreview />
      </section>

      {/* Features */}
      <section id="features" className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-2xl font-bold text-[#111827] mb-3">
            Everything your team needs
          </h2>
          <p className="text-[#6B7280] max-w-lg mx-auto">
            From ESP32 sensors to distributed microservices — Telemetry-X connects your entire stack in one view.
          </p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
          <FeatureCard
            icon={Eye}
            title="Live Graph"
            description="Every node and connection is visualized in real time. Watch data flow between services as it happens."
          />
          <FeatureCard
            icon={History}
            title="Replay Timeline"
            description="Every event is recorded. Drag back in time to inspect exactly what happened before a crash."
          />
          <FeatureCard
            icon={Activity}
            title="Node Inspector"
            description="Click any node to see CPU, memory, latency, packet rate, temperature, errors, and custom metrics."
          />
          <FeatureCard
            icon={Zap}
            title="Crash Detection"
            description="When a node goes offline, Telemetry-X automatically jumps to 5 seconds before the event."
          />
          <FeatureCard
            icon={Cpu}
            title="Live Metrics"
            description="Real-time charts for CPU, memory, latency, network throughput, and more across all nodes."
          />
          <FeatureCard
            icon={Wifi}
            title="SDK"
            description="Two lines of Python or Node.js — telemetry.connect() and telemetry.send(). That's it."
          />
        </div>
      </section>

      {/* SDK section */}
      <section id="sdk" className="max-w-6xl mx-auto px-6 py-20 border-t border-[#E5E7EB]">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-2xl font-bold text-[#111827] mb-4">
              Two lines of code
            </h2>
            <p className="text-[#6B7280] mb-6 leading-relaxed">
              Drop the SDK into your existing project. No agents, no sidecars, no YAML.
              Telemetry-X handles everything automatically.
            </p>
            <ul className="space-y-3">
              {[
                'Automatic metric collection',
                'WebSocket streaming built-in',
                'Works on ESP32, Raspberry Pi, servers',
                'Custom metric support',
              ].map((item) => (
                <li key={item} className="flex items-center gap-2 text-sm text-[#374151]">
                  <div className="w-4 h-4 bg-green-50 rounded-full flex items-center justify-center flex-shrink-0">
                    <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
                  </div>
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div className="space-y-3">
            {/* Python snippet */}
            <div className="bg-[#111827] rounded-xl overflow-hidden">
              <div className="flex items-center gap-2 px-4 py-2.5 border-b border-white/10">
                <span className="text-xs text-white/40 font-medium">Python</span>
              </div>
              <pre className="px-4 py-4 text-sm font-mono text-white/90 overflow-x-auto leading-relaxed"><code>{`from telemetry_x import TelemetryClient

t = TelemetryClient(
    project_id="my-project",
    node_id="backend-api"
)

t.connect()
t.send("request.processed", { "latency": 42 })`}</code></pre>
            </div>
            {/* Node snippet */}
            <div className="bg-[#111827] rounded-xl overflow-hidden">
              <div className="flex items-center gap-2 px-4 py-2.5 border-b border-white/10">
                <span className="text-xs text-white/40 font-medium">Node.js</span>
              </div>
              <pre className="px-4 py-4 text-sm font-mono text-white/90 overflow-x-auto leading-relaxed"><code>{`import { TelemetryClient } from 'telemetry-x'

const t = new TelemetryClient({
  projectId: 'my-project',
  nodeId: 'api-gateway',
})

await t.connect()
t.send('request.processed', { latency: 42 })`}</code></pre>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-[#E5E7EB] bg-white">
        <div className="max-w-6xl mx-auto px-6 py-20 text-center">
          <h2 className="text-2xl font-bold text-[#111827] mb-3">
            Start watching your systems
          </h2>
          <p className="text-[#6B7280] mb-8">
            Free during beta. No credit card required.
          </p>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 h-10 px-6 bg-[#2563EB] text-white text-sm font-medium rounded-lg hover:bg-[#1D4ED8] transition-colors"
          >
            Open dashboard
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#E5E7EB] bg-[#FAFAFA]">
        <div className="max-w-6xl mx-auto px-6 py-8 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 bg-[#2563EB] rounded flex items-center justify-center">
              <div className="w-2.5 h-2.5 rounded-full border border-white" />
            </div>
            <span className="text-sm font-semibold text-[#374151]">Telemetry-X</span>
          </div>
          <span className="text-xs text-[#9CA3AF]">© 2024 Telemetry-X. Mission Control for Modern Software.</span>
        </div>
      </footer>
    </div>
  )
}
