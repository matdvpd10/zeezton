import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar-zeezton">
      <div className="container navbar-zeezton-content">
        <div className="navbar-links">
          <Link to="/">Inicio</Link>
          <Link to="/productos">Catálogo</Link>
          <Link to="/contacto">Contacto</Link>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;