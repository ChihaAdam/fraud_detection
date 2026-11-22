import { NavLink } from 'react-router-dom'
import type { StatusTone } from '../types'
import './TopBar.css'

type Props = {
  statusText: string
  statusTone: StatusTone
}

export function TopBar({ statusText, statusTone }: Props) {
  return (
    <header className="topbar">
      <div className="brand">
        <span className="brand-mark" aria-hidden="true">R</span>
        <span className="brand-name">REDLINE</span>
        <span className="brand-divider" aria-hidden="true" />
        <span className="brand-sub">FRAUD SIGNAL DESK</span>
      </div>

      <nav className="route-nav" aria-label="Main navigation">
        <NavLink to="/" end className={({ isActive }) => `route-link ${isActive ? 'active' : ''}`}>
          <span className="route-index">01</span> PREDICTION
        </NavLink>
        <NavLink to="/visualisation" className={({ isActive }) => `route-link ${isActive ? 'active' : ''}`}>
          <span className="route-index">02</span> VISUALISATION
        </NavLink>
      </nav>

      <div className="topbar-right">
        <span className="build-tag">SVM / BINARY CLASSIFIER</span>
        <span className={`link-status ${statusTone}`}>
          <span className="status-dot" aria-hidden="true" />
          {statusText}
        </span>
      </div>
    </header>
  )
}
