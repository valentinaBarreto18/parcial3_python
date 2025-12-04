"""
Modelos de base de datos compartidos
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.db_config import Base

class Receta(Base):
    __tablename__ = "recetas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    tiempo_preparacion = Column(Integer)  # en minutos
    porciones = Column(Integer)
    
    # Relaciones
    pasos = relationship("Paso", back_populates="receta", cascade="all, delete-orphan")
    ingredientes = relationship("RecetaIngrediente", back_populates="receta", cascade="all, delete-orphan")

class Paso(Base):
    __tablename__ = "pasos"
    
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    numero_paso = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=False)
    
    # Relación con receta
    receta = relationship("Receta", back_populates="pasos")

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, unique=True)
    unidad_medida = Column(String(50))  # gramos, ml, unidades, etc.
    categoria = Column(String(100))  # lácteos, vegetales, carnes, etc.
    
    # Relación con recetas
    recetas = relationship("RecetaIngrediente", back_populates="ingrediente")

class RecetaIngrediente(Base):
    """Tabla intermedia para relacionar recetas con ingredientes"""
    __tablename__ = "receta_ingrediente"
    
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False)
    cantidad = Column(Float, nullable=False)
    
    # Relaciones
    receta = relationship("Receta", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="recetas")
