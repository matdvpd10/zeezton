import { Link } from 'react-router-dom'
import { Mail, Phone, MapPin } from 'lucide-react'

function Footer() {
  return (
    <footer className="footer-zeezton">
      <div className="footer-container">
        <div className="footer-grid">
          <div>
            <div className="footer-brand">
              <span>ZEEZTON</span>
            </div>

            <p>
              Repuestos, accesorios y detalles premium para BMW.
              Estilo, calidad y atención directa para entusiastas.
            </p>
          </div>

          <div>
            <h4>Enlaces rápidos</h4>
            <Link to="/">Inicio</Link>
            <Link to="/productos">Catálogo</Link>
            <Link to="/contacto">Contacto</Link>
          </div>

          <div>
            <h4>Contacto</h4>
            <p><MapPin size={18} /> Santiago, Chile</p>
            <p><Phone size={18} /> +56 9 6433 3347</p>
            <p><Mail size={18} /> contacto@zeezton.cl</p>
          </div>

          <div>
            <h4>Síguenos</h4>
            <div className="footer-social">
              <a href="https://facebook.com" target="_blank" rel="noreferrer">
                f
              </a>
              <a href="https://instagram.com" target="_blank" rel="noreferrer">
                IG
              </a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <span>© 2026 Zeezton Store. Todos los derechos reservados.</span>
          <div>
            <Link to="/privacidad">Política de Privacidad</Link>
            <Link to="/terminos">Términos de Servicio</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer