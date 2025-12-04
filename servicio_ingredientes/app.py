"""
Microservicio de Ingredientes
Maneja operaciones CRUD para ingredientes
"""
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
import sys
import os

# Agregar el directorio padre al path para importar database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db, init_db, Ingrediente

app = FastAPI(title="Microservicio de Ingredientes", version="1.0.0")

# Modelos Pydantic
class IngredienteCreate(BaseModel):
    nombre: str
    unidad_medida: Optional[str] = None
    categoria: Optional[str] = None

class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = None
    unidad_medida: Optional[str] = None
    categoria: Optional[str] = None

class IngredienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    unidad_medida: Optional[str] = None
    categoria: Optional[str] = None

# Eventos de inicio
@app.on_event("startup")
def startup_event():
    init_db()

# Endpoints
@app.get("/health")
def health_check():
    """Verificar que el servicio está activo"""
    return {"status": "healthy", "service": "ingredientes"}

@app.post("/ingredientes", response_model=IngredienteResponse, status_code=201)
def crear_ingrediente(ingrediente: IngredienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo ingrediente"""
    # Verificar si ya existe
    existing = db.query(Ingrediente).filter(Ingrediente.nombre == ingrediente.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail="El ingrediente ya existe")
    
    db_ingrediente = Ingrediente(
        nombre=ingrediente.nombre,
        unidad_medida=ingrediente.unidad_medida,
        categoria=ingrediente.categoria
    )
    db.add(db_ingrediente)
    db.commit()
    db.refresh(db_ingrediente)
    return db_ingrediente

@app.get("/ingredientes", response_model=List[IngredienteResponse])
def listar_ingredientes(
    skip: int = 0, 
    limit: int = 100, 
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de ingredientes, opcionalmente filtrados por categoría"""
    query = db.query(Ingrediente)
    
    if categoria:
        query = query.filter(Ingrediente.categoria == categoria)
    
    ingredientes = query.offset(skip).limit(limit).all()
    return ingredientes

@app.get("/ingredientes/{ingrediente_id}", response_model=IngredienteResponse)
def obtener_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    """Obtener un ingrediente específico por ID"""
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente

@app.put("/ingredientes/{ingrediente_id}", response_model=IngredienteResponse)
def actualizar_ingrediente(
    ingrediente_id: int, 
    ingrediente_update: IngredienteUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar un ingrediente existente"""
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    
    update_data = ingrediente_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ingrediente, key, value)
    
    db.commit()
    db.refresh(ingrediente)
    return ingrediente

@app.delete("/ingredientes/{ingrediente_id}")
def eliminar_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    """Eliminar un ingrediente"""
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    
    db.delete(ingrediente)
    db.commit()
    return {"message": "Ingrediente eliminado exitosamente"}

@app.get("/ingredientes/buscar/{nombre}")
def buscar_ingrediente(nombre: str, db: Session = Depends(get_db)):
    """Buscar ingredientes por nombre (búsqueda parcial)"""
    ingredientes = db.query(Ingrediente).filter(
        Ingrediente.nombre.ilike(f"%{nombre}%")
    ).all()
    return ingredientes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
