import { Link, Outlet } from 'react-router-dom'

function Layout() {
  return (
    <>
      <header className="site-header">
        <Link to="/" className="site-logo">
          FlixFit
        </Link>
      </header>
      <Outlet />
    </>
  )
}

export default Layout
