import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-black border-bottom border-secondary sticky-top">
      <div className="container">

        <Link className="navbar-brand fw-bold" to="/">
          ZEEZTON
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarZeezton"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarZeezton">
          <ul className="navbar-nav ms-auto">

            <li className="nav-item">
              <Link className="nav-link active" to="/">
                Inicio
              </Link>
            </li>

            <li className="nav-item">
              <Link className="nav-link" to="/productos">
                Productos
              </Link>
            </li>

            <li className="nav-item">
              <Link className="nav-link" to="/contacto">
                Contacto
              </Link>
            </li>

          </ul>
        </div>

      </div>
    </nav>
  )
}

export default Navbar