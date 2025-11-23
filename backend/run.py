#!/usr/bin/env python3
"""
Script de inicio para el servidor FastAPI
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        timeout_keep_alive=300,  # 5 minutos para archivos grandes
        limit_concurrency=10,
        limit_max_requests=100
    )

