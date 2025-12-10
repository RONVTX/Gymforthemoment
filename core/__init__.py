"""Módulo Core - Lógica de negocio central del proyecto.

Contiene:
- models: Modelos de datos y acceso a base de datos
- controller: Controlador principal con lógica de negocio
"""

from core.models import Database, Cliente, Aparato, Reserva, Recibo, Notificacion
from core.controller import GymController as Controlador

__all__ = [
    'Database',
    'Cliente',
    'Aparato',
    'Reserva',
    'Recibo',
    'Notificacion',
    'Controlador'
]
