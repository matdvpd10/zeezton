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
    <main className="catalogo-page">
      <section className="catalogo-header">
        <div className="container">
          <h1>Catálogo de accesorios</h1>
          <p>
            Descubre nuestra selección completa de repuestos y accesorios premium para tu BMW.
          </p>

          <div className="catalogo-filtros">
            <input
              type="text"
              placeholder="Buscar accesorios..."
              value={buscar}
              onChange={e => setBuscar(e.target.value)}
            />

            <select
              value={marca}
              onChange={e => setMarca(e.target.value)}
            >
              <option value="">Todas las marcas</option>
              {marcas.map(m => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </div>

          <span className="catalogo-count">
            Mostrando {productosFiltrados.length} productos
          </span>
        </div>
      </section>

      <section className="catalogo-grid-section">
        <div className="container">
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
<article className="catalogo-card">
  <div className="catalogo-img-wrap">
    {producto.imagen ? (
      <img
        src={producto.imagen}
        alt={producto.nombre}
        className="catalogo-img"
      />
    ) : (
      <img
        src="/image_not_found.jpg"
        alt="Sin imagen"
        className="catalogo-img"
      />
    )}
  </div>

  <div className="catalogo-info">
    <h5>{producto.nombre}</h5>

                      <p>
                        {producto.descripcion || 'Sin descripción disponible'}
                      </p>

                      <div className="catalogo-bottom">
                        <strong>
                          ${Number(producto.precio).toLocaleString('es-CL')} CLP
                        </strong>

                        <span className="catalogo-cart">
                          🛒
                        </span>
                      </div>
                    </div>
                  </article>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>
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