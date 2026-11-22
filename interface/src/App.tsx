import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { Footer } from './components/Footer'
import { TopBar } from './components/TopBar'
import { useFraudDetection } from './hooks/useFraudDetection'
import { ConfusionMatrixPage } from './pages/ConfusionMatrixPage'
import { CorrelationMatrixPage } from './pages/CorrelationMatrixPage'
import { PredictPage } from './pages/PredictPage'
import { TargetLinksPage } from './pages/TargetLinksPage'
import { VisualisationPage } from './pages/VisualisationPage'
import './App.css'

function Layout() {
  const detection = useFraudDetection()

  return (
    <div className="shell">
      <TopBar statusText={detection.statusText} statusTone={detection.statusTone} />

      <main className="workspace">
        <Outlet context={detection} />
      </main>

      <Footer endpoint={detection.endpoint} onEndpointChange={detection.changeEndpoint} />
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<PredictPage />} />
        <Route path="visualisation" element={<VisualisationPage />}>
          <Route index element={<Navigate to="confusion-matrix" replace />} />
          <Route path="confusion-matrix" element={<ConfusionMatrixPage />} />
          <Route path="correlation-matrix" element={<CorrelationMatrixPage />} />
          <Route path="target-links" element={<TargetLinksPage />} />
          <Route path="*" element={<Navigate to="confusion-matrix" replace />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
