import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { obtenerProductos } from '../services/api'

function Productos() {
  const [productos, setProductos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)

  const [buscar, setBuscar] = useState('')
  const [marca, setMarca] = useState('')

  useEffect(() => {
    obtenerProductos()
      .then(data => {
        const productosOrdenados = [...data].sort((a, b) => b.id - a.id)
        setProductos(productosOrdenados)
      })
      .catch(error => setError(error.message))
      .finally(() => setCargando(false))
  }, [])

  const agruparProductos = (lista, cantidad) => {
    const grupos = []

    for (let i = 0; i < lista.length; i += cantidad) {
      grupos.push(lista.slice(i, i + cantidad))
    }

    return grupos
  }

  const productosDestacados = productos.filter(producto => producto.destacado)

  const destacadosDesktop = agruparProductos(productosDestacados, 5)
  const destacadosMobile = agruparProductos(productosDestacados, 2)

  const marcas = [
    ...new Set(
      productos
        .map(producto => producto.marca)
        .filter(Boolean)
    )
  ]

  const productosFiltrados = productos.filter(producto => {
    const nombre = producto.nombre || ''
    const descripcion = producto.descripcion || ''

    const coincideBusqueda =
      nombre.toLowerCase().includes(buscar.toLowerCase()) ||
      descripcion.toLowerCase().includes(buscar.toLowerCase())

    const coincideMarca = marca === '' || producto.marca === marca

    return coincideBusqueda && coincideMarca
  })

  if (cargando) {
    return (
      <div className="container py-5 text-light">
        Cargando productos...
      </div>
    )
  }

  if (error) {
    return (
      <div className="container py-5 text-danger">
        {error}
      </div>
    )
  }

  return (
    <>
      <section className="destacados-section">
        <h2 className="destacados-title">Lo mas destacado 🤖</h2>

        <div className="d-none d-md-block">
          <div
            id="carouselDestacados"
            className="carousel slide"
            data-bs-ride="carousel"
          >
            <div className="carousel-inner">
              {destacadosDesktop.map((grupo, index) => (
                <div
                  className={`carousel-item ${index === 0 ? 'active' : ''}`}
                  key={index}
                >
                  <div className="row g-4 justify-content-center px-4">
                    {grupo.map(producto => (
                      <div
                        className="col-xl-2 col-lg-3 col-md-4 col-6 mb-3 d-flex"
                        key={producto.id}
                      >
                        <Link
                          to={`/productos/${producto.id}`}
                          className="text-decoration-none w-100"
                        >
                          <div className="card-small h-100">
                            {producto.imagen && (
                              <img
                                src={producto.imagen}
                                className="card-img-top3"
                                alt={producto.nombre}
                              />
                            )}

                            <div className="card-body">
                              <h5 className="producto-titulo">
                                {producto.nombre}
                              </h5>

                              <p className="producto-desc">
                                {producto.descripcion || 'Sin descripción disponible'}
                              </p>

                              <div className="producto-precio">
                                <span className="moneda">$</span>
                                {Number(producto.precio).toLocaleString('es-CL')}
                                <span className="moneda"> CLP</span>
                              </div>
                            </div>
                          </div>
                        </Link>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <button
              className="carousel-control-prev"
              type="button"
              data-bs-target="#carouselDestacados"
              data-bs-slide="prev"
            >
              <span className="carousel-control-prev-icon" aria-hidden="true"></span>
              <span className="visually-hidden">Anterior</span>
            </button>

            <button
              className="carousel-control-next"
              type="button"
              data-bs-target="#carouselDestacados"
              data-bs-slide="next"
            >
              <span className="carousel-control-next-icon" aria-hidden="true"></span>
              <span className="visually-hidden">Siguiente</span>
            </button>
          </div>
        </div>

        <div className="d-block d-md-none">
          <div
            id="carouselDestacadosMobile"
            className="carousel slide"
            data-bs-ride="carousel"
            data-bs-touch="true"
          >
            <div className="carousel-inner">
              {destacadosMobile.map((grupo, index) => (
                <div
                  className={`carousel-item ${index === 0 ? 'active' : ''}`}
                  key={index}
                >
                  <div className="row g-2 px-3">
                    {grupo.map(producto => (
                      <div className="col-6" key={producto.id}>
                        <Link
                          to={`/productos/${producto.id}`}
                          className="text-decoration-none"
                        >
                          <div className="card-small h-100">
                            {producto.imagen && (
                              <img
                                src={producto.imagen}
                                className="card-img-top3"
                                alt={producto.nombre}
                              />
                            )}

                            <div className="card-body p-2">
                              <p className="producto-titulo mb-1 destacado-mobile-title">
                                {producto.nombre}
                              </p>

                              <div className="producto-precio destacado-mobile-price">
                                <span className="moneda">$</span>
                                {Number(producto.precio).toLocaleString('es-CL')}
                              </div>
                            </div>
                          </div>
                        </Link>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="filtro-section">
        <div className="filtro-box">
          <input
            type="text"
            placeholder="Buscar producto..."
            value={buscar}
            onChange={e => setBuscar(e.target.value)}
          />

          <select
            value={marca}
            onChange={e => setMarca(e.target.value)}
          >
            <option value="">Filtrar por marca</option>
            {marcas.map(m => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>

          <button type="button">
            🔍 Buscar
          </button>
        </div>
      </section>

      <main className="productos-page">
        <div className="container py-5">
          <div className="row g-4">
            {productosFiltrados.map(producto => (
              <div
                className="col-6 col-md-4 col-xl-3 d-flex"
                key={producto.id}
              >
                <Link
                  to={`/productos/${producto.id}`}
                  className="text-decoration-none w-100"
                >
                  <article className="producto-card">
                    <div className="producto-img-wrapper">
                      {producto.imagen && (
                        <img
                          src={producto.imagen}
                          className="producto-img"
                          alt={producto.nombre}
                        />
                      )}
                    </div>

                    <div className="producto-info">
                      <h5 className="producto-title">
                        {producto.nombre}
                      </h5>

                      <p className="producto-desc">
                        {producto.descripcion || 'Sin descripción disponible'}
                      </p>

                      <p className="producto-price">
                        ${Number(producto.precio).toLocaleString('es-CL')} CLP
                      </p>
                    </div>
                  </article>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </main>

      <a
        href="https://wa.me/56964333347?text=Hola,%20quiero%20consultar%20por%20un%20producto"
        className="whatsapp-float"
        target="_blank"
        rel="noreferrer"
      >
        ☎
      </a>
    </>
  )
}

export default Productos