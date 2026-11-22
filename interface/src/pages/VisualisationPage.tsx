import { NavLink, Outlet } from 'react-router-dom'
import { useDetectionContext } from '../hooks/useFraudDetection'
import './VisualisationPage.css'

const tabs = [
  { to: '/visualisation/confusion-matrix', index: '01', label: 'CONFUSION MATRIX' },
  { to: '/visualisation/correlation-matrix', index: '02', label: 'CORRELATION MATRIX' },
  { to: '/visualisation/target-links', index: '03', label: 'TARGET LINKS' },
]

export function VisualisationPage() {
  const detection = useDetectionContext()

  return (
    <>
      <nav className="viz-tabs" aria-label="Visualisation sections">
        {tabs.map((tab) => (
          <NavLink
            key={tab.to}
            to={tab.to}
            className={({ isActive }) => `viz-tab ${isActive ? 'active' : ''}`}
          >
            <span className="viz-tab-index">{tab.index}</span>
            {tab.label}
          </NavLink>
        ))}
      </nav>

      <Outlet context={detection} />
    </>
  )
}
