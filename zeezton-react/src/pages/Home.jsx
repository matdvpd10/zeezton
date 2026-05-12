import { Link } from 'react-router-dom'

function Home() {
  return (
    <section className="hero-zeezton">
      <div className="container">
        <span className="hero-badge">Repuestos BMW Premium</span>

        <h1 className="hero-title">
          Zeezton Store
        </h1>

        <p className="hero-text">
          Repuestos, accesorios y estilo exclusivo para tu BMW.
        </p>

        <div className="d-flex gap-3 mt-4">
             <Link to="/productos" className="btn btn-light fw-bold">
            Ver productos
        </Link>

         <Link to="/contacto" className="btn btn-outline-light">
             Contactar
        </Link>
        </div>
      </div>
    </section>
  )
}

export default Home