import { useEffect, useRef, useState } from 'react'
import { Scatter, ScatterChart, Tooltip, XAxis, YAxis, ZAxis } from 'recharts'
import type { ConfusionMatrix } from '../../types'
import './ConfusionMatrixChart.css'

type Cell = {
  x: number
  y: number
  xLabel: string
  yLabel: string
  value: number
  code: string
  label: string
  correct: boolean
}

type CellShapeProps = {
  cx?: number
  cy?: number
  payload?: Cell
  cellSize: number
  maxValue: number
}

type TooltipContentProps = {
  active?: boolean
  payload?: Array<{ payload?: Cell }>
}

// Axis widths are fixed so the plot area stays perfectly square at any size.
const Y_AXIS_WIDTH = 72
const X_AXIS_HEIGHT = 28
const MARGIN = { top: 16, right: 16, bottom: 60, left: 16 }

function MatrixCell({ cx, cy, payload, cellSize, maxValue }: CellShapeProps) {
  if (cx == null || cy == null || !payload) return null

  const ratio = maxValue > 0 ? payload.value / maxValue : 0
  const opacity = 0.12 + ratio * 0.78
  const half = cellSize / 2
  const fill = payload.correct
    ? `rgba(239, 59, 44, ${opacity})`
    : `rgba(150, 141, 138, ${opacity})`
  const textColor = ratio > 0.62 ? '#fff' : 'var(--ink)'

  return (
    <g>
      <rect
        x={cx - half}
        y={cy - half}
        width={cellSize}
        height={cellSize}
        fill={fill}
        stroke={payload.correct ? 'rgba(239, 59, 44, 0.55)' : 'var(--line)'}
        strokeWidth={1}
      />
      <text
        x={cx}
        y={cy - 5}
        fill={textColor}
        fontFamily="var(--mono)"
        fontSize={24}
        fontWeight={700}
        textAnchor="middle"
        dominantBaseline="middle"
      >
        {payload.value.toLocaleString()}
      </text>
      <text
        x={cx}
        y={cy + 17}
        fill={textColor}
        opacity={0.75}
        fontFamily="var(--mono)"
        fontSize={8}
        letterSpacing="0.1em"
        textAnchor="middle"
        dominantBaseline="middle"
      >
        {payload.code}
      </text>
    </g>
  )
}

function MatrixTooltip({ active, payload }: TooltipContentProps) {
  const cell = payload?.[0]?.payload
  if (!active || !cell) return null

  return (
    <div className="cm-tooltip">
      <span>{cell.correct ? 'CORRECT PREDICTION' : 'MISPREDICTION'}</span>
      <strong>{cell.label}</strong>
      <div>
        <em>{cell.yLabel}</em>
        <span aria-hidden="true"> → </span>
        <em>{cell.xLabel}</em>
        <b>{cell.value.toLocaleString()}</b>
      </div>
    </div>
  )
}

function useContainerWidth() {
  const ref = useRef<HTMLDivElement>(null)
  const [width, setWidth] = useState(0)

  useEffect(() => {
    const element = ref.current
    if (!element) return

    const observer = new ResizeObserver((entries) => {
      setWidth(entries[0]?.contentRect.width ?? 0)
    })
    observer.observe(element)
    setWidth(element.getBoundingClientRect().width)

    return () => observer.disconnect()
  }, [])

  return { ref, width }
}

type Props = {
  data: ConfusionMatrix
}

export function ConfusionMatrixChart({ data }: Props) {
  const { ref, width } = useContainerWidth()
  const [normal, fraud] = data.labels
  const [tn, fp] = data.matrix[0]
  const [fn, tp] = data.matrix[1]

  const cells: Cell[] = [
    { x: 0, y: 0, xLabel: normal, yLabel: normal, value: tn, code: 'TN', label: 'True negative', correct: true },
    { x: 1, y: 0, xLabel: fraud, yLabel: normal, value: fp, code: 'FP', label: 'False positive', correct: false },
    { x: 0, y: 1, xLabel: normal, yLabel: fraud, value: fn, code: 'FN', label: 'False negative', correct: false },
    { x: 1, y: 1, xLabel: fraud, yLabel: fraud, value: tp, code: 'TP', label: 'True positive', correct: true },
  ]
  const maxValue = Math.max(...cells.map((cell) => cell.value), 1)

  const size = Math.min(Math.max(width, 280), 440)
  const plotSize = size - MARGIN.left - Y_AXIS_WIDTH - MARGIN.right
  const cellSize = Math.max(48, plotSize / 2 - 12)
  const area = Math.PI * (cellSize / 2) ** 2

  const tickStyle = { fill: 'var(--muted)', fontSize: 10, fontFamily: 'var(--mono)' }

  return (
    <div className="cm-chart" ref={ref}>
      <ScatterChart width={size} height={size} margin={MARGIN}>
        <XAxis
          type="number"
          dataKey="x"
          domain={[-0.5, 1.5]}
          ticks={[0, 1]}
          tickFormatter={(value) => data.labels[Number(value)] ?? ''}
          height={X_AXIS_HEIGHT}
          interval={0}
          axisLine={{ stroke: 'var(--line)' }}
          tickLine={false}
          tick={tickStyle}
        />
        <YAxis
          type="number"
          dataKey="y"
          domain={[-0.5, 1.5]}
          ticks={[0, 1]}
          tickFormatter={(value) => data.labels[Number(value)] ?? ''}
          width={Y_AXIS_WIDTH}
          interval={0}
          reversed
          axisLine={{ stroke: 'var(--line)' }}
          tickLine={false}
          tick={tickStyle}
        />
        <ZAxis range={[area, area]} />
        <Tooltip content={<MatrixTooltip />} cursor={false} />
        <Scatter
          data={cells}
          isAnimationActive={false}
          shape={<MatrixCell cellSize={cellSize} maxValue={maxValue} />}
        />
      </ScatterChart>
      <div className="cm-axis-note cm-axis-note-top">TRUE CLASS ↓</div>
      <div className="cm-axis-note cm-axis-note-bottom">PREDICTED CLASS →</div>
    </div>
  )
}
