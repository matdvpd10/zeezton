const API_URL = 'https://zeezton.cl'

export async function obtenerProductos() {
  const response = await fetch(`${API_URL}/api/productos/`)

  if (!response.ok) {
    throw new Error('No se pudieron cargar los productos')
  }

  return await response.json()
}