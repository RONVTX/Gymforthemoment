"""
Servicio de Autenticación - Gestiona login, logout y autenticación de usuarios.
Responsabilidad única: Autenticación y autorización.
"""

from typing import Optional, Tuple, Dict
import logging
from infrastructure.exceptions import (
    AuthenticationError, AuthorizationError, ValidationError
)
from infrastructure.validators import Validador

logger = logging.getLogger(__name__)


class AuthService:
    """Servicio especializado en autenticación y autorización."""
    
    def __init__(self, cliente_model):
        """Inicializa el servicio de autenticación."""
        self.cliente_model = cliente_model
        self.usuario_actual: Optional[Dict] = None
    
    def login(self, dni: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Autentica un usuario.
        
        Args:
            dni: DNI del usuario
            password: Contraseña en texto plano
            
        Returns:
            Tupla (éxito: bool, mensaje: str, usuario: Dict | None)
        """
        try:
            # Validar campos no vacíos
            Validador.validar_campos_no_vacios(dni, password)
            
            # Validar formato DNI
            Validador.validar_dni(dni)
            
            # Autenticar usuario
            usuario = self.cliente_model.autenticar(dni, password)
            if usuario:
                self.usuario_actual = usuario
                logger.info(f"Login exitoso: {usuario['dni']}")
                return True, "Inicio de sesión exitoso", usuario
            else:
                logger.warning(f"Intento de login fallido con DNI: {dni}")
                raise AuthenticationError("DNI o contraseña incorrectos")
                
        except ValidationError as e:
            logger.warning(f"Error de validación en login: {e}")
            return False, str(e), None
        except AuthenticationError as e:
            logger.warning(f"Error de autenticación: {e}")
            return False, str(e), None
        except Exception as e:
            logger.error(f"Error en login: {e}")
            return False, "Error en la autenticación", None
    
    def logout(self) -> None:
        """Cierra la sesión del usuario actual."""
        if self.usuario_actual:
            logger.info(f"Logout: {self.usuario_actual['dni']}")
        self.usuario_actual = None
    
    def es_admin(self) -> bool:
        """Verifica si el usuario actual es administrador."""
        return self.usuario_actual and self.usuario_actual.get('tipo') == 'admin'
    
    def es_cliente(self) -> bool:
        """Verifica si el usuario actual es cliente."""
        return self.usuario_actual and self.usuario_actual.get('tipo') == 'cliente'
    
    def hay_sesion_activa(self) -> bool:
        """Verifica si hay una sesión activa."""
        return self.usuario_actual is not None
    
    def _requiere_admin(self) -> bool:
        """Valida que haya sesión de admin activa."""
        if not self.es_admin():
            raise AuthorizationError("Se requieren permisos de administrador")
        return True
    
    def obtener_usuario_actual(self) -> Optional[Dict]:
        """Retorna el usuario actualmente autenticado."""
        return self.usuario_actual
