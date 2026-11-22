import { Fragment, useEffect, useRef, useState, type CSSProperties } from 'react'
import type { CorrelationMatrix } from '../../types'
import './CorrelationMatrixChart.css'

type ActiveCell = {
  row: number
  column: number
  value: number
}

const LABEL_WIDTH = 68

function cellColor(value: number): string {
  const opacity = 0.08 + Math.min(Math.abs(value), 1) * 0.86
  return value >= 0
    ? `rgba(239, 59, 44, ${opacity})`
    : `rgba(59, 125, 216, ${opacity})`
}

function formatValue(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(3)}`
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
  data: CorrelationMatrix
}

export function CorrelationMatrixChart({ data }: Props) {
  const { ref, width } = useContainerWidth()
  const [active, setActive] = useState<ActiveCell | null>(null)
  const { labels, matrix, target } = data
  const targetIndex = labels.indexOf(target)

  const cellWidth = width > 0 ? (width - LABEL_WIDTH) / labels.length : 0
  const gridStyle = {
    '--corr-size': labels.length,
    '--corr-label-width': `${LABEL_WIDTH}px`,
  } as CSSProperties

  return (
    <div className="corr-chart" ref={ref}>
      <div className="corr-readout" aria-live="polite">
        <span>{active ? 'CELL INSPECTOR' : `PEARSON r · ${labels.length} × ${labels.length}`}</span>
        <strong>
          {active
            ? `${labels[active.row]} × ${labels[active.column]}`
            : 'Hover a cell to inspect its correlation'}
        </strong>
        {active && (
          <b className={active.value >= 0 ? 'is-positive' : 'is-negative'}>
            {formatValue(active.value)}
          </b>
        )}
      </div>

      <div className="corr-grid-scroll">
        <div className="corr-grid" style={gridStyle}>
          <div className="corr-corner">FEATURE</div>
          {labels.map((label, index) => (
            <div
              className={`corr-col-label ${index === targetIndex ? 'is-target' : ''}`}
              key={`col-${label}-${index}`}
            >
              <span>{label}</span>
            </div>
          ))}

          {matrix.map((row, rowIndex) => (
            <Fragment key={`row-${labels[rowIndex]}-${rowIndex}`}>
              <div
                className={`corr-row-label ${rowIndex === targetIndex ? 'is-target' : ''}`}
              >
                {labels[rowIndex]}
              </div>
              {row.map((value, columnIndex) => {
                const highlighted =
                  rowIndex === targetIndex || columnIndex === targetIndex
                return (
                  <div
                    className={`corr-cell ${highlighted ? 'is-target' : ''}`}
                    key={`cell-${rowIndex}-${columnIndex}`}
                    style={{ backgroundColor: cellColor(value) }}
                    onMouseEnter={() =>
                      setActive({ row: rowIndex, column: columnIndex, value })
                    }
                    onMouseLeave={() => setActive(null)}
                    onFocus={() => setActive({ row: rowIndex, column: columnIndex, value })}
                    onBlur={() => setActive(null)}
                    tabIndex={0}
                    role="img"
                    aria-label={`${labels[rowIndex]} and ${labels[columnIndex]}: Pearson r ${formatValue(value)}`}
                  >
                    <span className={Math.abs(value) >= 0.6 ? 'is-strong' : ''}>
                      {cellWidth >= 34 ? value.toFixed(2) : value.toFixed(1)}
                    </span>
                  </div>
                )
              })}
            </Fragment>
          ))}
        </div>
      </div>

      <div className="corr-legend">
        <span>-1.0</span>
        <div className="corr-scale" aria-hidden="true" />
        <span>+1.0</span>
        <small>NEGATIVE · 0 · POSITIVE</small>
      </div>
    </div>
  )
}
