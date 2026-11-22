import { useCallback, useEffect, useState } from 'react'
import { requestConfusionMatrix } from '../lib/confusionMatrix'
import type { ConfusionMatrix, Phase } from '../types'

type Result = {
  endpoint: string
  key: number
  data: ConfusionMatrix | null
  error: string
}

export function useConfusionMatrix(endpoint: string) {
  const [reloadKey, setReloadKey] = useState(0)
  const [result, setResult] = useState<Result | null>(null)

  const reload = useCallback(() => setReloadKey((key) => key + 1), [])

  useEffect(() => {
    const controller = new AbortController()
    const key = reloadKey

    requestConfusionMatrix(endpoint, controller.signal)
      .then((data) => setResult({ endpoint, key, data, error: '' }))
      .catch((caught: unknown) => {
        if (controller.signal.aborted) return
        setResult({
          endpoint,
          key,
          data: null,
          error: caught instanceof Error ? caught.message : 'Unable to reach the model API.',
        })
      })

    return () => controller.abort()
  }, [endpoint, reloadKey])

  const current =
    result && result.endpoint === endpoint && result.key === reloadKey ? result : null
  const phase: Phase = current ? (current.data ? 'done' : 'error') : 'loading'

  return {
    phase,
    matrix: current?.data ?? null,
    error: current?.error ?? '',
    reload,
    endpoint,
  }
}
