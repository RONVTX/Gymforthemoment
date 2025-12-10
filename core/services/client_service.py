"""
Servicio de Clientes - Gestiona operaciones CRUD de clientes.
Responsabilidad única: Gestión de datos de clientes.
"""

from typing import List, Dict, Tuple
import logging
from infrastructure.exceptions import (
    ValidationError, NotFoundError, BusinessLogicError
)
from infrastructure.validators import ValidadorCliente
from infrastructure.dtos import UsuarioDTO, ResponseDTO

logger = logging.getLogger(__name__)


class ClientService:
    """Servicio especializado en gestión de clientes."""
    
    def __init__(self, cliente_model):
        """Inicializa el servicio de clientes."""
        self.cliente_model = cliente_model
    
    def obtener_clientes(self) -> List[Dict]:
        """Obtiene la lista de todos los clientes."""
        try:
            clientes = self.cliente_model.obtener_todos()
            logger.info(f"Se obtuvieron {len(clientes)} clientes")
            return clientes
        except Exception as e:
            logger.error(f"Error al obtener clientes: {e}")
            return []
    
    def crear_cliente_admin(self, nombre: str, apellido: str, dni: str, 
                           telefono: str, email: str, password: str, tipo: str = 'cliente') -> Tuple[bool, str]:
        """Crea un nuevo cliente desde el panel de administrador.
        
        Args:
            nombre: Nombre del cliente
            apellido: Apellido del cliente
            dni: DNI único del cliente
            telefono: Teléfono de contacto
            email: Email del cliente
            password: Contraseña inicial
            tipo: Tipo de usuario ('cliente' o 'admin')
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Validar campos
            ValidadorCliente.validar_datos_registro(nombre, apellido, dni, password, email, telefono)
            
            # Validar tipo
            if tipo not in ['cliente', 'admin']:
                raise ValidationError("El tipo debe ser 'cliente' o 'admin'")
            
            # Verificar que el DNI no exista
            if self.cliente_model.dni_existe(dni):
                raise BusinessLogicError(f"El cliente con DNI {dni} ya existe")
            
            # Crear cliente con el tipo especificado
            success = self.cliente_model.crear_cliente(nombre, apellido, dni, telefono, email, password, tipo_usuario=tipo)
            if success:
                logger.info(f"Cliente creado exitosamente: {dni} (tipo: {tipo})")
                return True, f"Cliente {nombre} {apellido} creado exitosamente como {tipo}"
            else:
                raise BusinessLogicError("No se pudo crear el cliente")
                
        except (ValidationError, BusinessLogicError) as e:
            logger.warning(f"Error al crear cliente: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al crear cliente: {e}")
            return False, "Error al crear el cliente"
    
    def registrar_usuario(self, nombre: str, apellido: str, dni: str, 
                         telefono: str, email: str, password: str) -> Tuple[bool, str]:
        """Registra un nuevo usuario cliente (auto-registro).
        
        Args:
            nombre: Nombre del cliente
            apellido: Apellido del cliente
            dni: DNI único del cliente
            telefono: Teléfono de contacto
            email: Email del cliente
            password: Contraseña elegida
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Validar campos
            ValidadorCliente.validar_datos_registro(nombre, apellido, dni, password, email, telefono)
            
            # Verificar que el DNI no exista
            if self.cliente_model.dni_existe(dni):
                raise BusinessLogicError(f"El DNI {dni} ya está registrado")
            
            # Crear cliente con rol 'cliente'
            success = self.cliente_model.crear_cliente(nombre, apellido, dni, telefono, email, password, tipo_usuario='cliente')
            if success:
                logger.info(f"Usuario registrado exitosamente: {dni}")
                return True, "Registro completado exitosamente. Ya puedes iniciar sesión"
            else:
                raise BusinessLogicError("No se pudo registrar el usuario")
                
        except (ValidationError, BusinessLogicError) as e:
            logger.warning(f"Error en registro de usuario: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado en registro: {e}")
            return False, "Error durante el registro"

    def eliminar_cliente(self, id_cliente: int) -> Tuple[bool, str]:
        """Elimina un cliente del sistema (solo admin).
        
        Args:
            id_cliente: ID del cliente a eliminar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # El cliente debe existir
            cliente = self.cliente_model.obtener_por_id(id_cliente)
            if not cliente:
                raise NotFoundError(f"Cliente con ID {id_cliente} no encontrado")
            
            # No permitir eliminar admin
            if cliente.get('tipo') == 'admin':
                raise BusinessLogicError("No se puede eliminar un usuario administrador")
            
            # Aquí iría la lógica de eliminación si el modelo la tuviera
            # Por ahora retornamos un mensaje informativo
            logger.warning(f"Eliminación de cliente {id_cliente} solicitada pero no implementada en modelo")
            return False, "La eliminación de clientes aún no está implementada a nivel de base de datos"
                
        except (ValidationError, NotFoundError, BusinessLogicError) as e:
            logger.warning(f"Error al eliminar cliente: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al eliminar cliente: {e}")
            return False, "Error al eliminar el cliente"