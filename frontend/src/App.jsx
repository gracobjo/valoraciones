import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react'
import { Upload, FileText, AlertTriangle, CheckCircle, Activity, Scale, ChevronRight, BookOpen, BarChart3, Brain, Eye, Info } from 'lucide-react'
import { DocumentUpload } from './components/DocumentUpload'

// Diccionario de acrónimos del RD 888/2022
const ACRONYMS = {
  BDGP: {
    name: "Baremo de Deficiencia Global de la Persona",
    description: "Evalúa las deficiencias físicas, mentales, intelectuales o sensoriales de la persona. Se encuentra en el Anexo III del RD 888/2022. Clasifica las deficiencias en clases (0-4) según su severidad.",
    annex: "Anexo III"
  },
  BLA: {
    name: "Baremo de Limitaciones en la Actividad",
    description: "Evalúa las dificultades que una persona puede tener para realizar actividades. Se encuentra en el Anexo IV del RD 888/2022. Máximo 12 puntos.",
    annex: "Anexo IV"
  },
  BRP: {
    name: "Baremo de Restricciones en la Participación",
    description: "Evalúa los problemas que una persona puede experimentar al involucrarse en situaciones vitales. Se encuentra en el Anexo V del RD 888/2022. Máximo 12 puntos.",
    annex: "Anexo V"
  },
  BFCA: {
    name: "Baremo de Factores Contextuales y Barreras Ambientales",
    description: "Evalúa los factores ambientales y personales que pueden actuar como barreras o facilitadores. Se encuentra en el Anexo VI del RD 888/2022. Máximo 24 puntos.",
    annex: "Anexo VI"
  },
  GDA: {
    name: "Grado de Discapacidad Ajustado",
    description: "Resultado del cálculo que combina el BDGP (convertido a VIA - Valor Inicial de Ajuste) con los ajustes de BLA y BRP. Se calcula según el Art. 4.2 del RD 888/2022.",
    annex: "Art. 4.2"
  },
  GFD: {
    name: "Grado Final de Discapacidad",
    description: "Resultado final que incluye el GDA más los puntos del BFCA. Es el porcentaje definitivo de discapacidad reconocido.",
    annex: "Art. 4.2"
  },
  VIA: {
    name: "Valor Inicial de Ajuste",
    description: "Valor central (punto C) de la clase determinada por el BDGP. Se utiliza como base para calcular el GDA aplicando los ajustes de BLA y BRP.",
    annex: "Anexo I"
  },
  VIG: {
    name: "Valor Inicial de Ajuste",
    description: "Sinónimo de VIA. Valor central de la clase determinada por el BDGP según la metodología del Anexo I.",
    annex: "Anexo I"
  }
}

// Componente de Tooltip accesible
const AccessibleTooltip = ({ acronym, children, className = "" }) => {
  const [isVisible, setIsVisible] = useState(false)
  const [isFocused, setIsFocused] = useState(false)
  const [position, setPosition] = useState({ top: 'auto', bottom: '100%', left: '50%', transform: 'translateX(-50%)' })
  const tooltipRef = useRef(null)
  const triggerRef = useRef(null)

  const acronymData = ACRONYMS[acronym] || { name: acronym, description: "Información no disponible" }

  const calculatePosition = () => {
    if (!tooltipRef.current || !triggerRef.current) return

    const tooltip = tooltipRef.current
    const trigger = triggerRef.current
    const rect = trigger.getBoundingClientRect()
    const tooltipRect = tooltip.getBoundingClientRect()
    const viewportWidth = window.innerWidth
    const viewportHeight = window.innerHeight

    // Como ahora usamos fixed, calculamos posiciones absolutas respecto al viewport
    const triggerCenterX = rect.left + rect.width / 2
    const triggerTop = rect.top
    const triggerBottom = rect.bottom
    
    let top = 'auto'
    let bottom = 'auto'
    let left = '50%'
    let right = 'auto'
    let transform = 'translateX(-50%)'
    let marginBottom = '8px'
    let marginTop = '0px'

    // Verificar si hay espacio arriba
    const spaceAbove = triggerTop
    const spaceBelow = viewportHeight - triggerBottom
    const tooltipHeight = tooltipRect.height || 200 // Estimación si aún no se ha renderizado

    // Si no hay suficiente espacio arriba, mostrar abajo
    if (spaceAbove < tooltipHeight + 20 && spaceBelow > tooltipHeight + 20) {
      top = `${triggerBottom + 8}px`
      bottom = 'auto'
      marginTop = '0px'
      marginBottom = '0px'
    } else {
      bottom = `${viewportHeight - triggerTop + 8}px`
      top = 'auto'
      marginTop = '0px'
      marginBottom = '0px'
    }

    // Ajustar posición horizontal para no salirse de la pantalla
    const tooltipWidth = tooltipRect.width || 320 // Estimación si aún no se ha renderizado
    const tooltipLeft = triggerCenterX - tooltipWidth / 2

    if (tooltipLeft < 10) {
      // Muy a la izquierda, alinear a la izquierda
      left = '10px'
      right = 'auto'
      transform = 'translateX(0)'
    } else if (tooltipLeft + tooltipWidth > viewportWidth - 10) {
      // Muy a la derecha, alinear a la derecha
      left = 'auto'
      right = '10px'
      transform = 'translateX(0)'
    } else {
      // Centrado
      left = `${triggerCenterX}px`
      right = 'auto'
      transform = 'translateX(-50%)'
    }

    setPosition({
      top,
      bottom,
      left,
      right,
      transform,
      marginBottom,
      marginTop
    })
  }

  const showTooltip = () => {
    setIsVisible(true)
    setTimeout(() => {
      calculatePosition()
    }, 10)
  }

  const hideTooltip = () => {
    setIsVisible(false)
    setIsFocused(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      hideTooltip()
      triggerRef.current?.blur()
    } else if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      if (!isVisible && !isFocused) {
        setIsFocused(true)
        setIsVisible(true)
        setTimeout(() => {
          calculatePosition()
        }, 10)
      } else {
        hideTooltip()
      }
    }
  }

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (tooltipRef.current && !tooltipRef.current.contains(event.target) &&
          triggerRef.current && !triggerRef.current.contains(event.target)) {
        hideTooltip()
      }
    }

    if (isVisible || isFocused) {
      document.addEventListener('mousedown', handleClickOutside)
      window.addEventListener('resize', calculatePosition)
      window.addEventListener('scroll', calculatePosition)
      return () => {
        document.removeEventListener('mousedown', handleClickOutside)
        window.removeEventListener('resize', calculatePosition)
        window.removeEventListener('scroll', calculatePosition)
      }
    }
  }, [isVisible, isFocused])

  return (
    <span className={`relative inline-block ${className}`}>
      <span
        ref={triggerRef}
        className="underline decoration-dotted decoration-2 underline-offset-2 cursor-help focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 rounded px-1"
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
        onFocus={() => {
          setIsFocused(true)
          setIsVisible(true)
          setTimeout(() => {
            calculatePosition()
          }, 10)
        }}
        onBlur={() => {
          setTimeout(() => {
            if (!isVisible) setIsFocused(false)
          }, 200)
        }}
        onKeyDown={handleKeyDown}
        tabIndex={0}
        role="button"
        aria-label={`${acronym}: ${acronymData.name}. Presiona Enter o Espacio para más información`}
        aria-describedby={isVisible || isFocused ? `tooltip-${acronym}` : undefined}
      >
        {children || acronym}
        <Info className="inline-block w-3 h-3 ml-1 text-blue-600" aria-hidden="true" />
      </span>
      
      {(isVisible || isFocused) && (
        <div
          ref={tooltipRef}
          id={`tooltip-${acronym}`}
          role="tooltip"
          className="fixed z-[99999] w-80 max-w-[90vw] p-4 bg-slate-900 text-white text-sm rounded-lg shadow-2xl pointer-events-auto border border-slate-700"
          style={{ 
            ...position,
            marginBottom: position.marginBottom,
            marginTop: position.marginTop,
            zIndex: 99999
          }}
        >
          <button
            onClick={hideTooltip}
            onKeyDown={(e) => {
              if (e.key === 'Escape') {
                hideTooltip()
                triggerRef.current?.focus()
              }
            }}
            className="absolute top-2 right-2 text-slate-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white rounded w-6 h-6 flex items-center justify-center text-lg leading-none"
            aria-label="Cerrar información"
            title="Cerrar (Escape)"
          >
            ×
          </button>
          <div className="font-bold text-base mb-2 flex items-center gap-2 pr-6">
            <span className="text-white">{acronym}</span>
            <span className="text-xs font-normal text-slate-300">({acronymData.annex})</span>
          </div>
          <div className="font-semibold text-blue-300 mb-2">{acronymData.name}</div>
          <p className="text-slate-200 leading-relaxed text-sm">{acronymData.description}</p>
          {position.bottom === '100%' && (
            <div 
              className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-slate-900"
              aria-hidden="true"
            ></div>
          )}
          {position.top === '100%' && (
            <div 
              className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-slate-900"
              aria-hidden="true"
            ></div>
          )}
        </div>
      )}
    </span>
  )
}

// Componente para etiquetas con descripción accesible
const AccessibleLabel = ({ id, label, description, required = false }) => {
  return (
    <div className="mb-2">
      <label
        htmlFor={id}
        className="block text-sm font-semibold text-slate-700"
        aria-describedby={description ? `${id}-description` : undefined}
      >
        {label}
        {required && <span className="text-red-500 ml-1" aria-label="requerido">*</span>}
      </label>
      {description && (
        <p
          id={`${id}-description`}
          className="text-xs text-slate-500 mt-1"
          role="note"
        >
          {description}
        </p>
      )}
    </div>
  )
}

const Card = ({ children, className = "" }) => (
  <div className={`bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden ${className}`}>
    {children}
  </div>
)

const Badge = ({ type, children, title, ariaLabel }) => {
  const styles = {
    high: "bg-red-100 text-red-700 border-red-200",
    critical: "bg-red-100 text-red-800 border-red-300 font-bold",
    medium: "bg-amber-100 text-amber-700 border-amber-200",
    success: "bg-emerald-100 text-emerald-700 border-emerald-200",
    info: "bg-blue-50 text-blue-700 border-blue-200",
  }
  return (
    <span
      className={`px-2 py-1 rounded-md text-xs font-medium border ${styles[type] || styles.info}`}
      title={title}
      aria-label={ariaLabel || title}
    >
      {children}
    </span>
  )
}

