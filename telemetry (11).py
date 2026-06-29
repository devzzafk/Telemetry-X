'use client'

import { useState, useRef, useCallback } from 'react'
import {
  Play, Pause, SkipBack, SkipForward,
  Square, ChevronDown, FastForward,
} from 'lucide-react'
import { useReplayStore } from '@/store'
import { formatDuration, cn } from '@/utils'

const SPEED_OPTIONS = [0.25, 0.5, 1, 2, 4]

export function ReplayTimeline() {
  const { status, currentTime, speed, session, setStatus, setCurrentTime, setSpeed, reset } =
    useReplayStore()

  const [isDragging, setIsDragging] = useState(false)
  const trackRef = useRef<HTMLDivElement>(null)
  const isReplaying = status !== 'idle'
  const duration = session?.duration ?? 300 // Demo: 5 min

  const progress = Math.min((currentTime / duration) * 100, 100)

  const handleTrackClick = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (!trackRef.current) return
      const rect = trackRef.current.getBoundingClientRect()
      const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
      setCurrentTime(ratio * duration)
    },
    [duration, setCurrentTime]
  )

  return (
    <div className="h-[80px] border-t border-[#E5E7EB] bg-white flex items-center px-4 gap-4 flex-shrink-0">
      {/* Controls */}
      <div className="flex items-center gap-1.5">
        <button
          onClick={reset}
          className="w-7 h-7 rounded-md hover:bg-[#F3F4F6] flex items-center justify-center text-[#6B7280] transition-colors"
          title="Reset"
        >
          <Square className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => setCurrentTime(Math.max(0, currentTime - 5))}
          className="w-7 h-7 rounded-md hover:bg-[#F3F4F6] flex items-center justify-center text-[#6B7280] transition-colors"
          title="Skip back 5s"
        >
          <SkipBack className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => setStatus(status === 'playing' ? 'paused' : 'playing')}
          className={cn(
            'w-8 h-8 rounded-md flex items-center justify-center transition-colors',
            status === 'playing'
              ? 'bg-[#111827] text-white hover:bg-[#374151]'
              : 'bg-[#2563EB] text-white hover:bg-[#1D4ED8]'
          )}
        >
          {status === 'playing' ? (
            <Pause className="w-4 h-4" />
          ) : (
            <Play className="w-4 h-4 ml-0.5" />
          )}
        </button>
        <button
          onClick={() => setCurrentTime(Math.min(duration, currentTime + 5))}
          className="w-7 h-7 rounded-md hover:bg-[#F3F4F6] flex items-center justify-center text-[#6B7280] transition-colors"
          title="Skip forward 5s"
        >
          <SkipForward className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Time display */}
      <div className="flex items-center gap-1 text-xs font-mono text-[#374151] flex-shrink-0">
        <span className="font-semibold">{formatDuration(currentTime)}</span>
        <span className="text-[#9CA3AF]">/</span>
        <span className="text-[#9CA3AF]">{formatDuration(duration)}</span>
      </div>

      {/* Track */}
      <div className="flex-1 relative">
        <div
          ref={trackRef}
          onClick={handleTrackClick}
          className="w-full h-2 bg-[#F3F4F6] rounded-full cursor-pointer group"
        >
          {/* Filled portion */}
          <div
            className="h-full bg-[#2563EB] rounded-full relative transition-all duration-100"
            style={{ width: `${progress}%` }}
          >
            {/* Scrubber handle */}
            <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1/2 w-3.5 h-3.5 bg-white border-2 border-[#2563EB] rounded-full shadow-sm opacity-0 group-hover:opacity-100 transition-opacity" />
          </div>

          {/* Crash marker */}
          {session?.crashAt && (
            <div
              className="absolute top-1/2 -translate-y-1/2 w-1 h-4 bg-red-500 rounded-full"
              style={{
                left: `${((new Date(session.crashAt).getTime() - new Date(session.startTime).getTime()) / 1000 / duration) * 100}%`,
              }}
              title="Crash detected here"
            />
          )}
        </div>

        {/* Track labels */}
        <div className="flex justify-between mt-0.5">
          <span className="text-[9px] text-[#9CA3AF]">Start</span>
          <span className="text-[9px] text-[#9CA3AF]">End</span>
        </div>
      </div>

      {/* Speed control */}
      <div className="flex items-center gap-1.5 flex-shrink-0">
        <FastForward className="w-3.5 h-3.5 text-[#9CA3AF]" />
        <div className="flex gap-0.5">
          {SPEED_OPTIONS.map((s) => (
            <button
              key={s}
              onClick={() => setSpeed(s)}
              className={cn(
                'h-6 px-1.5 rounded text-[10px] font-medium transition-colors',
                speed === s
                  ? 'bg-[#111827] text-white'
                  : 'text-[#6B7280] hover:bg-[#F3F4F6]'
              )}
            >
              {s}×
            </button>
          ))}
        </div>
      </div>

      {/* Status */}
      <div className="flex-shrink-0">
        <span
          className={cn(
            'text-[10px] font-semibold uppercase tracking-wider',
            status === 'playing' ? 'text-[#2563EB]' :
            status === 'paused' ? 'text-orange-600' :
            'text-[#9CA3AF]'
          )}
        >
          {status === 'idle' ? 'Live' : status}
        </span>
      </div>
    </div>
  )
}
