import type { FeatureSelection } from '../../types'
import './TargetLinks.css'

type Props = {
  data: FeatureSelection
}

export function TargetLinks({ data }: Props) {
  const maxScore = Math.max(...data.features.map((feature) => feature.anova_f))

  return (
    <div className="target-links-body">
      <p className="target-links-lede">
        The <strong>{data.k}</strong> variables kept by SelectKBest out of {data.total_features},
        ranked by ANOVA F against <strong>{data.target}</strong>. Bars scale to the strongest score;
        mutual information (MI) also picks up non-linear links.
      </p>

      <div className="target-links-head">
        <span>RANK</span>
        <span>FEATURE</span>
        <span>ANOVA F</span>
        <span>SCORE</span>
        <span>MI</span>
      </div>

      <div className="target-links-list">
        {data.features.map((feature) => (
          <div className="target-links-row" key={feature.name}>
            <span className="target-links-index">{String(feature.rank).padStart(2, '0')}</span>
            <span className="target-links-name">{feature.name}</span>
            <div className="target-links-track" aria-hidden="true">
              <span
                style={{ width: `${maxScore > 0 ? (feature.anova_f / maxScore) * 100 : 0}%` }}
              />
            </div>
            <strong>{feature.anova_f.toFixed(1)}</strong>
            <span className="target-links-mi">{feature.mutual_information.toFixed(3)}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
