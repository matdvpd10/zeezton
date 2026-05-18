import {
  BrowserRouter,
  Routes,
  Route
} from 'react-router-dom'

import Navbar from './components/Navbar'
import Footer from './components/Footer'

import Home from './pages/Home'
import Productos from './pages/Productos'
import Contacto from './pages/Contacto'
import DetalleProducto from './pages/DetalleProducto'

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/productos" element={<Productos />} />
        <Route path="/contacto" element={<Contacto />} />
        <Route path="/productos/:id" element={<DetalleProducto />} />
      </Routes>

      <Footer />
    </BrowserRouter>
  )
}

export default App