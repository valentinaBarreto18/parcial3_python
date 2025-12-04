"""
Configuración y fixtures compartidos para pytest
"""
import pytest
import sys
import os

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
