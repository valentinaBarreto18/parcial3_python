"""
Microservicio de Recetas
Maneja operaciones CRUD para recetas y sus pasos de preparación
"""
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
import sys
import os

# Agregar el directorio padre al path para importar database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db, init_db, Receta, Paso, RecetaIngrediente

app = FastAPI(title="Microservicio de Recetas", version="1.0.0")

# Modelos Pydantic para validación
class PasoCreate(BaseModel):
    numero_paso: int
    descripcion: str

class PasoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    numero_paso: int
    descripcion: str

class IngredienteRecetaCreate(BaseModel):
    ingrediente_id: int
    cantidad: float

class IngredienteRecetaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    ingrediente_id: int
    cantidad: float
    nombre_ingrediente: Optional[str] = None

class RecetaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    porciones: Optional[int] = None
    pasos: List[PasoCreate] = []
    ingredientes: List[IngredienteRecetaCreate] = []

class RecetaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    porciones: Optional[int] = None

class RecetaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    descripcion: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    porciones: Optional[int] = None
    pasos: List[PasoResponse] = []

# Eventos de inicio
@app.on_event("startup")
def startup_event():
    init_db()

# Endpoints
@app.get("/health")
def health_check():
    """Verificar que el servicio está activo"""
    return {"status": "healthy", "service": "recetas"}

@app.post("/recetas", response_model=RecetaResponse, status_code=201)
def crear_receta(receta: RecetaCreate, db: Session = Depends(get_db)):
    """Crear una nueva receta con sus pasos e ingredientes"""
    db_receta = Receta(
        nombre=receta.nombre,
        descripcion=receta.descripcion,
        tiempo_preparacion=receta.tiempo_preparacion,
        porciones=receta.porciones
    )
    db.add(db_receta)
    db.flush()
    
    # Agregar pasos
    for paso in receta.pasos:
        db_paso = Paso(
            receta_id=db_receta.id,
            numero_paso=paso.numero_paso,
            descripcion=paso.descripcion
        )
        db.add(db_paso)
    
    # Agregar ingredientes
    for ingrediente in receta.ingredientes:
        db_receta_ingrediente = RecetaIngrediente(
            receta_id=db_receta.id,
            ingrediente_id=ingrediente.ingrediente_id,
            cantidad=ingrediente.cantidad
        )
        db.add(db_receta_ingrediente)
    
    db.commit()
    db.refresh(db_receta)
    return db_receta

@app.get("/recetas", response_model=List[RecetaResponse])
def listar_recetas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de todas las recetas"""
    recetas = db.query(Receta).offset(skip).limit(limit).all()
    return recetas

@app.get("/recetas/{receta_id}", response_model=RecetaResponse)
def obtener_receta(receta_id: int, db: Session = Depends(get_db)):
    """Obtener una receta específica por ID"""
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

@app.put("/recetas/{receta_id}", response_model=RecetaResponse)
def actualizar_receta(receta_id: int, receta_update: RecetaUpdate, db: Session = Depends(get_db)):
    """Actualizar una receta existente"""
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    update_data = receta_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(receta, key, value)
    
    db.commit()
    db.refresh(receta)
    return receta

@app.delete("/recetas/{receta_id}")
def eliminar_receta(receta_id: int, db: Session = Depends(get_db)):
    """Eliminar una receta"""
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    db.delete(receta)
    db.commit()
    return {"message": "Receta eliminada exitosamente"}

@app.post("/recetas/{receta_id}/pasos", response_model=PasoResponse, status_code=201)
def agregar_paso(receta_id: int, paso: PasoCreate, db: Session = Depends(get_db)):
    """Agregar un paso a una receta"""
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    db_paso = Paso(
        receta_id=receta_id,
        numero_paso=paso.numero_paso,
        descripcion=paso.descripcion
    )
    db.add(db_paso)
    db.commit()
    db.refresh(db_paso)
    return db_paso

@app.delete("/recetas/{receta_id}/pasos/{paso_id}")
def eliminar_paso(receta_id: int, paso_id: int, db: Session = Depends(get_db)):
    """Eliminar un paso de una receta"""
    paso = db.query(Paso).filter(Paso.id == paso_id, Paso.receta_id == receta_id).first()
    if not paso:
        raise HTTPException(status_code=404, detail="Paso no encontrado")
    
    db.delete(paso)
    db.commit()
    return {"message": "Paso eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
