"""
Archivo de compatibilidad para importaciones.

Este archivo permite importar desde la raíz del proyecto
manteniendo compatibilidad con código existente.
"""

# Exports para compatibilidad
from core import Controlador, Database, Cliente, Aparato, Reserva, Recibo
from infrastructure import (
    Validador, ValidadorCliente, ValidadorReserva, ValidadorAparato,
    GymException, AuthenticationError, AuthorizationError,
    ValidationError, NotFoundError, BusinessLogicError, DatabaseError,
    UsuarioDTO, AparatoDTO, ReservaDTO, ReciboDTO, EstadisticasDTO, ResponseDTO
)

__all__ = [
    # Core
    'Controlador',
    'Database',
    'Cliente',
    'Aparato',
    'Reserva',
    'Recibo',
    # Infrastructure - Exceptions
    'GymException',
    'AuthenticationError',
    'AuthorizationError',
    'ValidationError',
    'NotFoundError',
    'BusinessLogicError',
    'DatabaseError',
    # Infrastructure - Validators
    'Validador',
    'ValidadorCliente',
    'ValidadorReserva',
    'ValidadorAparato',
    # Infrastructure - DTOs
    'UsuarioDTO',
    'AparatoDTO',
    'ReservaDTO',
    'ReciboDTO',
    'EstadisticasDTO',
    'ResponseDTO'
]
