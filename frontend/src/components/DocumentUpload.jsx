import React, { useState, useEffect } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

export const DocumentUpload = ({
  type,
  label,
  autoAnalyze,
  file,
  analysis,
  onFileChange,
  onAnalysisStart,
  onAnalysisComplete
}) => {
  const [loading, setLoading] = useState(false)
  const [hasAnalysis, setHasAnalysis] = useState(false)

  // Efecto para manejar auto-análisis
  useEffect(() => {
    if (autoAnalyze && file && !analysis && !loading) {
      handleAnalyze()
    }
  }, [autoAnalyze, file, analysis, loading])

  // Actualizar estado cuando hay análisis
  useEffect(() => {
    if (analysis) {
      setHasAnalysis(true)
      setLoading(false)
    }
  }, [analysis])

  const handleFileSelect = async (e) => {
    const selectedFile = e.target.files[0]
    if (!selectedFile) return

    // Validar tipo de archivo
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!allowedTypes.includes(selectedFile.type)) {
      alert('Por favor, selecciona un archivo PDF, DOC o DOCX')
      return
    }

    // Validar tamaño (máximo 10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      alert('El archivo es demasiado grande. Máximo 10MB')
      return
    }

    if (onFileChange) {
      onFileChange(selectedFile)
    }
  }

  const handleAnalyze = async () => {
    if (!file) return

    setLoading(true)
    if (onAnalysisStart) {
      onAnalysisStart(type)
    }

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('document_type', type)

      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Error al analizar el documento')
      }

      const data = await response.json()

      if (onAnalysisComplete) {
        onAnalysisComplete(type, data)
      }

      setHasAnalysis(true)
    } catch (error) {
      console.error('Error analizando documento:', error)
      alert('Error al analizar el documento. Por favor, intenta de nuevo.')
    } finally {
      setLoading(false)
      if (onAnalysisStart) {
        onAnalysisStart(null) // Indicar que el análisis terminó
      }
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-slate-200 hover:shadow-lg transition-shadow">
      <div className="text-center mb-4">
        <h3 className="font-semibold text-slate-800 mb-2">{label}</h3>
        
        {file ? (
          <div className="space-y-2">
            <FileText className="w-8 h-8 text-blue-600 mx-auto" />
            <p className="text-sm text-slate-600 truncate" title={file.name}>
              {file.name}
            </p>
            {analysis && (
              <div className="flex items-center justify-center gap-2 text-green-600 text-sm">
                <CheckCircle className="w-4 h-4" />
                <span>Analizado</span>
              </div>
            )}
            {loading && (
              <div className="flex items-center justify-center gap-2 text-blue-600 text-sm">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Analizando...</span>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
              <Upload className="w-8 h-8 text-blue-600" />
            </div>
            <label className="cursor-pointer">
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileSelect}
                className="hidden"
              />
              <span className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors inline-block">
                Seleccionar archivo
              </span>
            </label>
            <p className="text-xs text-slate-500">PDF, DOC, DOCX</p>
          </div>
        )}
      </div>

      {file && !analysis && !loading && (
        <div className="mt-4 text-center">
          <button
            onClick={handleAnalyze}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors w-full"
          >
            Analizar Documento
          </button>
        </div>
      )}

      {analysis && (
        <div className="mt-4 pt-4 border-t border-slate-200">
          <div className="text-xs text-slate-500 space-y-1">
            <p className="font-semibold text-slate-700">Análisis completado</p>
            {analysis.legal_analysis && (
              <p className="text-green-600">✓ Análisis legal disponible</p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
