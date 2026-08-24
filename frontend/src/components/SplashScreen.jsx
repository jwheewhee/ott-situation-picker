import { useEffect } from 'react'
import { PopcornMascot } from './Mascots'

const SPLASH_DURATION_MS = 1800

function SplashScreen({ onFinish }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onFinish?.()
    }, SPLASH_DURATION_MS)
    return () => clearTimeout(timer)
  }, [onFinish])

  return (
    <div className="splash-screen">
      <div className="splash-backdrop">
        <div className="splash-flash" />
        <div className="splash-mascot-wrap">
          <PopcornMascot size={420} />
          <span className="splash-ripple" />
        </div>
      </div>
      <h1 className="splash-logo">FlixFit</h1>
    </div>
  )
}

export default SplashScreen
