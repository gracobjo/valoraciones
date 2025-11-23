import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Filtrar errores conocidos de extensiones del navegador que no afectan la aplicación
const originalConsoleError = console.error
console.error = (...args) => {
  // Ignorar el error de extensiones del navegador sobre "message channel"
  const errorMessage = args.join(' ')
  if (errorMessage.includes('message channel') || 
      errorMessage.includes('asynchronous response') ||
      errorMessage.includes('listener indicated')) {
    // Este error es de extensiones del navegador y no afecta la aplicación
    return
  }
  // Mostrar otros errores normalmente
  originalConsoleError.apply(console, args)
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)




