# JurisMed AI - Frontend

Frontend React con Tailwind CSS para la aplicación de análisis legal-médico.

## Instalación

```bash
npm install
```

## Ejecución

```bash
npm run dev
```

La aplicación estará disponible en: http://localhost:3000

## Tecnologías

- **React 18**: Framework de UI
- **Vite**: Build tool y dev server
- **Tailwind CSS**: Framework de estilos
- **Lucide React**: Iconos modernos
- **Axios**: Cliente HTTP (opcional)

## Estructura

```
frontend/
├── src/
│   ├── components/
│   │   └── DocumentUpload.jsx      # Componente de carga de documentos
│   ├── App.jsx                      # Componente principal con toda la UI
│   ├── main.jsx                     # Punto de entrada
│   └── index.css                    # Estilos globales con Tailwind
├── tailwind.config.js              # Configuración de Tailwind
├── postcss.config.js                # Configuración de PostCSS
└── package.json
```

## Características

- **Diseño moderno**: Interfaz con Tailwind CSS y iconos Lucide
- **Carga de documentos**: Múltiples PDFs (informes clínicos, sentencias, resoluciones)
- **Visualización avanzada**: Comparativa visual entre datos médicos y legales
- **Detección de incongruencias**: Reporte detallado con niveles de severidad
- **Predicción de grado**: Estimación basada en RD 888/2022
- **Responsive**: Diseño adaptativo para móviles y desktop
- **Animaciones**: Transiciones suaves y feedback visual

## Componentes Principales

### App.jsx
Componente principal que maneja:
- Estados de la aplicación (upload, analyzing, results)
- Integración con el backend
- Renderizado condicional de vistas
- Gestión de análisis y incongruencias

### DocumentUpload.jsx
Componente para carga y análisis de documentos:
- Selección de archivos PDF
- Envío al backend para análisis
- Feedback visual del estado

## Personalización

Para modificar los colores o estilos, edita `tailwind.config.js`:

```js
theme: {
  extend: {
    colors: {
      // Tus colores personalizados
    }
  }
}
```