function App() {
  const [step, setStep] = useState('upload') // upload, analyzing, results
  const [analyses, setAnalyses] = useState({
    clinical: null,
    judicial: null,
    administrative: null
  })
  const [files, setFiles] = useState({
    clinical: null,
    judicial: null,
    administrative: null
  })
  const [autoAnalyze, setAutoAnalyze] = useState({
    clinical: false,
    judicial: false,
    administrative: false
  })
  const [inconsistencies, setInconsistencies] = useState(null)
  const [loading, setLoading] = useState(false)
  const [analyzing, setAnalyzing] = useState({
    clinical: false,
    judicial: false,
    administrative: false
  })
  const [progress, setProgress] = useState(0)
  const [highlightedRange, setHighlightedRange] = useState(null)
  const [showDocumentViewer, setShowDocumentViewer] = useState(false)
  const [report, setReport] = useState(null)
  const [showReport, setShowReport] = useState(false)
  const [inconsistencyReport, setInconsistencyReport] = useState(null)
  const [showInconsistencyReport, setShowInconsistencyReport] = useState(false)

  const handleAnalysisComplete = async (typeOrData, dataOrUndefined) => {
    // Manejar ambos casos: (type, data) o solo (data)
    let type, data
    if (dataOrUndefined === undefined) {
      // Solo se pasó un parámetro (data) - usar componentType si está disponible
      data = typeOrData
      type = data.componentType || data.document_type || 'unknown'
      // Mapear document_type del backend al tipo del componente si es necesario
      if (!data.componentType && data.document_type) {
        if (data.document_type === 'judicial') type = 'judicial'
        else if (data.document_type === 'clinical') type = 'clinical'
        else if (data.document_type === 'administrative') type = 'administrative'
      }
    } else {
      // Se pasaron dos parámetros (type, data) - usar el tipo del componente
      type = typeOrData
      data = dataOrUndefined
      // Asegurar que el tipo del componente esté en los datos (solo si data es un objeto)
      if (data && typeof data === 'object' && !data.componentType) {
        data.componentType = type
      }
    }
    // Debug: verificar qué datos se están recibiendo
    console.log(`💾 RECIBIENDO análisis de tipo "${type}":`, {
      has_legal_analysis: !!data?.legal_analysis,
      legal_analysis_type: typeof data?.legal_analysis,
      legal_analysis_value: data?.legal_analysis,
      legal_analysis_keys: data?.legal_analysis ? Object.keys(data.legal_analysis) : [],
      chapter_valuations_count: data?.legal_analysis?.chapter_valuations?.length || 0,
      data_keys: data ? Object.keys(data) : [],
      data_stringified: data ? JSON.stringify(data).substring(0, 200) : 'null'
    })
    
    // IMPORTANTE: Crear una copia profunda para evitar mutaciones
    const dataToStore = JSON.parse(JSON.stringify(data))
    
    console.log(`💾 Datos a guardar (después de copia profunda):`, {
      has_legal_analysis: !!dataToStore.legal_analysis,
      legal_analysis_keys: dataToStore.legal_analysis ? Object.keys(dataToStore.legal_analysis) : [],
      chapter_valuations_count: dataToStore.legal_analysis?.chapter_valuations?.length || 0,
      final_valuation: !!dataToStore.legal_analysis?.final_valuation
    })
    
    const updatedAnalyses = {
      ...analyses,
      [type]: dataToStore
    }
    
    // Debug: verificar qué se está guardando en el estado
    console.log(`💾 Estado actualizado para "${type}":`, {
      has_legal_analysis: !!updatedAnalyses[type]?.legal_analysis,
      legal_analysis_keys: updatedAnalyses[type]?.legal_analysis ? Object.keys(updatedAnalyses[type].legal_analysis) : [],
      chapter_valuations_count: updatedAnalyses[type]?.legal_analysis?.chapter_valuations?.length || 0,
      final_valuation: !!updatedAnalyses[type]?.legal_analysis?.final_valuation
    })
    
    setAnalyses(updatedAnalyses)
    
    // Analizar automáticamente otros documentos pendientes SOLO cuando se completa un análisis
    // Verificar qué documentos tienen archivo pero no análisis
    const pendingTypes = []
    if (files.clinical && !updatedAnalyses.clinical && type !== 'clinical') {
      pendingTypes.push('clinical')
    }
    if (files.judicial && !updatedAnalyses.judicial && type !== 'judicial') {
      pendingTypes.push('judicial')
    }
    if (files.administrative && !updatedAnalyses.administrative && type !== 'administrative') {
      pendingTypes.push('administrative')
    }
    
    // Activar análisis automático para documentos pendientes (secuencialmente, uno tras otro)
    if (pendingTypes.length > 0) {
      console.log(`🔄 Documentos pendientes de análisis automático: ${pendingTypes.join(', ')}`)
      
      // Activar el primero inmediatamente
      const firstPendingType = pendingTypes[0]
      console.log(`🚀 Activando auto-análisis para: ${firstPendingType}`)
      
      setAutoAnalyze(prev => ({
        ...prev,
        [firstPendingType]: true
      }))
      
      // Desactivar después de un momento
      setTimeout(() => {
        setAutoAnalyze(prev => ({
          ...prev,
          [firstPendingType]: false
        }))
      }, 3000) // Dar más tiempo para que se complete el análisis
      
      // Si hay más documentos pendientes, activarlos después de que se complete el primero
      // Esto se manejará cuando se complete el análisis del primero (en el próximo handleAnalysisComplete)
    }
    
    // No cambiar automáticamente a 'results' para permitir analizar múltiples documentos
    // El usuario puede ver los resultados cuando quiera usando el botón
    const hasAnyAnalysis = Object.values(updatedAnalyses).some(a => a !== null)
    
    console.log('🔍 Verificando si mostrar resultados:', {
      hasAnyAnalysis,
      clinical: !!updatedAnalyses.clinical,
      judicial: !!updatedAnalyses.judicial,
      administrative: !!updatedAnalyses.administrative,
      currentStep: step
    })
    
    // No cambiar automáticamente a 'results' - el usuario puede seguir analizando documentos
    // y ver los resultados cuando quiera usando el botón "Ver Resultados"
    
    // Detectar discrepancias automáticamente si hay dos documentos cargados
    const hasClinicalOrJudicial = updatedAnalyses.clinical !== null || updatedAnalyses.judicial !== null
    const hasAdministrative = updatedAnalyses.administrative !== null
    
    if (hasClinicalOrJudicial && hasAdministrative && !inconsistencies) {
      // Esperar un momento para que el estado se actualice
      setTimeout(async () => {
        await handleCheckInconsistencies(updatedAnalyses)
      }, 500)
    }
  }
  
  const handleFileChange = (type, file) => {
    setFiles(prev => ({
      ...prev,
      [type]: file
    }))
  }
  
  const handleCheckInconsistencies = async (analysesToCheck = null) => {
    const analysesToUse = analysesToCheck || analyses
    setLoading(true)
    try {
      const response = await fetch('/api/analyze/inconsistencies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          clinical_report: analysesToUse.clinical,
          judicial_sentence: analysesToUse.judicial,
          administrative_resolution: analysesToUse.administrative
        })
      })
      const data = await response.json()
      setInconsistencies(data)
    } catch (error) {
      console.error('Error checking inconsistencies:', error)
      // No mostrar alerta, solo loggear el error
    } finally {
      setLoading(false)
    }
  }

  const handleHighlightText = (start, end, diagnosis) => {
    setHighlightedRange({ start, end, diagnosis })
    setShowDocumentViewer(true)
    // Scroll al visor de documento
    setTimeout(() => {
      const viewer = document.getElementById('document-viewer')
      if (viewer) {
        viewer.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }, 100)
  }


  const handleGenerateInconsistencyReport = async () => {
    setLoading(true)
    try {
      // Determinar qué documentos usar (pericial vs resolución)
      const pericialData = analyses.clinical || analyses.judicial
      const resolutionData = analyses.administrative
      
      if (!pericialData || !resolutionData) {
        alert('Necesitas tener al menos un documento pericial y una resolución administrativa para generar el informe de inconsistencia')
        setLoading(false)
        return
      }
      
      const response = await fetch('/api/generate/inconsistency-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resolution_data: resolutionData,
          pericial_data: pericialData
        })
      })
      
      if (!response.ok) {
        // Manejar respuesta de error del servidor
        let errorMessage = 'Error al generar el informe de inconsistencias'
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorData.message || errorMessage
        } catch (e) {
          errorMessage = `Error del servidor: ${response.status} ${response.statusText}`
        }
        alert(`Error: ${errorMessage}`)
        setLoading(false)
        return
      }
      
      const data = await response.json()
      if (data && data.report) {
        setInconsistencyReport(data.report)
        setShowInconsistencyReport(true)
        setTimeout(() => {
          const reportViewer = document.getElementById('inconsistency-report-viewer')
          if (reportViewer) {
            reportViewer.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        }, 100)
      } else {
        alert('Error: El servidor no devolvió el informe correctamente')
      }
    } catch (err) {
      console.error('Error generando informe de inconsistencia:', err)
      alert(`Error al generar el informe de inconsistencia: ${err.message || 'Error desconocido'}`)
    } finally {
      setLoading(false)
    }
  }

  // Simulación del proceso de análisis
  useEffect(() => {
    if (step === 'analyzing') {
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval)
            setStep('results')
            return 100
          }
          return prev + 2
        })
      }, 50)
      return () => clearInterval(interval)
    }
  }, [step])

  // Callbacks optimizados para DocumentUpload
  const handleClinicalFileChange = useCallback((file) => handleFileChange('clinical', file), [handleFileChange])
  const handleJudicialFileChange = useCallback((file) => handleFileChange('judicial', file), [handleFileChange])
  const handleAdministrativeFileChange = useCallback((file) => handleFileChange('administrative', file), [handleFileChange])

  const handleClinicalAnalysisStart = useCallback((type) => {
    if (type === null) {
      return
    }
    setAnalyzing(prev => ({ ...prev, [type]: true }))
    console.log(`🟡 Análisis iniciado para: ${type}`)
  }, [])

  const handleJudicialAnalysisStart = useCallback((type) => {
    if (type === null) {
      return
    }
    setAnalyzing(prev => ({ ...prev, [type]: true }))
    console.log(`🟡 Análisis iniciado para: ${type}`)
  }, [])

  const handleAdministrativeAnalysisStart = useCallback((type) => {
    if (type === null) {
      return
    }
    setAnalyzing(prev => ({ ...prev, [type]: true }))
    console.log(`🟡 Análisis iniciado para: ${type}`)
  }, [])

  const handleClinicalAnalysisComplete = useCallback((typeOrData, dataOrUndefined) => {
    let type, data
    if (dataOrUndefined === undefined) {
      data = typeOrData
      type = 'clinical'
    } else {
      type = typeOrData
      data = dataOrUndefined
    }
    handleAnalysisComplete(type, data)
  }, [handleAnalysisComplete])

  const handleJudicialAnalysisComplete = useCallback((typeOrData, dataOrUndefined) => {
    let type, data
    if (dataOrUndefined === undefined) {
      data = typeOrData
      type = 'judicial'
    } else {
      type = typeOrData
      data = dataOrUndefined
    }
    console.log('🔍 CALLBACK judicial - datos recibidos:', {
      type,
      has_legal_analysis: !!data?.legal_analysis,
      legal_analysis_keys: data?.legal_analysis ? Object.keys(data.legal_analysis) : [],
      data_keys: data ? Object.keys(data) : []
    })
    handleAnalysisComplete(type, data)
  }, [handleAnalysisComplete])

  const handleAdministrativeAnalysisComplete = useCallback((typeOrData, dataOrUndefined) => {
    let type, data
    if (dataOrUndefined === undefined) {
      data = typeOrData
      type = 'administrative'
    } else {
      type = typeOrData
      data = dataOrUndefined
    }
    handleAnalysisComplete(type, data)
  }, [handleAnalysisComplete])

  // JSX para el paso de upload (convertido de función a variable para evitar re-montajes)
  const renderUploadJsx = (
    <div className="max-w-2xl mx-auto mt-10 p-6">
      <div className="text-center mb-10">
        <div className="bg-blue-600 w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-blue-200">
          <Scale className="text-white w-8 h-8" />
        </div>
        <h1 className="text-3xl font-bold text-slate-900 mb-2">JurisMed AI</h1>
        <p className="text-slate-500">
          Sube tus informes médicos, sentencias y la resolución administrativa (PDF, DOC, DOCX).
          Nuestra IA cruzará los datos con el RD 888/2022 para detectar errores de valoración.
        </p>
      </div>

      {/* Botón para ver resultados si hay análisis completados */}
      {Object.values(analyses).some(a => a !== null) && (
        <div className="mb-6 text-center">
          <button
            onClick={() => {
              console.log('🖱️ Click en "Ver Resultados del Análisis"')
              console.log('📊 Análisis disponibles:', {
                clinical: !!analyses.clinical,
                judicial: !!analyses.judicial,
                administrative: !!analyses.administrative
              })
              setStep('results')
            }}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 mx-auto shadow-md"
          >
            <BarChart3 className="w-5 h-5" />
            Ver Resultados del Análisis
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <DocumentUpload
          key="clinical-upload"
          type="clinical"
          label="Informe Clínico"
          autoAnalyze={autoAnalyze.clinical}
          file={files.clinical}
          analysis={analyses.clinical}
          onFileChange={handleClinicalFileChange}
          onAnalysisStart={handleClinicalAnalysisStart}
          onAnalysisComplete={handleClinicalAnalysisComplete}
        />
        <DocumentUpload
          key="judicial-upload"
          type="judicial"
          label="Sentencia Judicial"
          autoAnalyze={autoAnalyze.judicial}
          file={files.judicial}
          analysis={analyses.judicial}
          onFileChange={handleJudicialFileChange}
          onAnalysisStart={handleJudicialAnalysisStart}
          onAnalysisComplete={handleJudicialAnalysisComplete}
        />
        <DocumentUpload
          key="administrative-upload"
          type="administrative"
          label="Resolución Administrativa"
          autoAnalyze={autoAnalyze.administrative}
          file={files.administrative}
          analysis={analyses.administrative}
          onFileChange={handleAdministrativeFileChange}
          onAnalysisStart={handleAdministrativeAnalysisStart}
          onAnalysisComplete={handleAdministrativeAnalysisComplete}
        />
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
        <div className="p-4">
          <Brain className="w-6 h-6 text-purple-500 mx-auto mb-2" />
          <h3 className="font-semibold text-sm text-slate-800">Minería de Texto</h3>
          <p className="text-xs text-slate-600">Extrae "Hechos Probados" de sentencias</p>
        </div>
        <div className="p-4">
          <BookOpen className="w-6 h-6 text-indigo-600 mx-auto mb-2" />
          <h3 className="font-semibold text-sm text-slate-800">RD 888/2022</h3>
          <p className="text-xs text-slate-600">Aplica reglas de Clases y Grados</p>
        </div>
        <div className="p-4">
          <Eye className="w-6 h-6 text-emerald-600 mx-auto mb-2" />
          <h3 className="font-semibold text-sm text-slate-800">Auditoría Legal</h3>
          <p className="text-xs text-slate-600">Detecta incongruencias administrativas</p>
        </div>
      </div>
    </div>
  )

  // JSX para el paso de analyzing (convertido de función a variable para evitar re-montajes)
  const renderAnalyzingJsx = (
    <div className="max-w-xl mx-auto mt-20 text-center p-6">
      <Activity className="w-16 h-16 text-blue-500 mx-auto mb-6 animate-pulse" />
      <h2 className="text-2xl font-bold text-slate-800 mb-4">Procesando Expediente...</h2>

      <div className="w-full bg-slate-200 rounded-full h-4 mb-2 overflow-hidden">
        <div
          className="bg-blue-600 h-4 rounded-full transition-all duration-300 ease-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <div className="flex justify-between text-xs text-slate-500 font-medium">
        <span>Extracción OCR</span>
        <span>Análisis Semántico</span>
        <span>Verificación RD 888/2022</span>
      </div>

      <div className="mt-8 text-left space-y-2">
        <p className={`text-sm ${progress > 20 ? 'text-slate-700' : 'text-slate-300'} transition-colors flex items-center`}>
          {progress > 20 ? <CheckCircle className="w-4 h-4 text-green-500 mr-2" /> : <span className="w-4 h-4 mr-2 inline-block"></span>}
          Leyendo documentos...
        </p>
        <p className={`text-sm ${progress > 50 ? 'text-slate-700' : 'text-slate-300'} transition-colors flex items-center`}>
          {progress > 50 ? <CheckCircle className="w-4 h-4 text-green-500 mr-2" /> : <span className="w-4 h-4 mr-2 inline-block"></span>}
          Extrayendo goniometría y limitaciones funcionales...
        </p>
        <p className={`text-sm ${progress > 80 ? 'text-slate-700' : 'text-slate-300'} transition-colors flex items-center`}>
          {progress > 80 ? <CheckCircle className="w-4 h-4 text-green-500 mr-2" /> : <span className="w-4 h-4 mr-2 inline-block"></span>}
          Comparando con Resolución y Anexos BOE...
        </p>
      </div>
    </div>
  )

  // JSX para el paso de results (convertido usando useMemo para evitar re-montajes)
  const renderResultsJsx = useMemo(() => {
    const hasDocuments = Object.values(analyses).some(a => a !== null)
    
    // Debug: verificar qué documentos hay
    console.log('🔍 RenderResults - documentos disponibles:', {
      clinical: !!analyses.clinical,
      judicial: !!analyses.judicial,
      administrative: !!analyses.administrative,
      hasDocuments,
      step
    })
    
    if (!hasDocuments) {
      return (
        <div className="max-w-2xl mx-auto mt-20 text-center p-6">
          <p className="text-slate-600">No hay documentos analizados aún.</p>
          <button
            onClick={() => setStep('upload')}
            className="mt-4 text-blue-600 font-medium hover:underline flex items-center justify-center gap-2"
          >
            Volver a cargar documentos <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )
    }

    // Extraer datos para visualización
    const clinicalData = analyses.clinical
    const judicialData = analyses.judicial
    const administrativeData = analyses.administrative

    // Obtener diagnósticos (usar los deduplicados del análisis legal)
    const getDiagnoses = (data) => {
      if (!data) return []
      
      // Priorizar diagnósticos deduplicados del análisis legal
      if (data.legal_analysis && data.legal_analysis.detected_diagnoses) {
        return data.legal_analysis.detected_diagnoses.map(d => 
          typeof d === 'string' ? d : d.text || d
        )
      }
      
      // Fallback: usar entidades originales si no hay análisis legal
      if (data.entities && data.entities.DIAGNOSIS) {
        // Deduplicar en el frontend también
        const seen = new Set()
        const unique = []
        for (const d of data.entities.DIAGNOSIS) {
          const text = (d.text || d).trim()
          const normalized = text.toLowerCase().replace(/\s+/g, ' ').trim()
          if (text && !seen.has(normalized)) {
            seen.add(normalized)
            unique.push(text)
          }
        }
        return unique
      }
      
      return []
    }

    // Obtener limitaciones
    const getLimitations = (data) => {
      if (!data || !data.legal_analysis) return []
      const metrics = data.legal_analysis.detected_metrics || {}
      const limitations = []
      if (metrics.abduccion) limitations.push(`Abducción limitada a ${metrics.abduccion}º`)
      if (metrics.flexion) limitations.push(`Flexión limitada a ${metrics.flexion}º`)
      if (metrics.rotacion) limitations.push(`Rotación limitada a ${metrics.rotacion}º`)
      return limitations
    }

    // Obtener clasificación
    const getClassification = (data) => {
      if (!data || !data.legal_analysis) return null
      return data.legal_analysis.suggested_classification
    }

    const medicalDiagnoses = getDiagnoses(judicialData || clinicalData)
    const medicalLimitations = getLimitations(judicialData || clinicalData)
    const adminClassification = getClassification(administrativeData)
    const predictedClassification = getClassification(clinicalData || judicialData)
    
    // Obtener valoraciones por capítulo
    const getChapterValuations = (data) => {
      if (!data || !data.legal_analysis) return []
      return data.legal_analysis.chapter_valuations || []
    }
    
    // Obtener valoración final
    const getFinalValuation = (data) => {
      if (!data || !data.legal_analysis) return null
      return data.legal_analysis.final_valuation || null
    }
    
    // Calcular valoraciones
    // Para resoluciones administrativas, también mostrar valoraciones
    const chapterValuations = getChapterValuations(judicialData || clinicalData || administrativeData)
    const finalValuation = getFinalValuation(judicialData || clinicalData || administrativeData)
    
    // Debug: mostrar en consola si hay valoraciones
    console.log('📊 Datos de análisis:', {
      judicial: !!judicialData,
      clinical: !!clinicalData,
      administrative: !!administrativeData,
      chapterValuations: chapterValuations.length,
      finalValuation: !!finalValuation,
      judicial_has_legal: !!judicialData?.legal_analysis,
      clinical_has_legal: !!clinicalData?.legal_analysis,
      admin_has_legal: !!administrativeData?.legal_analysis
    })
    
    // Debug detallado de cada análisis
    if (judicialData) {
      console.log('📄 Judicial data:', {
        has_legal_analysis: !!judicialData.legal_analysis,
        chapter_valuations_count: judicialData.legal_analysis?.chapter_valuations?.length || 0,
        final_valuation: judicialData.legal_analysis?.final_valuation,
        suggested_classification: judicialData.legal_analysis?.suggested_classification
      })
    }
    if (clinicalData) {
      console.log('📄 Clinical data:', {
        has_legal_analysis: !!clinicalData.legal_analysis,
        chapter_valuations_count: clinicalData.legal_analysis?.chapter_valuations?.length || 0,
        final_valuation: clinicalData.legal_analysis?.final_valuation,
        suggested_classification: clinicalData.legal_analysis?.suggested_classification
      })
    }
    
    if (chapterValuations.length > 0) {
      console.log('✅ Valoraciones por capítulo encontradas:', chapterValuations)
    } else {
      console.log('⚠️ No hay valoraciones por capítulo. Revisando datos originales...')
      if (judicialData?.legal_analysis?.chapter_valuations) {
        console.log('  - Judicial tiene chapter_valuations:', judicialData.legal_analysis.chapter_valuations)
      }
      if (clinicalData?.legal_analysis?.chapter_valuations) {
        console.log('  - Clinical tiene chapter_valuations:', clinicalData.legal_analysis.chapter_valuations)
      }
    }
    if (finalValuation) {
      console.log('✅ Valoración final encontrada:', finalValuation)
    } else {
      console.log('⚠️ No se encontró valoración final. Datos disponibles:', {
        judicial_final: judicialData?.legal_analysis?.final_valuation,
        clinical_final: clinicalData?.legal_analysis?.final_valuation,
        admin_final: administrativeData?.legal_analysis?.final_valuation
      })
    }

    return (
      <div className="max-w-5xl mx-auto p-4 md:p-8 pb-20">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
              <FileText className="text-blue-600" /> Informe de Auditoría
            </h2>
            <p className="text-slate-500 text-sm mt-1">
              {inconsistencies && inconsistencies.total_count > 0 ? (
                <span>Estado: <span className="text-red-500 font-bold">Reclamable</span></span>
              ) : (
                <span>Estado: <span className="text-green-500 font-bold">Sin incongruencias detectadas</span></span>
              )}
            </p>
          </div>
          <button
            onClick={() => {
              setStep('upload')
              setAnalyses({ clinical: null, judicial: null, administrative: null })
              setInconsistencies(null)
            }}
            className="mt-4 md:mt-0 text-blue-600 font-medium hover:underline flex items-center"
          >
            Nuevo Análisis <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {/* Comparativa Diagnósticos */}
            <Card className="p-0">
              <div className="bg-slate-50 p-4 border-b border-slate-200 font-semibold text-slate-700 flex justify-between items-center">
                <span>Cruce de Datos: Médico vs Legal</span>
                <Badge type="info">Análisis NLP</Badge>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200">
                <div className="p-5">
                  <h4 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
                    <Activity className="w-4 h-4 text-blue-500" /> Realidad (Documentos)
                  </h4>
                  <ul className="space-y-2">
                    {medicalDiagnoses.length > 0 ? (
                      medicalDiagnoses.map((d, i) => (
                        <li key={i} className="text-sm text-slate-600 bg-blue-50 p-2 rounded border border-blue-100">{d}</li>
                      ))
                    ) : (
                      <li className="text-sm text-slate-600 italic">No se detectaron diagnósticos</li>
                    )}
                  </ul>
                  {medicalLimitations.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-slate-100">
                      <p className="text-xs font-bold text-slate-500 uppercase mb-2">Limitaciones Detectadas</p>
                      {medicalLimitations.map((l, i) => (
                        <div key={i} className="text-xs text-slate-600 flex items-center gap-1 mb-1">
                          <div className="w-1.5 h-1.5 bg-red-400 rounded-full"></div> {l}
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="p-5 bg-slate-50/50">
                  <h4 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
                    <Scale className="w-4 h-4 text-slate-500" /> Valoración Administrativa
                  </h4>
                  {adminClassification ? (
                    <>
                      <div className="mb-4">
                        <p className="text-xs text-slate-600 uppercase font-bold">Clasificación</p>
                        <p className="text-sm font-medium text-slate-700">
                          {adminClassification.description || `Clase ${adminClassification.class_number || 'N/A'}`}
                        </p>
                      </div>
                      <div className="flex justify-between items-center bg-white p-3 rounded-lg border border-slate-200 shadow-sm">
                        <div>
                          <p className="text-xs text-slate-600 uppercase font-bold">Grado</p>
                          <p className="text-2xl font-bold text-slate-800">
                            {adminClassification.suggested_percentage || 'N/A'}%
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-slate-600 uppercase font-bold">Clase</p>
                          <Badge type="info">Clase {adminClassification.class_number || 'N/A'}</Badge>
                        </div>
                      </div>
                    </>
                  ) : administrativeData ? (
                    <div className="space-y-2">
                      <p className="text-sm text-slate-600">
                        Resolución administrativa cargada: <span className="font-semibold">{administrativeData.filename || 'Documento'}</span>
                      </p>
                      
                      {/* Verificar si es una copia auténtica con enlace externo */}
                      {(() => {
                        const extractedText = administrativeData.full_extracted_text || administrativeData.extracted_text || ''
                        const urlPattern = /https?:\/\/[^\s\)]+/g
                        const urls = extractedText.match(urlPattern) || []
                        const isCopyWithLink = urls.some(url => url.toLowerCase().includes('verdocumentos') || url.toLowerCase().includes('jcyl.es'))
                        
                        if (isCopyWithLink) {
                          return (
                            <div className="mt-3 p-3 bg-amber-50 border-2 border-amber-300 rounded-lg">
                              <p className="text-xs font-bold text-amber-800 uppercase mb-2 flex items-center gap-2">
                                <AlertTriangle className="w-4 h-4" />
                                Copia Auténtica con Enlace Externo
                              </p>
                              <p className="text-xs text-amber-700 mb-2">
                                Este PDF solo contiene metadatos de registro. El contenido real de la resolución está en una URL externa.
                              </p>
                              {urls.length > 0 && (
                                <div className="mt-2">
                                  <p className="text-xs font-semibold text-amber-800 mb-1">Documento real disponible en:</p>
                                  <a 
                                    href={urls[0]} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="text-xs text-blue-600 hover:text-blue-800 underline break-all"
                                  >
                                    {urls[0]}
                                  </a>
                                  <button
                                    onClick={async () => {
                                      setLoading(true)
                                      try {
                                        const response = await fetch('/api/download-and-analyze', {
                                          method: 'POST',
                                          headers: {
                                            'Content-Type': 'application/json',
                                          },
                                          body: JSON.stringify({
                                            url: urls[0],
                                            document_type: 'administrative'
                                          })
                                        })
                                        
                                        if (!response.ok) {
                                          const errorData = await response.json()
                                          throw new Error(errorData.detail || 'Error al descargar el documento')
                                        }
                                        
                                        const data = await response.json()
                                        
                                        // Mostrar logs de depuración
                                        if (data.debug_logs && data.debug_logs.length > 0) {
                                          console.group(`📥 Documento descargado y analizado`)
                                          data.debug_logs.forEach(log => {
                                            if (log.includes('[SUCCESS]')) {
                                              console.log('%c' + log, 'color: green; font-weight: bold')
                                            } else if (log.includes('[WARNING]')) {
                                              console.warn(log)
                                            } else if (log.includes('[ERROR]')) {
                                              console.error(log)
                                            } else {
                                              console.log(log)
                                            }
                                          })
                                          console.groupEnd()
                                        }
                                        
                                        // Actualizar el análisis con el documento descargado
                                        handleAnalysisComplete('administrative', data)
                                        
                                        // Mostrar mensaje de éxito
                                        alert('Documento descargado y analizado correctamente')
                                      } catch (error) {
                                        console.error('Error descargando documento:', error)
                                        alert(`Error al descargar el documento: ${error.message}\n\nPuedes intentar descargarlo manualmente desde el enlace.`)
                                      } finally {
                                        setLoading(false)
                                      }
                                    }}
                                    disabled={loading}
                                    className="mt-3 w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                  >
                                    {loading ? (
                                      <>
                                        <Activity className="w-4 h-4 animate-spin" />
                                        Descargando y analizando...
                                      </>
                                    ) : (
                                      <>
                                        <Upload className="w-4 h-4" />
                                        Descargar y Analizar Automáticamente
                                      </>
                                    )}
                                  </button>
                                  <p className="text-xs text-amber-600 mt-2 italic">
                                    O descarga el documento manualmente desde la URL y súbelo.
                                  </p>
                                </div>
                              )}
                            </div>
                          )
                        }
                        return null
                      })()}
                      
                      {administrativeData.legal_analysis?.detected_diagnoses?.length > 0 && (
                        <div className="mt-2">
                          <p className="text-xs text-slate-500 uppercase font-bold mb-1">Diagnósticos detectados:</p>
                          <ul className="space-y-1">
                            {administrativeData.legal_analysis.detected_diagnoses.slice(0, 3).map((diag, idx) => (
                              <li key={idx} className="text-xs text-slate-600 bg-white p-2 rounded border border-slate-200">
                                {diag.text || diag}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {administrativeData.legal_analysis?.suggested_classification && (
                        <div className="mt-2 p-2 bg-white rounded border border-slate-200">
                          <p className="text-xs text-slate-500 uppercase font-bold">Valoración detectada:</p>
                          <p className="text-sm font-bold text-slate-700">
                            {administrativeData.legal_analysis.suggested_classification.suggested_percentage || 'N/A'}%
                            {administrativeData.legal_analysis.suggested_classification.class_number && (
                              <span className="ml-2 text-xs font-normal">(Clase {administrativeData.legal_analysis.suggested_classification.class_number})</span>
                            )}
                          </p>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-sm text-slate-600 italic">No hay resolución administrativa cargada</p>
                  )}
                </div>
              </div>
            </Card>

            {/* Valoración Detallada de Lesiones (BDGP - Anexo III) */}
            {(chapterValuations && chapterValuations.length > 0) && (
              <Card>
                <div className="bg-blue-50 p-4 border-b border-blue-100 font-semibold text-blue-800 flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" aria-hidden="true" /> 
                  Desglose Detallado de Lesiones y Valoración (<AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip> - <AccessibleTooltip acronym="BDGP">Anexo III</AccessibleTooltip>)
                </div>
                <div className="p-5 space-y-4">
                  {chapterValuations.map((val, i) => {
                    const classification = val.classification || {}
                    const bodyPart = val.body_part || 'N/A'
                    
                    // Obtener métricas relevantes para esta lesión (vienen del backend)
                    const relevantMetricsData = val.relevant_metrics || {}
                    const relevantMetrics = []
                    
                    if (relevantMetricsData.abduccion) {
                      relevantMetrics.push({ name: 'Abducción', value: relevantMetricsData.abduccion, unit: '°' })
                    }
                    if (relevantMetricsData.flexion) {
                      relevantMetrics.push({ name: 'Flexión', value: relevantMetricsData.flexion, unit: '°' })
                    }
                    if (relevantMetricsData.rotacion) {
                      relevantMetrics.push({ name: 'Rotación', value: relevantMetricsData.rotacion, unit: '°' })
                    }
                    if (relevantMetricsData.extension) {
                      relevantMetrics.push({ name: 'Extensión', value: relevantMetricsData.extension, unit: '°' })
                    }
                    
                    // Justificación de la valoración
                    let justification = classification.legal_basis || 'RD 888/2022, Anexo III (BDGP)'
                    if (relevantMetrics.length > 0) {
                      const metricsText = relevantMetrics.map(m => `${m.name}: ${m.value}${m.unit}`).join(', ')
                      justification = `Basado en métricas funcionales: ${metricsText}. ${justification}`
                    }
                    
                    return (
                      <div key={i} className="border border-slate-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
                        <div className="bg-slate-50 p-4 border-b border-slate-200">
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <span className="text-xs font-bold text-slate-500 bg-slate-200 px-2 py-1 rounded">
                                  LESION {i + 1}
                                </span>
                                <Badge 
                                  type="info"
                                  title={`Capítulo ${val.chapter_number || val.chapter || 'N/A'} del RD 888/2022`}
                                  ariaLabel={`Capítulo ${val.chapter_number || val.chapter || 'N/A'} del Real Decreto 888/2022`}
                                >
                                  Cap. {val.chapter_number || val.chapter || 'N/A'}
                                </Badge>
                                {val.is_proven_fact && (
                                  <Badge 
                                    type="success"
                                    title="Este diagnóstico está reconocido como hecho probado en la sentencia judicial"
                                    ariaLabel="Hecho probado: este diagnóstico está reconocido como hecho probado en la sentencia judicial"
                                  >
                                    Hecho Probado
                                  </Badge>
                                )}
                              </div>
                              <h4 
                                className="font-bold text-slate-800 text-base mb-1"
                                aria-label={`Diagnóstico: ${val.diagnosis || 'Diagnóstico no especificado'}`}
                              >
                                {val.diagnosis || 'Diagnóstico no especificado'}
                              </h4>
                              <p 
                                className="text-xs text-slate-500"
                                aria-label={`Capítulo ${val.chapter || val.chapter_number || 'N/A'}, parte del cuerpo afectada: ${bodyPart}`}
                              >
                                {val.chapter || val.chapter_number || 'N/A'} - {bodyPart}
                              </p>
                            </div>
                            <div className="text-right">
                              <div 
                                className="text-3xl font-bold text-blue-600 mb-1"
                                aria-label={`Porcentaje de discapacidad: ${val.percentage || 0} por ciento`}
                              >
                                {val.percentage || 0}%
                              </div>
                              <Badge 
                                type="info" 
                                className="text-xs"
                                title={`Clase ${val.class || val.class_number || classification.class_number || 'N/A'}: ${val.description || classification.description || 'Deficiencia moderada'}`}
                                ariaLabel={`Clase ${val.class || val.class_number || classification.class_number || 'N/A'}, ${val.description || classification.description || 'Deficiencia moderada'}`}
                              >
                                Clase {val.class || val.class_number || classification.class_number || 'N/A'}
                              </Badge>
                            </div>
                          </div>
                        </div>
                        
                        <div className="p-4 bg-white">
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            {/* Métricas que determinan la valoración */}
                            {relevantMetrics.length > 0 && (
                              <div className="bg-blue-50 p-3 rounded-lg border border-blue-100">
                                <p className="text-xs font-semibold text-blue-800 uppercase mb-2" id={`metrics-${i}`}>
                                  Métricas Funcionales Detectadas
                                </p>
                                <div className="space-y-1" role="list" aria-labelledby={`metrics-${i}`}>
                                  {relevantMetrics.map((metric, idx) => (
                                    <div key={idx} className="flex items-center justify-between text-sm" role="listitem">
                                      <span className="text-slate-700" aria-label={`${metric.name} medida en grados`}>{metric.name}:</span>
                                      <span className="font-bold text-blue-600" aria-label={`${metric.name}: ${metric.value} ${metric.unit}`}>{metric.value}{metric.unit}</span>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                            
                            {/* Criterios de clasificación */}
                            <div className="bg-emerald-50 p-3 rounded-lg border border-emerald-100">
                              <p className="text-xs font-semibold text-emerald-800 uppercase mb-2">
                                Categorización
                              </p>
                              <div className="space-y-1 text-sm">
                                <div className="flex items-center justify-between">
                                  <span className="text-slate-700" aria-label="Clasificación de la deficiencia">Clase:</span>
                                  <span 
                                    className="font-bold text-emerald-600"
                                    aria-label={`Clase ${val.class || val.class_number || classification.class_number || 'N/A'}`}
                                  >
                                    Clase {val.class || val.class_number || classification.class_number || 'N/A'}
                                  </span>
                                </div>
                                <div className="flex items-center justify-between">
                                  <span className="text-slate-700" aria-label="Descripción de la deficiencia">Descripción:</span>
                                  <span 
                                    className="font-medium text-emerald-700 text-xs text-right"
                                    aria-label={`Descripción: ${val.description || classification.description || 'Deficiencia moderada'}`}
                                  >
                                    {val.description || classification.description || 'Deficiencia moderada'}
                                  </span>
                                </div>
                                {classification.percentage_range && (
                                  <div className="flex items-center justify-between">
                                    <span className="text-slate-700" aria-label="Rango de porcentaje para esta clase">Rango:</span>
                                    <span 
                                      className="font-medium text-emerald-700 text-xs"
                                      aria-label={`Rango de porcentaje: de ${classification.percentage_range[0]} a ${classification.percentage_range[1]} por ciento`}
                                    >
                                      {classification.percentage_range[0]}% - {classification.percentage_range[1]}%
                                    </span>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                          
                          {/* Justificación de la valoración */}
                          <div className="bg-amber-50 p-3 rounded-lg border border-amber-100">
                            <p 
                              className="text-xs font-semibold text-amber-800 uppercase mb-2"
                              id={`justification-title-${i}`}
                            >
                              Justificación de la Valoración
                            </p>
                            <p 
                              className="text-sm text-slate-700 leading-relaxed"
                              aria-labelledby={`justification-title-${i}`}
                              role="note"
                            >
                              {justification}
                            </p>
                            {relevantMetrics.length > 0 && (
                              <div className="mt-2 pt-2 border-t border-amber-200">
                                <p className="text-xs text-amber-700">
                                  <span className="font-semibold">Criterio aplicado:</span> Las métricas funcionales ({relevantMetrics.map(m => `${m.name} ${m.value}${m.unit}`).join(', ')}) 
                                  determinan la clasificación según los rangos establecidos en el <AccessibleTooltip acronym="BDGP">Anexo III</AccessibleTooltip> del RD 888/2022.
                                </p>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    )
                  })}
                  
                  {/* Resumen de puntos */}
                  {finalValuation && (
                    <div className="mt-6 bg-gradient-to-r from-indigo-50 to-blue-50 p-5 rounded-lg border-2 border-indigo-200">
                      <h4 
                        className="font-bold text-indigo-800 mb-4 flex items-center gap-2"
                        id="summary-title"
                      >
                        <Scale className="w-5 h-5" aria-hidden="true" />
                        Resumen del Cálculo de Puntos
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div className="bg-white p-4 rounded-lg border border-indigo-200">
                          <p className="text-xs font-semibold text-indigo-700 uppercase mb-3">
                            <AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip> (<AccessibleTooltip acronym="BDGP">Anexo III</AccessibleTooltip>) - Deficiencias
                          </p>
                          <div className="space-y-2">
                            {chapterValuations.map((val, idx) => (
                              <div 
                                key={idx} 
                                className="flex items-center justify-between text-sm border-b border-slate-100 pb-1"
                                role="listitem"
                                aria-label={`Deficiencia ${idx + 1}: ${val.diagnosis || 'Diagnóstico no especificado'}, porcentaje: ${val.percentage || 0} por ciento`}
                              >
                                <span className="text-slate-600 text-xs flex-1 pr-2">
                                  {idx + 1}. {val.diagnosis || 'Diagnóstico no especificado'}
                                </span>
                                <span className="font-bold text-indigo-600 whitespace-nowrap">{val.percentage || 0}%</span>
                              </div>
                            ))}
                            <div className="pt-2 border-t-2 border-indigo-300 mt-2">
                              <div className="flex items-center justify-between">
                                <span className="font-semibold text-indigo-800">
                                  <AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip> Total:
                                </span>
                                <span 
                                  className="text-xl font-bold text-indigo-600"
                                  aria-label={`Baremo de deficiencia global de la persona total: ${finalValuation.bdgp_percentage || 0} por ciento`}
                                >
                                  {finalValuation.bdgp_percentage || 0}%
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <div className="bg-white p-4 rounded-lg border border-indigo-200">
                          <p className="text-xs font-semibold text-indigo-700 uppercase mb-3">
                            Baremos Complementarios
                          </p>
                          <div className="space-y-2 text-sm">
                            <div className="flex items-center justify-between">
                              <span className="text-slate-600">
                                <AccessibleTooltip acronym="BLA">BLA</AccessibleTooltip> (<AccessibleTooltip acronym="BLA">Anexo IV</AccessibleTooltip>):
                              </span>
                              <span className="font-bold text-indigo-600" aria-label={`Baremo de limitaciones en la actividad: ${finalValuation.bla_score || 0} puntos`}>
                                {finalValuation.bla_score || 0} pts
                              </span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span className="text-slate-600">
                                <AccessibleTooltip acronym="BRP">BRP</AccessibleTooltip> (<AccessibleTooltip acronym="BRP">Anexo V</AccessibleTooltip>):
                              </span>
                              <span className="font-bold text-indigo-600" aria-label={`Baremo de restricciones en la participación: ${finalValuation.brp_score || 0} puntos`}>
                                {finalValuation.brp_score || 0} pts
                              </span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span className="text-slate-600">
                                <AccessibleTooltip acronym="BFCA">BFCA</AccessibleTooltip> (<AccessibleTooltip acronym="BFCA">Anexo VI</AccessibleTooltip>):
                              </span>
                              <span className="font-bold text-indigo-600" aria-label={`Baremo de factores contextuales y barreras ambientales: ${finalValuation.bfca_score || 0} puntos`}>
                                {finalValuation.bfca_score || 0} pts
                              </span>
                            </div>
                            {finalValuation.via && (
                              <div className="pt-2 border-t border-slate-200 mt-2">
                                <div className="flex items-center justify-between text-xs text-slate-500">
                                  <span>
                                    <AccessibleTooltip acronym="VIA">VIA</AccessibleTooltip> (Valor Inicial Ajuste):
                                  </span>
                                  <span aria-label={`Valor inicial de ajuste: ${finalValuation.via} por ciento`}>{finalValuation.via}%</span>
                                </div>
                                {finalValuation.adjustment > 0 && (
                                  <div className="flex items-center justify-between text-xs text-slate-500">
                                    <span>Ajuste (BLA/BRP):</span>
                                    <span>+{finalValuation.adjustment}%</span>
                                  </div>
                                )}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      {/* Fórmula final */}
                      <div className="bg-white p-4 rounded-lg border-2 border-indigo-300">
                        <p className="text-xs font-semibold text-indigo-800 uppercase mb-2">
                          Fórmula de Cálculo (Art. 4.2 RD 888/2022)
                        </p>
                        <div className="flex items-center justify-center gap-2 text-sm font-mono bg-slate-50 p-3 rounded border border-slate-200" role="math" aria-label="Fórmula de cálculo del grado de discapacidad ajustado">
                          <span className="text-slate-600"><AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip>:</span>
                          <span className="font-bold text-indigo-600" aria-label={`Baremo de deficiencia global de la persona: ${finalValuation.bdgp_percentage || 0} por ciento`}>{finalValuation.bdgp_percentage || 0}%</span>
                          {finalValuation.via && (
                            <>
                              <span className="text-slate-600" aria-hidden="true">→</span>
                              <span className="text-slate-600"><AccessibleTooltip acronym="VIA">VIA</AccessibleTooltip>:</span>
                              <span className="font-bold text-indigo-600" aria-label={`Valor inicial de ajuste: ${finalValuation.via} por ciento`}>{finalValuation.via}%</span>
                              {finalValuation.adjustment > 0 && (
                                <>
                                  <span className="text-slate-600" aria-hidden="true">+</span>
                                  <span className="text-slate-600">Ajuste:</span>
                                  <span className="font-bold text-indigo-600" aria-label={`Ajuste por baremos complementarios: más ${finalValuation.adjustment} por ciento`}>+{finalValuation.adjustment}%</span>
                                </>
                              )}
                            </>
                          )}
                          {finalValuation.bfca_score > 0 && (
                            <>
                              <span className="text-slate-600" aria-hidden="true">+</span>
                              <span className="text-slate-600"><AccessibleTooltip acronym="BFCA">BFCA</AccessibleTooltip>:</span>
                              <span className="font-bold text-indigo-600" aria-label={`Baremo de factores contextuales y barreras ambientales: más ${finalValuation.bfca_score} puntos`}>+{finalValuation.bfca_score} pts</span>
                            </>
                          )}
                          <span className="text-slate-600" aria-hidden="true">=</span>
                          <span className="text-2xl font-bold text-indigo-700" aria-label={`Grado de discapacidad ajustado final: ${finalValuation.gda_percentage || finalValuation.total_percentage || 0} por ciento`}>
                            {finalValuation.gda_percentage || finalValuation.total_percentage || 0}%
                          </span>
                        </div>
                        {finalValuation.formula && (
                          <p className="text-xs text-slate-500 mt-2 text-center italic">
                            {finalValuation.formula}
                          </p>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            )}

            {/* Valoración Final (GDA) */}
            {finalValuation && (finalValuation.gda_percentage !== undefined || finalValuation.total_percentage !== undefined) && (
              <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Scale className="w-6 h-6 text-blue-700" />
                      <h3 className="text-xl font-bold text-slate-900">
                        Grado de Discapacidad Ajustado (<AccessibleTooltip acronym="GDA">GDA</AccessibleTooltip>)
                      </h3>
                    </div>
                    <Badge type="success" className="bg-blue-100 text-blue-800 border-blue-300" title="Artículo 4.2 del Real Decreto 888/2022" ariaLabel="Artículo 4.2 del Real Decreto 888/2022">
                      Art. 4.2 RD 888/2022
                    </Badge>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="bg-white rounded-lg p-4 border border-slate-200 shadow-sm">
                      <p className="text-slate-600 text-xs uppercase mb-1 font-semibold">GDA Final</p>
                      <p className="text-4xl font-bold text-blue-700">{finalValuation.gda_percentage || finalValuation.total_percentage || 0}%</p>
                      {finalValuation.bdgp_percentage && (
                        <p className="text-slate-600 text-xs mt-1">
                          <AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip>: {finalValuation.bdgp_percentage}%
                        </p>
                      )}
                    </div>
                    <div className="bg-white rounded-lg p-4 border border-slate-200 shadow-sm">
                      <p className="text-slate-600 text-xs uppercase mb-1 font-semibold">Clase</p>
                      <p className="text-2xl font-bold text-blue-700">Clase {finalValuation.final_class || 'N/A'}</p>
                      <p className="text-slate-700 text-sm mt-1">{finalValuation.description || 'Deficiencia'}</p>
                    </div>
                    <div className="bg-white rounded-lg p-4 border border-slate-200 shadow-sm">
                      <p className="text-slate-600 text-xs uppercase mb-1 font-semibold">Componentes</p>
                      <p className="text-2xl font-bold text-blue-700">{finalValuation.components_count || 0}</p>
                      <p className="text-slate-700 text-sm mt-1">deficiencia(s)</p>
                    </div>
                  </div>
                  
                  {/* Lista detallada de deficiencias */}
                  {chapterValuations && chapterValuations.length > 0 && (
                    <div className="bg-white rounded-lg p-4 border border-slate-200 shadow-sm mt-4">
                      <p className="text-slate-800 text-sm font-semibold mb-3">Deficiencias valoradas ({chapterValuations.length}):</p>
                      <div className="space-y-2 max-h-64 overflow-y-auto">
                        {chapterValuations.map((val, i) => (
                          <button
                            key={i}
                            onClick={() => {
                              if (val.text_position && val.text_position.start !== null && val.text_position.end !== null) {
                                handleHighlightText(val.text_position.start, val.text_position.end, val.diagnosis)
                              }
                            }}
                            className="w-full text-left bg-slate-50 hover:bg-blue-50 rounded-lg p-3 transition-colors border border-slate-200 hover:border-blue-300"
                            title={val.text_position ? "Clic para ver en el documento" : "Posición no disponible"}
                          >
                            <div className="flex items-start justify-between gap-2">
                              <div className="flex-1">
                                <p className="text-slate-900 text-sm font-medium mb-1">
                                  {i + 1}. {val.diagnosis || 'Diagnóstico no especificado'}
                                </p>
                                <div className="flex items-center gap-2 text-xs text-slate-600">
                                  <span>{val.chapter || val.chapter_number || 'N/A'}</span>
                                  <span>•</span>
                                  <Badge type="info" className="bg-blue-100 text-blue-800 border-blue-300 text-xs">
                                    Clase {val.class || val.class_number || 'N/A'}
                                  </Badge>
                                  <span>•</span>
                                  <span className="font-bold text-blue-700">{val.percentage || 0}%</span>
                                </div>
                              </div>
                              {val.text_position && val.text_position.start !== null && (
                                <FileText className="w-4 h-4 text-slate-400 flex-shrink-0 mt-1" />
                              )}
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {/* Desglose de baremos */}
                  {(finalValuation.bla_score > 0 || finalValuation.brp_score > 0 || finalValuation.bfca_score > 0) && (
                    <div className="bg-white rounded-lg p-3 border border-slate-200 shadow-sm mb-3">
                      <p className="text-slate-800 text-xs font-semibold mb-2">Desglose de Baremos:</p>
                      <div className="grid grid-cols-3 gap-2 text-xs">
                        {finalValuation.bla_score > 0 && (
                          <div>
                            <span className="text-slate-600">
                              <AccessibleTooltip acronym="BLA">BLA</AccessibleTooltip> (<AccessibleTooltip acronym="BLA">Anexo IV</AccessibleTooltip>):
                            </span>
                            <span className="text-slate-900 font-bold ml-1">{finalValuation.bla_score}</span>
                          </div>
                        )}
                        {finalValuation.brp_score > 0 && (
                          <div>
                            <span className="text-slate-600">
                              <AccessibleTooltip acronym="BRP">BRP</AccessibleTooltip> (<AccessibleTooltip acronym="BRP">Anexo V</AccessibleTooltip>):
                            </span>
                            <span className="text-slate-900 font-bold ml-1">{finalValuation.brp_score}</span>
                          </div>
                        )}
                        {finalValuation.bfca_score > 0 && (
                          <div>
                            <span className="text-slate-600">
                              <AccessibleTooltip acronym="BFCA">BFCA</AccessibleTooltip> (<AccessibleTooltip acronym="BFCA">Anexo VI</AccessibleTooltip>):
                            </span>
                            <span className="text-slate-900 font-bold ml-1">{finalValuation.bfca_score}/24</span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                  
                  <div className="bg-white rounded-lg p-3 border border-slate-200 shadow-sm">
                    <p className="text-slate-800 text-xs">
                      <span className="font-semibold">Cálculo (Art. 4.2):</span>
                    </p>
                    <p className="text-slate-700 text-xs mt-1" aria-label="Fórmula de cálculo del grado de discapacidad ajustado">
                      {finalValuation.formula || (
                        <>
                          <AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip> + <AccessibleTooltip acronym="BLA">BLA</AccessibleTooltip> + <AccessibleTooltip acronym="BRP">BRP</AccessibleTooltip> + <AccessibleTooltip acronym="BFCA">BFCA</AccessibleTooltip> = <AccessibleTooltip acronym="GDA">GDA</AccessibleTooltip>
                        </>
                      )}
                    </p>
                    {finalValuation.legal_basis && (
                      <p className="text-slate-600 text-xs mt-1 italic">
                        {finalValuation.legal_basis}
                      </p>
                    )}
                  </div>
                  
                  {/* Botón para generar informe */}
                  <button
                    onClick={async () => {
                      // Enviar todos los análisis disponibles para comparación
                      const allAnalyses = {
                        clinical: clinicalData,
                        judicial: judicialData,
                        administrative: administrativeData
                      }
                      
                      // Verificar que hay al menos un análisis
                      if (clinicalData || judicialData || administrativeData) {
                        setLoading(true)
                        try {
                          const response = await fetch('/api/generate/report', {
                            method: 'POST',
                            headers: {
                              'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(allAnalyses)
                          })
                          
                          if (!response.ok) {
                            // Manejar respuesta de error del servidor
                            let errorMessage = 'Error al generar el informe'
                            try {
                              const errorData = await response.json()
                              errorMessage = errorData.detail || errorData.message || errorMessage
                            } catch (e) {
                              errorMessage = `Error del servidor: ${response.status} ${response.statusText}`
                            }
                            alert(`Error: ${errorMessage}`)
                            setLoading(false)
                            return
                          }
                          
                          const data = await response.json()
                          if (data && data.report) {
                            setReport(data.report)
                            setShowReport(true)
                            setTimeout(() => {
                              const reportViewer = document.getElementById('report-viewer')
                              if (reportViewer) {
                                reportViewer.scrollIntoView({ behavior: 'smooth', block: 'start' })
                              }
                            }, 100)
                          } else {
                            alert('Error: El servidor no devolvió el informe correctamente')
                          }
                        } catch (err) {
                          console.error('Error generando informe:', err)
                          alert(`Error al generar el informe: ${err.message || 'Error desconocido'}`)
                        } finally {
                          setLoading(false)
                        }
                      } else {
                        alert('No hay documentos analizados para generar el informe')
                      }
                    }}
                    className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 shadow-md"
                  >
                    <FileText className="w-4 h-4" />
                    Generar Informe Legal Completo
                  </button>
                </div>
              </Card>
            )}

            {/* Incongruencias */}
            {inconsistencies && inconsistencies.total_count > 0 && (
              <Card>
                <div className="bg-red-50 p-4 border-b border-red-100 font-semibold text-red-800 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5" /> Incongruencias Detectadas (RD 888/2022)
                </div>
                <div className="divide-y divide-slate-100">
                  {inconsistencies.inconsistencies.map((inc, i) => (
                    <div key={i} className="p-5 hover:bg-slate-50 transition-colors">
                      <div className="flex justify-between items-start mb-2">
                        <h5 className="font-bold text-slate-800">{inc.type}</h5>
                        <Badge type={inc.severity}>
                          {inc.severity === 'critical' ? 'CRÍTICO' : inc.severity === 'high' ? 'GRAVE' : inc.severity === 'medium' ? 'MEDIO' : 'BAJO'}
                        </Badge>
                      </div>
                      <p className="text-sm text-slate-600 leading-relaxed mb-2">{inc.description}</p>
                      <p className="text-xs text-slate-500 italic">{inc.recommendation}</p>
                    </div>
                  ))}
                </div>
                
                {/* Comparación de metodologías */}
                {(analyses.clinical || analyses.judicial) && analyses.administrative && (
                  <div className="p-4 bg-blue-50 border-t border-blue-100">
                    <h4 className="font-semibold text-blue-900 mb-3 flex items-center gap-2">
                      <Scale className="w-4 h-4" />
                      Comparación de Metodologías
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm mb-4">
                      <div className="bg-white p-3 rounded border border-blue-200">
                        <p className="font-semibold text-blue-800 mb-2">Administración</p>
                        <ul className="space-y-1 text-blue-700 text-xs">
                          <li>• Diagnóstico: Genérico</li>
                          <li>• Metodología: Valoración única</li>
                          <li>• Baremo: Solo Anexo III</li>
                          <li>• Resultado: Porcentaje bajo (Clase 1)</li>
                        </ul>
                      </div>
                      <div className="bg-white p-3 rounded border border-emerald-200">
                        <p className="font-semibold text-emerald-800 mb-2">Nuestro Sistema</p>
                        <ul className="space-y-1 text-emerald-700 text-xs">
                          <li>• Diagnósticos: {((analyses.clinical || analyses.judicial)?.legal_analysis?.chapter_valuations?.length || 0)} específicos</li>
                          <li>• Metodología: Fórmula combinación</li>
                          <li>• Baremos: BDGP + BLA + BRP + BFCA</li>
                          <li>• Resultado: {((analyses.clinical || analyses.judicial)?.legal_analysis?.final_valuation?.gda_percentage || 0)}% (Clase {((analyses.clinical || analyses.judicial)?.legal_analysis?.final_valuation?.final_class || 'N/A')})</li>
                        </ul>
                      </div>
                    </div>
                    <div className="bg-amber-50 p-3 rounded border border-amber-200 text-xs text-amber-800">
                      <p className="font-semibold mb-1">💡 Cómo verificar la valoración administrativa:</p>
                      <p>Revisa en la resolución las secciones "Fundamentos" y "Dispositivo" para verificar:</p>
                      <ul className="list-disc list-inside mt-1 space-y-0.5">
                        <li>¿Qué diagnóstico reconoce? (debe ser específico, no genérico)</li>
                        <li>¿Aplica fórmula de combinación para múltiples deficiencias?</li>
                        <li>¿Menciona los baremos BLA, BRP, BFCA según Art. 4.2?</li>
                      </ul>
                    </div>
                  </div>
                )}
                
                {/* Botón para generar informe de inconsistencia */}
                {(analyses.clinical || analyses.judicial) && analyses.administrative && (
                  <div className="p-4 bg-red-50 border-t border-red-100">
                    <button
                      onClick={handleGenerateInconsistencyReport}
                      disabled={loading}
                      className="w-full bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                    >
                      <FileText className="w-4 h-4" />
                      {loading ? 'Generando...' : 'Generar Informe de Inconsistencia Completo'}
                    </button>
                  </div>
                )}
              </Card>
            )}

            {/* Botón para verificar incongruencias */}
            {Object.values(analyses).filter(a => a !== null).length >= 2 && !inconsistencies && (
              <div className="text-center">
                <button
                  onClick={handleCheckInconsistencies}
                  disabled={loading}
                  className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 mx-auto"
                >
                  {loading ? 'Analizando...' : 'Verificar Incongruencias'}
                  <AlertTriangle className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>

          {/* Columna derecha: Predicción */}
          <div className="lg:col-span-1 space-y-6">
            {/* Mostrar valoración final si existe, sino mostrar la clasificación predicha */}
            {finalValuation && (finalValuation.gda_percentage !== undefined || finalValuation.total_percentage !== undefined) ? (
              <Card className="bg-gradient-to-br from-indigo-50 to-blue-50 border-2 border-indigo-200 shadow-md">
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-4 text-indigo-700">
                    <BarChart3 className="w-5 h-5" />
                    <span className="font-bold tracking-wide text-sm uppercase">Valoración Correcta</span>
                  </div>

                  <div className="mb-6">
                    <div className="text-slate-700 text-sm mb-1 font-semibold">
                      Grado de Discapacidad Ajustado (<AccessibleTooltip acronym="GDA">GDA</AccessibleTooltip>)
                    </div>
                    <div className="text-5xl font-bold text-indigo-700 tracking-tight" aria-label={`Grado de discapacidad ajustado: ${finalValuation.gda_percentage || finalValuation.total_percentage || 0} por ciento`}>
                      {finalValuation.gda_percentage || finalValuation.total_percentage || 0}%
                    </div>
                    {finalValuation.bdgp_percentage && (
                      <div className="text-slate-600 text-xs mt-1 font-medium">
                        <AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip> (<AccessibleTooltip acronym="BDGP">Anexo III</AccessibleTooltip>): {finalValuation.bdgp_percentage}%
                        {finalValuation.bfca_score > 0 && (
                          <span> + <AccessibleTooltip acronym="BFCA">BFCA</AccessibleTooltip>: {finalValuation.bfca_score} pts</span>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-slate-700 font-semibold">Certeza Jurídica</span>
                        <span className="text-emerald-600 font-bold text-base">
                          {chapterValuations.length > 0 ? Math.min(95, 70 + (chapterValuations.length * 5)) : 70}%
                        </span>
                      </div>
                      <div className="w-full bg-slate-200 rounded-full h-3 shadow-inner">
                        <div
                          className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-3 rounded-full shadow-sm"
                          style={{ width: `${Math.min(95, 70 + (chapterValuations.length * 5))}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="bg-white p-4 rounded-lg border-2 border-indigo-200 shadow-sm">
                      <div className="text-sm text-slate-700 leading-relaxed">
                        <span className="font-bold text-indigo-700 block mb-2">Fundamentación Técnica:</span>
                        <span className="text-slate-600">{finalValuation.formula || 'RD 888/2022 - Valoración final por suma de deficiencias'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ) : (chapterValuations && chapterValuations.length > 0) ? (
              // Si hay valoraciones por capítulo pero no final_valuation, mostrar la suma
              <Card className="bg-gradient-to-br from-indigo-50 to-blue-50 border-2 border-indigo-200 shadow-md">
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-4 text-indigo-700">
                    <BarChart3 className="w-5 h-5" />
                    <span className="font-bold tracking-wide text-sm uppercase">Valoración Correcta</span>
                  </div>

                  <div className="mb-6">
                    <div className="text-slate-700 text-sm mb-1 font-semibold">
                      Grado de Discapacidad (<AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip>)
                    </div>
                    <div className="text-5xl font-bold text-indigo-700 tracking-tight">
                      {chapterValuations.reduce((sum, val) => sum + (val.percentage || 0), 0).toFixed(1)}%
                    </div>
                    <div className="text-slate-600 text-xs mt-1 font-medium">
                      Basado en {chapterValuations.length} deficiencia(s) detectada(s)
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-slate-700 font-semibold">Certeza Jurídica</span>
                        <span className="text-emerald-600 font-bold text-base">
                          {Math.min(95, 70 + (chapterValuations.length * 5))}%
                        </span>
                      </div>
                      <div className="w-full bg-slate-200 rounded-full h-3 shadow-inner">
                        <div
                          className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-3 rounded-full shadow-sm"
                          style={{ width: `${Math.min(95, 70 + (chapterValuations.length * 5))}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="bg-white p-4 rounded-lg border-2 border-indigo-200 shadow-sm">
                      <div className="text-sm text-slate-700 leading-relaxed">
                        <span className="font-bold text-indigo-700 block mb-2">Fundamentación Técnica:</span>
                        <span className="text-slate-600">RD 888/2022 - Valoración basada en hechos probados (métricas funcionales)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ) : predictedClassification && predictedClassification.suggested_percentage ? (
              <Card className="bg-gradient-to-br from-indigo-50 to-blue-50 border-2 border-indigo-200 shadow-md">
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-4 text-indigo-700">
                    <BarChart3 className="w-5 h-5" />
                    <span className="font-bold tracking-wide text-sm uppercase">Valoración Correcta</span>
                  </div>

                  <div className="mb-6">
                    <p className="text-slate-700 text-sm mb-1 font-semibold">Grado Estimado IA</p>
                    <div className="text-5xl font-bold text-indigo-700 tracking-tight">
                      {predictedClassification.suggested_percentage || 'N/A'}%
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-slate-700 font-semibold">Certeza Jurídica</span>
                        <span className="text-emerald-600 font-bold text-base">
                          {Math.round((predictedClassification.confidence || 0.7) * 100)}%
                        </span>
                      </div>
                      <div className="w-full bg-slate-200 rounded-full h-3 shadow-inner">
                        <div
                          className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-3 rounded-full shadow-sm"
                          style={{ width: `${(predictedClassification.confidence || 0.7) * 100}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="bg-white p-4 rounded-lg border-2 border-indigo-200 shadow-sm">
                      <p className="text-sm text-slate-700 leading-relaxed">
                        <span className="font-bold text-indigo-700 block mb-2">Fundamentación Técnica:</span>
                        <span className="text-slate-600">{predictedClassification.legal_basis || 'Basado en RD 888/2022'}</span>
                      </p>
                    </div>
                  </div>
                </div>
              </Card>
            ) : null}

            <Card className="p-5 bg-blue-50 border-blue-100">
              <h4 className="font-bold text-blue-900 mb-3 text-sm uppercase">Legislación Aplicable</h4>
              <ul className="space-y-2 text-sm text-blue-800">
                <li className="flex items-start gap-2">
                  <BookOpen className="w-4 h-4 mt-0.5 flex-shrink-0" />
                  <span>RD 888/2022, Art. 3 y 4 - Baremos I a VI</span>
                </li>
                <li className="flex items-start gap-2">
                  <BookOpen className="w-4 h-4 mt-0.5 flex-shrink-0" aria-hidden="true" />
                  <span>Anexo III: <AccessibleTooltip acronym="BDGP">BDGP</AccessibleTooltip> (Baremo Deficiencia Global Persona)</span>
                </li>
                <li className="flex items-start gap-2">
                  <BookOpen className="w-4 h-4 mt-0.5 flex-shrink-0" aria-hidden="true" />
                  <span>Anexo IV: <AccessibleTooltip acronym="BLA">BLA</AccessibleTooltip> (Baremo Limitaciones Actividad)</span>
                </li>
                <li className="flex items-start gap-2">
                  <BookOpen className="w-4 h-4 mt-0.5 flex-shrink-0" aria-hidden="true" />
                  <span>Anexo V: <AccessibleTooltip acronym="BRP">BRP</AccessibleTooltip> (Baremo Restricciones Participación)</span>
                </li>
                <li className="flex items-start gap-2">
                  <BookOpen className="w-4 h-4 mt-0.5 flex-shrink-0" aria-hidden="true" />
                  <span>Anexo VI: <AccessibleTooltip acronym="BFCA">BFCA</AccessibleTooltip> (Baremo Factores Contextuales) - máx. 24 pts</span>
                </li>
              </ul>
            </Card>
          </div>
        </div>
        
        {/* Visor de Documento con Resaltado */}
        {showDocumentViewer && (clinicalData || judicialData || administrativeData) && (
          <Card className="mt-6">
            <div className="bg-slate-50 p-4 border-b border-slate-200 font-semibold text-slate-700 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                <span>Visor de Documento</span>
                {highlightedRange && (
                  <Badge type="info" className="ml-2">
                    {highlightedRange.diagnosis}
                  </Badge>
                )}
              </div>
              <button
                onClick={() => {
                  setShowDocumentViewer(false)
                  setHighlightedRange(null)
                }}
                className="text-slate-500 hover:text-slate-700 text-sm"
              >
                Cerrar
              </button>
            </div>
            <div id="document-viewer" className="p-6 max-h-96 overflow-y-auto bg-slate-50">
              {(() => {
                const currentData = clinicalData || judicialData || adminData
                const text = currentData?.extracted_text || ''
                
                if (!text) {
                  return <p className="text-slate-500">Texto del documento no disponible</p>
                }
                
                if (highlightedRange && highlightedRange.start !== null && highlightedRange.end !== null) {
                  const before = text.substring(0, highlightedRange.start)
                  const highlighted = text.substring(highlightedRange.start, highlightedRange.end)
                  const after = text.substring(highlightedRange.end)
                  
                  return (
                    <div className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                      <span>{before}</span>
                      <mark className="bg-yellow-300 text-slate-900 font-semibold px-1 rounded">
                        {highlighted}
                      </mark>
                      <span>{after}</span>
                    </div>
                  )
                }
                
                return (
                  <div className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                    {text}
                  </div>
                )
              })()}
            </div>
          </Card>
        )}
        
        {/* Visor de Informe Legal */}
        {showReport && report && (() => {
          const currentData = clinicalData || judicialData || administrativeData
          const filename = currentData?.filename || 'documento'
          const cleanFilename = filename.replace(/\.[^/.]+$/, '').replace(/[^a-z0-9]/gi, '_').toLowerCase()
          const dateStr = new Date().toISOString().split('T')[0]
          
          return (
            <Card className="mt-6" id="report-viewer">
              <div className="bg-blue-50 p-4 border-b border-blue-100 font-semibold text-blue-800 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  <span>Informe Legal Completo (RD 888/2022)</span>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => {
                      const blob = new Blob([report], { type: 'text/plain;charset=utf-8' })
                      const url = URL.createObjectURL(blob)
                      const a = document.createElement('a')
                      a.href = url
                      a.download = `informe_legal_${cleanFilename}_${dateStr}.txt`
                      document.body.appendChild(a)
                      a.click()
                      document.body.removeChild(a)
                      URL.revokeObjectURL(url)
                    }}
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Descargar
                  </button>
                  <button
                    onClick={() => {
                      setShowReport(false)
                      setReport(null)
                    }}
                    className="text-slate-500 hover:text-slate-700 text-sm"
                  >
                    Cerrar
                  </button>
                </div>
              </div>
              <div className="p-6 max-h-[600px] overflow-y-auto bg-white">
                <div className="prose prose-sm max-w-none">
                  <pre className="text-xs text-slate-700 leading-relaxed whitespace-pre-wrap font-mono bg-slate-50 p-4 rounded-lg border border-slate-200">
                    {report}
                  </pre>
                </div>
              </div>
            </Card>
          )
        })()}
        
        {/* Visor de Informe de Inconsistencia */}
        {showInconsistencyReport && inconsistencyReport && (
          <Card className="mt-6" id="inconsistency-report-viewer">
            <div className="bg-red-50 p-4 border-b border-red-100 font-semibold text-red-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                <span>Informe de Inconsistencia: Resolución vs Pericial</span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    const blob = new Blob([inconsistencyReport], { type: 'text/plain;charset=utf-8' })
                    const url = URL.createObjectURL(blob)
                    const a = document.createElement('a')
                    a.href = url
                    a.download = `informe_inconsistencia_${new Date().toISOString().split('T')[0]}.txt`
                    document.body.appendChild(a)
                    a.click()
                    document.body.removeChild(a)
                    URL.revokeObjectURL(url)
                  }}
                  className="text-red-600 hover:text-red-800 text-sm font-medium"
                >
                  Descargar
                </button>
                <button
                  onClick={() => {
                    setShowInconsistencyReport(false)
                    setInconsistencyReport(null)
                  }}
                  className="text-slate-500 hover:text-slate-700 text-sm"
                >
                  Cerrar
                </button>
              </div>
            </div>
            <div className="p-6 max-h-[600px] overflow-y-auto bg-white">
              <pre className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap font-sans">
                {inconsistencyReport}
              </pre>
            </div>
          </Card>
        )}
      </div>
    )
  }, [analyses, inconsistencies, step, loading, showDocumentViewer, highlightedRange, report, showReport, inconsistencyReport, showInconsistencyReport, setStep, setAnalyses, setInconsistencies, setLoading, handleAnalysisComplete, handleCheckInconsistencies, handleGenerateInconsistencyReport, handleHighlightText, setShowDocumentViewer, setHighlightedRange, setReport, setShowReport, setShowInconsistencyReport, setInconsistencyReport])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {step === 'upload' && renderUploadJsx}
      {step === 'analyzing' && renderAnalyzingJsx}
      {step === 'results' && renderResultsJsx}
    </div>
  )
}

export default App
