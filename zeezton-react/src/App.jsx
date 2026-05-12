import DetalleProducto from './pages/DetalleProducto'

import {
  BrowserRouter,
  Routes,
  Route
} from 'react-router-dom'

import Navbar from './components/Navbar'

import Home from './pages/Home'
import Productos from './pages/Productos'
import Contacto from './pages/Contacto'

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
    </BrowserRouter>
  )
}

export default App