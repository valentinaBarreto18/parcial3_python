"""
API Gateway
Enruta las peticiones a los microservicios correspondientes
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI(title="API Gateway - Recetario Familiar", version="1.0.0")

# URLs de los microservicios
RECETAS_SERVICE_URL = os.getenv("RECETAS_SERVICE_URL", "http://localhost:8001")
INGREDIENTES_SERVICE_URL = os.getenv("INGREDIENTES_SERVICE_URL", "http://localhost:8002")

@app.get("/")
def root():
    """Endpoint raíz con información del API Gateway"""
    return {
        "mensaje": "API Gateway - Recetario de Cocina Familiar",
        "version": "1.0.0",
        "servicios": {
            "recetas": f"{RECETAS_SERVICE_URL}",
            "ingredientes": f"{INGREDIENTES_SERVICE_URL}"
        },
        "endpoints": {
            "recetas": "/api/recetas",
            "ingredientes": "/api/ingredientes"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar el estado de todos los servicios"""
    services_status = {}
    
    # Verificar servicio de recetas
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{RECETAS_SERVICE_URL}/health", timeout=5.0)
            services_status["recetas"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        services_status["recetas"] = f"unhealthy: {str(e)}"
    
    # Verificar servicio de ingredientes
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{INGREDIENTES_SERVICE_URL}/health", timeout=5.0)
            services_status["ingredientes"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        services_status["ingredientes"] = f"unhealthy: {str(e)}"
    
    all_healthy = all(status == "healthy" for status in services_status.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "services": services_status
    }

@app.api_route("/api/recetas/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_recetas(path: str, request: Request):
    """Proxy para el microservicio de recetas"""
    url = f"{RECETAS_SERVICE_URL}/recetas/{path}" if path else f"{RECETAS_SERVICE_URL}/recetas"
    return await forward_request(url, request)

@app.api_route("/api/ingredientes/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_ingredientes(path: str, request: Request):
    """Proxy para el microservicio de ingredientes"""
    url = f"{INGREDIENTES_SERVICE_URL}/ingredientes/{path}" if path else f"{INGREDIENTES_SERVICE_URL}/ingredientes"
    return await forward_request(url, request)

async def forward_request(url: str, request: Request):
    """Función auxiliar para reenviar peticiones a los microservicios"""
    try:
        async with httpx.AsyncClient() as client:
            # Obtener el body de la petición si existe
            body = await request.body()
            
            # Preparar headers
            headers = dict(request.headers)
            headers.pop("host", None)  # Remover el header host
            
            # Hacer la petición al microservicio
            response = await client.request(
                method=request.method,
                url=url,
                content=body,
                headers=headers,
                params=request.query_params,
                timeout=30.0
            )
            
            # Retornar la respuesta del microservicio
            return JSONResponse(
                content=response.json() if response.content else {},
                status_code=response.status_code
            )
    
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503, 
            detail="Servicio no disponible. Verifique que el microservicio esté en ejecución."
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504, 
            detail="Tiempo de espera agotado al conectar con el servicio."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al procesar la solicitud: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
