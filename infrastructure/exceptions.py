"""
Excepciones personalizadas para el sistema de gestión del gimnasio.
Permite mejor manejo de errores y debugging.
"""


class GymException(Exception):
    """Excepción base del sistema"""
    pass


class AuthenticationError(GymException):
    """Error de autenticación"""
    pass


class AuthorizationError(GymException):
    """Error de autorización (permisos)"""
    pass


class ValidationError(GymException):
    """Error de validación de datos"""
    pass


class NotFoundError(GymException):
    """Recurso no encontrado"""
    pass


class BusinessLogicError(GymException):
    """Error en la lógica de negocio"""
    pass


class DatabaseError(GymException):
    """Error en la base de datos"""
    pass
