"""
Pruebas unitarias para el microservicio de Recetas
"""
import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from servicio_recetas.app import app
from database import Base, get_db

# Configurar base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_recetas.db"
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

class TestRecetasEndpoints:
    """Pruebas para los endpoints de recetas"""
    
    def test_health_check(self, client):
        """Probar que el endpoint de health funciona"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "recetas"
    
    def test_crear_receta_simple(self, client):
        """Probar creación de una receta simple sin pasos ni ingredientes"""
        receta_data = {
            "nombre": "Ensalada César",
            "descripcion": "Ensalada clásica romana",
            "tiempo_preparacion": 15,
            "porciones": 4,
            "pasos": [],
            "ingredientes": []
        }
        response = client.post("/recetas", json=receta_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Ensalada César"
        assert data["tiempo_preparacion"] == 15
        assert "id" in data
    
    def test_crear_receta_con_pasos(self, client):
        """Probar creación de una receta con pasos de preparación"""
        receta_data = {
            "nombre": "Pasta Carbonara",
            "descripcion": "Pasta italiana clásica",
            "tiempo_preparacion": 20,
            "porciones": 2,
            "pasos": [
                {"numero_paso": 1, "descripcion": "Hervir agua con sal"},
                {"numero_paso": 2, "descripcion": "Cocinar la pasta"},
                {"numero_paso": 3, "descripcion": "Mezclar con salsa"}
            ],
            "ingredientes": []
        }
        response = client.post("/recetas", json=receta_data)
        assert response.status_code == 201
        data = response.json()
        assert len(data["pasos"]) == 3
        assert data["pasos"][0]["numero_paso"] == 1
    
    def test_listar_recetas_vacio(self, client):
        """Probar listado cuando no hay recetas"""
        response = client.get("/recetas")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_listar_recetas(self, client):
        """Probar listado de recetas"""
        # Crear algunas recetas
        recetas = [
            {"nombre": "Receta 1", "descripcion": "Desc 1", "pasos": [], "ingredientes": []},
            {"nombre": "Receta 2", "descripcion": "Desc 2", "pasos": [], "ingredientes": []},
        ]
        for receta in recetas:
            client.post("/recetas", json=receta)
        
        response = client.get("/recetas")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_obtener_receta_por_id(self, client):
        """Probar obtención de una receta específica"""
        # Crear receta
        receta_data = {
            "nombre": "Tarta de Manzana",
            "descripcion": "Postre delicioso",
            "tiempo_preparacion": 60,
            "porciones": 8,
            "pasos": [],
            "ingredientes": []
        }
        create_response = client.post("/recetas", json=receta_data)
        receta_id = create_response.json()["id"]
        
        # Obtener receta
        response = client.get(f"/recetas/{receta_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Tarta de Manzana"
        assert data["id"] == receta_id
    
    def test_obtener_receta_no_existente(self, client):
        """Probar obtener una receta que no existe"""
        response = client.get("/recetas/999")
        assert response.status_code == 404
        assert "no encontrada" in response.json()["detail"].lower()
    
    def test_actualizar_receta(self, client):
        """Probar actualización de una receta"""
        # Crear receta
        receta_data = {
            "nombre": "Pizza Original",
            "descripcion": "Pizza básica",
            "tiempo_preparacion": 30,
            "porciones": 4,
            "pasos": [],
            "ingredientes": []
        }
        create_response = client.post("/recetas", json=receta_data)
        receta_id = create_response.json()["id"]
        
        # Actualizar receta
        update_data = {
            "nombre": "Pizza Mejorada",
            "tiempo_preparacion": 45
        }
        response = client.put(f"/recetas/{receta_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Pizza Mejorada"
        assert data["tiempo_preparacion"] == 45
        assert data["descripcion"] == "Pizza básica"  # No cambió
    
    def test_eliminar_receta(self, client):
        """Probar eliminación de una receta"""
        # Crear receta
        receta_data = {
            "nombre": "Receta Temporal",
            "descripcion": "Para eliminar",
            "pasos": [],
            "ingredientes": []
        }
        create_response = client.post("/recetas", json=receta_data)
        receta_id = create_response.json()["id"]
        
        # Eliminar receta
        response = client.delete(f"/recetas/{receta_id}")
        assert response.status_code == 200
        assert "eliminada" in response.json()["message"].lower()
        
        # Verificar que ya no existe
        get_response = client.get(f"/recetas/{receta_id}")
        assert get_response.status_code == 404
    
    def test_agregar_paso_a_receta(self, client):
        """Probar agregar un paso a una receta existente"""
        # Crear receta sin pasos
        receta_data = {
            "nombre": "Sopa",
            "descripcion": "Sopa casera",
            "pasos": [],
            "ingredientes": []
        }
        create_response = client.post("/recetas", json=receta_data)
        receta_id = create_response.json()["id"]
        
        # Agregar paso
        paso_data = {
            "numero_paso": 1,
            "descripcion": "Calentar agua"
        }
        response = client.post(f"/recetas/{receta_id}/pasos", json=paso_data)
        assert response.status_code == 201
        data = response.json()
        assert data["descripcion"] == "Calentar agua"
        assert data["numero_paso"] == 1
    
    def test_eliminar_paso_de_receta(self, client):
        """Probar eliminar un paso de una receta"""
        # Crear receta con pasos
        receta_data = {
            "nombre": "Receta con pasos",
            "pasos": [
                {"numero_paso": 1, "descripcion": "Paso 1"},
                {"numero_paso": 2, "descripcion": "Paso 2"}
            ],
            "ingredientes": []
        }
        create_response = client.post("/recetas", json=receta_data)
        receta_id = create_response.json()["id"]
        paso_id = create_response.json()["pasos"][0]["id"]
        
        # Eliminar paso
        response = client.delete(f"/recetas/{receta_id}/pasos/{paso_id}")
        assert response.status_code == 200
        assert "eliminado" in response.json()["message"].lower()
    
    def test_crear_receta_con_ingredientes(self, client):
        """Probar creación de receta con ingredientes"""
        receta_data = {
            "nombre": "Receta con ingredientes",
            "descripcion": "Test ingredientes",
            "pasos": [],
            "ingredientes": [
                {"ingrediente_id": 1, "cantidad": 200.0},
                {"ingrediente_id": 2, "cantidad": 100.0}
            ]
        }
        response = client.post("/recetas", json=receta_data)
        assert response.status_code == 201
        # Nota: Los ingredientes deben existir en la base de datos
    
    def test_paginacion_recetas(self, client):
        """Probar paginación en el listado de recetas"""
        # Crear 5 recetas
        for i in range(5):
            receta_data = {
                "nombre": f"Receta {i+1}",
                "descripcion": f"Descripción {i+1}",
                "pasos": [],
                "ingredientes": []
            }
            client.post("/recetas", json=receta_data)
        
        # Obtener primeras 2
        response = client.get("/recetas?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2
        
        # Obtener siguientes 2
        response = client.get("/recetas?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
