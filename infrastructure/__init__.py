"""
Módulo de Infraestructura - Componentes transversales del proyecto.

Contiene:
- exceptions: Jerarquía de excepciones personalizadas
- validators: Lógica centralizada de validación
- dtos: Data Transfer Objects con dataclasses
"""

from infrastructure.exceptions import (
    GymException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    BusinessLogicError,
    DatabaseError
)

from infrastructure.validators import (
    Validador,
    ValidadorCliente,
    ValidadorReserva,
    ValidadorAparato
)

from infrastructure.dtos import (
    UsuarioDTO,
    AparatoDTO,
    ReservaDTO,
    ReciboDTO,
    EstadisticasDTO,
    ResponseDTO
)

__all__ = [
    # Excepciones
    'GymException',
    'AuthenticationError',
    'AuthorizationError',
    'ValidationError',
    'NotFoundError',
    'BusinessLogicError',
    'DatabaseError',
    # Validadores
    'Validador',
    'ValidadorCliente',
    'ValidadorReserva',
    'ValidadorAparato',
    # DTOs
    'UsuarioDTO',
    'AparatoDTO',
    'ReservaDTO',
    'ReciboDTO',
    'EstadisticasDTO',
    'ResponseDTO'
]
