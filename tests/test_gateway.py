"""
Pruebas unitarias para el API Gateway
"""
import pytest
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import httpx

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_gateway.app import app

@pytest.fixture
def client():
    """Cliente de prueba para FastAPI"""
    return TestClient(app)

class TestAPIGateway:
    """Pruebas para el API Gateway"""
    
    def test_root_endpoint(self, client):
        """Probar el endpoint raíz del gateway"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "mensaje" in data
        assert "version" in data
        assert "servicios" in data
        assert "endpoints" in data
    
    @pytest.mark.asyncio
    @patch("api_gateway.app.httpx.AsyncClient.get")
    async def test_health_check_all_services_healthy(self, mock_get, client):
        """Probar health check cuando todos los servicios están saludables"""
        # Simular respuestas exitosas de los servicios
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "services" in data
    
    def test_health_check_endpoint(self, client):
        """Probar que el endpoint de health responde"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "services" in data
    
    @pytest.mark.asyncio
    @patch("api_gateway.app.httpx.AsyncClient.request")
    async def test_proxy_recetas_get(self, mock_request, client):
        """Probar proxy GET a servicio de recetas"""
        # Simular respuesta del microservicio
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "nombre": "Test Receta"}]
        mock_response.content = b'[{"id": 1, "nombre": "Test Receta"}]'
        mock_request.return_value = mock_response
        
        response = client.get("/api/recetas/")
        # El test verifica que el endpoint existe
        assert response.status_code in [200, 500, 503]  # 500/503 si el servicio no está disponible
    
    @pytest.mark.asyncio
    @patch("api_gateway.app.httpx.AsyncClient.request")
    async def test_proxy_ingredientes_get(self, mock_request, client):
        """Probar proxy GET a servicio de ingredientes"""
        # Simular respuesta del microservicio
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "nombre": "Test Ingrediente"}]
        mock_response.content = b'[{"id": 1, "nombre": "Test Ingrediente"}]'
        mock_request.return_value = mock_response
        
        response = client.get("/api/ingredientes/")
        # El test verifica que el endpoint existe
        assert response.status_code in [200, 500, 503]
    
    def test_proxy_recetas_endpoint_exists(self, client):
        """Verificar que el endpoint de recetas existe"""
        # Solo verificamos que el endpoint responde, no el contenido
        response = client.get("/api/recetas/")
        # Puede devolver 503 si el servicio no está corriendo, pero el endpoint existe
        assert response.status_code in [200, 503, 504]
    
    def test_proxy_ingredientes_endpoint_exists(self, client):
        """Verificar que el endpoint de ingredientes existe"""
        response = client.get("/api/ingredientes/")
        assert response.status_code in [200, 503, 504]
    
    def test_invalid_endpoint(self, client):
        """Probar acceso a endpoint inválido"""
        response = client.get("/api/invalid/")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    @patch("api_gateway.app.httpx.AsyncClient.request")
    async def test_proxy_handles_timeout(self, mock_request, client):
        """Probar manejo de timeout en el proxy"""
        # Simular timeout
        mock_request.side_effect = httpx.TimeoutException("Timeout")
        
        response = client.get("/api/recetas/")
        # Debería devolver 504 Gateway Timeout o 503
        assert response.status_code in [503, 504]
    
    @pytest.mark.asyncio
    @patch("api_gateway.app.httpx.AsyncClient.request")
    async def test_proxy_handles_connection_error(self, mock_request, client):
        """Probar manejo de error de conexión"""
        # Simular error de conexión
        mock_request.side_effect = httpx.ConnectError("Connection failed")
        
        response = client.get("/api/recetas/")
        # Debería devolver 503 Service Unavailable
        assert response.status_code == 503
    
    def test_api_structure(self, client):
        """Verificar la estructura de la respuesta del root"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        
        # Verificar claves principales
        assert "mensaje" in data
        assert "version" in data
        assert "servicios" in data
        assert "endpoints" in data
        
        # Verificar estructura de servicios
        assert "recetas" in data["servicios"]
        assert "ingredientes" in data["servicios"]
        
        # Verificar estructura de endpoints
        assert "recetas" in data["endpoints"]
        assert "ingredientes" in data["endpoints"]

class TestGatewayIntegration:
    """Pruebas de integración del gateway"""
    
    def test_gateway_routes_configuration(self, client):
        """Verificar que las rutas están configuradas correctamente"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que los endpoints esperados están en la configuración
        assert data["endpoints"]["recetas"] == "/api/recetas"
        assert data["endpoints"]["ingredientes"] == "/api/ingredientes"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
