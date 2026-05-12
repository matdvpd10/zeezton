import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { obtenerProductos } from '../services/api'

function DetalleProducto() {
  const { id } = useParams()

  const [producto, setProducto] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    obtenerProductos()
      .then(data => {
        const encontrado = data.find(p => String(p.id) === String(id))

        if (!encontrado) {
          throw new Error('Producto no encontrado')
        }

        setProducto(encontrado)
        setCargando(false)
      })
      .catch(error => {
        setError(error.message)
        setCargando(false)
      })
  }, [id])

  if (cargando) {
    return <div className="container py-5 text-light">Cargando producto...</div>
  }

  if (error) {
    return <div className="container py-5 text-danger">{error}</div>
  }

  return (
    <div className="container py-5 text-light">
      <div className="row g-5 align-items-center">
        <div className="col-md-6">
          <img
            src={producto.imagen}
            alt={producto.nombre}
            className="detalle-img"
          />
        </div>

        <div className="col-md-6">
          <span className="detalle-marca">{producto.marca}</span>

          <h1 className="detalle-title">{producto.nombre}</h1>

          <p className="detalle-desc">{producto.descripcion}</p>

          <h2 className="detalle-price">
            ${producto.precio.toLocaleString('es-CL')} CLP
          </h2>

          <p className={producto.stock > 0 ? 'stock-ok' : 'stock-no'}>
            {producto.stock > 0 ? `Stock disponible: ${producto.stock}` : 'Sin stock disponible'}
          </p>

          <a
            href={`https://wa.me/56900000000?text=Hola,%20quiero%20consultar%20por%20${encodeURIComponent(producto.nombre)}`}
            target="_blank"
            className="btn btn-light fw-bold mt-3"
          >
            Consultar por WhatsApp
          </a>
        </div>
      </div>
    </div>
  )
}

export default DetalleProducto