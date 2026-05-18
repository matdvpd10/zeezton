const API_URL = 'http://127.0.0.1:8000'

export async function obtenerProductos() {
  const response = await fetch(`${API_URL}/api/productos/`)

  if (!response.ok) {
    throw new Error('No se pudieron cargar los productos')
  }

  return await response.json()
}
