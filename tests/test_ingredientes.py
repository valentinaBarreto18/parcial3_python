"""
Pruebas unitarias para el microservicio de Ingredientes
"""
import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from servicio_ingredientes.app import app
from database import Base, get_db

# Configurar base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_ingredientes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    """Crear y limpiar la base de datos para cada test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """Cliente de prueba para FastAPI"""
    return TestClient(app)

class TestIngredientesEndpoints:
    """Pruebas para los endpoints de ingredientes"""
    
    def test_health_check(self, client):
        """Probar que el endpoint de health funciona"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "ingredientes"
    
    def test_crear_ingrediente(self, client):
        """Probar creación de un ingrediente"""
        ingrediente_data = {
            "nombre": "Tomate",
            "unidad_medida": "gramos",
            "categoria": "vegetales"
        }
        response = client.post("/ingredientes", json=ingrediente_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Tomate"
        assert data["unidad_medida"] == "gramos"
        assert data["categoria"] == "vegetales"
        assert "id" in data
    
    def test_crear_ingrediente_duplicado(self, client):
        """Probar que no se puede crear un ingrediente duplicado"""
        ingrediente_data = {
            "nombre": "Cebolla",
            "unidad_medida": "gramos",
            "categoria": "vegetales"
        }
        # Crear primera vez
        response1 = client.post("/ingredientes", json=ingrediente_data)
        assert response1.status_code == 201
        
        # Intentar crear duplicado
        response2 = client.post("/ingredientes", json=ingrediente_data)
        assert response2.status_code == 400
        assert "ya existe" in response2.json()["detail"].lower()
    
    def test_listar_ingredientes_vacio(self, client):
        """Probar listado cuando no hay ingredientes"""
        response = client.get("/ingredientes")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_listar_ingredientes(self, client):
        """Probar listado de ingredientes"""
        # Crear algunos ingredientes
        ingredientes = [
            {"nombre": "Sal", "unidad_medida": "gramos", "categoria": "condimentos"},
            {"nombre": "Azúcar", "unidad_medida": "gramos", "categoria": "endulzantes"},
            {"nombre": "Leche", "unidad_medida": "ml", "categoria": "lácteos"}
        ]
        for ingrediente in ingredientes:
            client.post("/ingredientes", json=ingrediente)
        
        response = client.get("/ingredientes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_filtrar_ingredientes_por_categoria(self, client):
        """Probar filtrado de ingredientes por categoría"""
        # Crear ingredientes de diferentes categorías
        ingredientes = [
            {"nombre": "Queso", "unidad_medida": "gramos", "categoria": "lácteos"},
            {"nombre": "Yogurt", "unidad_medida": "gramos", "categoria": "lácteos"},
            {"nombre": "Pollo", "unidad_medida": "gramos", "categoria": "carnes"}
        ]
        for ingrediente in ingredientes:
            client.post("/ingredientes", json=ingrediente)
        
        # Filtrar por lácteos
        response = client.get("/ingredientes?categoria=lácteos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(ing["categoria"] == "lácteos" for ing in data)
    
    def test_obtener_ingrediente_por_id(self, client):
        """Probar obtención de un ingrediente específico"""
        # Crear ingrediente
        ingrediente_data = {
            "nombre": "Ajo",
            "unidad_medida": "dientes",
            "categoria": "vegetales"
        }
        create_response = client.post("/ingredientes", json=ingrediente_data)
        ingrediente_id = create_response.json()["id"]
        
        # Obtener ingrediente
        response = client.get(f"/ingredientes/{ingrediente_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Ajo"
        assert data["id"] == ingrediente_id
    
    def test_obtener_ingrediente_no_existente(self, client):
        """Probar obtener un ingrediente que no existe"""
        response = client.get("/ingredientes/999")
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"].lower()
    
    def test_actualizar_ingrediente(self, client):
        """Probar actualización de un ingrediente"""
        # Crear ingrediente
        ingrediente_data = {
            "nombre": "Pimienta",
            "unidad_medida": "gramos",
            "categoria": "especias"
        }
        create_response = client.post("/ingredientes", json=ingrediente_data)
        ingrediente_id = create_response.json()["id"]
        
        # Actualizar ingrediente
        update_data = {
            "unidad_medida": "cucharadas",
            "categoria": "condimentos"
        }
        response = client.put(f"/ingredientes/{ingrediente_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["unidad_medida"] == "cucharadas"
        assert data["categoria"] == "condimentos"
        assert data["nombre"] == "Pimienta"  # No cambió
    
    def test_actualizar_ingrediente_no_existente(self, client):
        """Probar actualizar un ingrediente que no existe"""
        update_data = {"nombre": "Nuevo Nombre"}
        response = client.put("/ingredientes/999", json=update_data)
        assert response.status_code == 404
    
    def test_eliminar_ingrediente(self, client):
        """Probar eliminación de un ingrediente"""
        # Crear ingrediente
        ingrediente_data = {
            "nombre": "Ingrediente Temporal",
            "unidad_medida": "gramos"
        }
        create_response = client.post("/ingredientes", json=ingrediente_data)
        ingrediente_id = create_response.json()["id"]
        
        # Eliminar ingrediente
        response = client.delete(f"/ingredientes/{ingrediente_id}")
        assert response.status_code == 200
        assert "eliminado" in response.json()["message"].lower()
        
        # Verificar que ya no existe
        get_response = client.get(f"/ingredientes/{ingrediente_id}")
        assert get_response.status_code == 404
    
    def test_buscar_ingrediente_por_nombre(self, client):
        """Probar búsqueda de ingredientes por nombre"""
        # Crear ingredientes
        ingredientes = [
            {"nombre": "Aceite de Oliva", "unidad_medida": "ml"},
            {"nombre": "Aceite de Girasol", "unidad_medida": "ml"},
            {"nombre": "Vinagre", "unidad_medida": "ml"}
        ]
        for ingrediente in ingredientes:
            client.post("/ingredientes", json=ingrediente)
        
        # Buscar por "Aceite"
        response = client.get("/ingredientes/buscar/Aceite")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("Aceite" in ing["nombre"] for ing in data)
    
    def test_buscar_ingrediente_sin_resultados(self, client):
        """Probar búsqueda sin resultados"""
        response = client.get("/ingredientes/buscar/NoExiste")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_crear_ingrediente_sin_categoria(self, client):
        """Probar creación de ingrediente sin categoría"""
        ingrediente_data = {
            "nombre": "Harina",
            "unidad_medida": "gramos"
        }
        response = client.post("/ingredientes", json=ingrediente_data)
        assert response.status_code == 201
        data = response.json()
        assert data["categoria"] is None
    
    def test_paginacion_ingredientes(self, client):
        """Probar paginación en el listado de ingredientes"""
        # Crear 5 ingredientes
        for i in range(5):
            ingrediente_data = {
                "nombre": f"Ingrediente {i+1}",
                "unidad_medida": "gramos"
            }
            client.post("/ingredientes", json=ingrediente_data)
        
        # Obtener primeros 2
        response = client.get("/ingredientes?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2
        
        # Obtener siguientes 2
        response = client.get("/ingredientes?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2
    
    def test_busqueda_case_insensitive(self, client):
        """Probar que la búsqueda no distingue mayúsculas/minúsculas"""
        # Crear ingrediente
        ingrediente_data = {
            "nombre": "Chocolate Negro",
            "unidad_medida": "gramos"
        }
        client.post("/ingredientes", json=ingrediente_data)
        
        # Buscar en minúsculas
        response = client.get("/ingredientes/buscar/chocolate")
        assert response.status_code == 200
        assert len(response.json()) == 1
        
        # Buscar en mayúsculas
        response = client.get("/ingredientes/buscar/CHOCOLATE")
        assert response.status_code == 200
        assert len(response.json()) == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
