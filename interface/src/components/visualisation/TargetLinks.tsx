import type { CorrelationMatrix } from '../../types'
import './TargetLinks.css'

const MAX_ENTRIES = 8

function formatValue(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(3)}`
}

type Props = {
  data: CorrelationMatrix
}

export function TargetLinks({ data }: Props) {
  const ranked = Object.entries(data.target_correlations)
    .filter(([name]) => name !== data.target)
    .sort((first, second) => Math.abs(second[1]) - Math.abs(first[1]))
    .slice(0, MAX_ENTRIES)

  return (
    <div className="target-links-body">
      <p className="target-links-lede">
        Strongest linear relationships with <strong>{data.target}</strong>, ranked by absolute
        Pearson r. Bars run from the centre outward: red for positive, blue for negative.
      </p>

      <div className="target-links-head">
        <span>FEATURE</span>
        <span>r</span>
      </div>

      <div className="target-links-list">
        {ranked.map(([name, value], index) => (
          <div className="target-links-row" key={name}>
            <span className="target-links-index">{String(index + 1).padStart(2, '0')}</span>
            <span className="target-links-name">{name}</span>
            <div className="target-links-track">
              <span
                className={value >= 0 ? 'is-positive' : 'is-negative'}
                style={{ width: `${Math.min(Math.abs(value), 1) * 50}%` }}
              />
            </div>
            <strong className={value >= 0 ? 'is-positive' : 'is-negative'}>
              {formatValue(value)}
            </strong>
          </div>
        ))}
      </div>
    </div>
  )
}
