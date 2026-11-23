export type Phase = 'idle' | 'loading' | 'done' | 'error'

export type StatusTone = 'idle' | 'busy' | 'up' | 'down'

export type Verdict = {
  prediction: number
  label: string
  latency: number
  features: number[]
}

export type PreviewValue = number | null

export type ConfusionMatrix = {
  dataset: string
  split: string
  rows: string
  columns: string
  labels: string[]
  matrix: number[][]
  values: {
    true_negative: number
    false_positive: number
    false_negative: number
    true_positive: number
  }
}

export type CorrelationMatrix = {
  dataset: string
  method: string
  target: string
  labels: string[]
  matrix: number[][]
  target_correlations: Record<string, number>
}

export type FeatureScore = {
  name: string
  anova_f: number
  mutual_information: number
  rank: number
}

export type FeatureSelection = {
  dataset: string
  target: string
  method: string
  selector: string
  k: number
  total_features: number
  features: FeatureScore[]
}
