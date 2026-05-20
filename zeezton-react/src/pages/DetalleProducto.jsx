import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { obtenerProductos } from '../services/api'
import '../styles/detalleProducto.css'

function DetalleProducto() {
  const { id } = useParams()
  const [producto, setProducto] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    obtenerProductos()
      .then(data => {
        const productoEncontrado = data.find(p => String(p.id) === String(id))

        if (!productoEncontrado) {
          setError('Producto no encontrado')
        } else {
          setProducto(productoEncontrado)
        }

        setCargando(false)
      })
      .catch(error => {
        setError(error.message)
        setCargando(false)
      })
  }, [id])

  if (cargando) {
    return <div className="container py-5">Cargando producto...</div>
  }

  if (error) {
    return <div className="container py-5 text-danger">{error}</div>
  }

  return (
    <div className="product-detail-mobile">

      <div className="product-gallery-box">
        <img
          src={producto.imagen || '/image_not_found.jpg'}
          alt={producto.nombre}
          className="product-main-image"
        />
      </div>

      <section className="product-info-premium">
        <span className="product-status">Disponible</span>

        <h1>{producto.nombre}</h1>

        <p className="product-brand">
          Marca: <span>{producto.marca}</span>
        </p>

        <div className="product-price">
          ${Number(producto.precio).toLocaleString('es-CL')} CLP
        </div>

        <div className="product-stock">
          Stock disponible: {producto.stock}
        </div>

        <div className="product-benefits">
          <div>
            <i className="fa fa-shield"></i>
            <span>Calidad premium</span>
          </div>
          <div>
            <i className="fa fa-wrench"></i>
            <span>Fácil instalación</span>
          </div>
          <div>
            <i className="fa fa-star"></i>
            <span>Acabado elegante</span>
          </div>
          <div>
            <i className="fa fa-check-circle"></i>
            <span>Compra segura</span>
          </div>
        </div>

        <a
          href={`https://zeezton.cl/pagar/${producto.id}/`}
          className="btn-buy-premium"
        >
          <i className="fa fa-bolt"></i> Comprar ahora
        </a>

        <Link to="/productos" className="btn-back-premium">
          <i className="fa fa-arrow-left"></i> Volver a productos
        </Link>
      </section>

      <section className="product-description-premium">
        <h3>Descripción del producto</h3>

        <p>
          {producto.descripcion ||
            'Producto seleccionado especialmente para mejorar la estética, comodidad y personalización de tu vehículo.'}
        </p>
      </section>

    </div>
  )
}

export default DetalleProducto