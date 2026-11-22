import type { ReactNode } from 'react'
import './Intro.css'

export type IntroStat = {
  value: string
  label: string
}

type Props = {
  eyebrow?: string
  title?: ReactNode
  lede?: string
  stats?: IntroStat[]
}

export function Intro({
  eyebrow = 'TRANSACTION INTELLIGENCE / 001',
  title = (
    <>
      Read the signal.<br /><em>Call the fraud.</em>
    </>
  ),
  lede = 'Feed the classifier thirty transaction parameters in their exact model order. The decision comes straight from the deployed model — no smoothing, no guesswork.',
  stats = [
    { value: '30', label: 'INPUT VALUES' },
    { value: 'SVM', label: 'ENGINE' },
    { value: '0 / 1', label: 'OUTPUT CLASS' },
  ],
}: Props) {
  return (
    <section className="intro">
      <div className="intro-copy">
        <p className="eyebrow"><span className="eyebrow-line" />{eyebrow}</p>
        <h1>{title}</h1>
        <p className="lede">{lede}</p>
      </div>
      <div className="intro-stats" aria-label="Model interface facts">
        {stats.map((stat) => (
          <div className="intro-stat" key={stat.label}>
            <strong>{stat.value}</strong>
            <span>{stat.label}</span>
          </div>
        ))}
      </div>
    </section>
  )
}
