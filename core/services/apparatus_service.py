"""
Servicio de Aparatos - Gestiona operaciones CRUD de aparatos del gimnasio.
Responsabilidad única: Gestión de aparatos y equipos.
"""

from typing import List, Dict, Tuple
import logging
from infrastructure.exceptions import (
    ValidationError, NotFoundError, BusinessLogicError
)
from infrastructure.validators import ValidadorAparato

logger = logging.getLogger(__name__)


class ApparatusService:
    """Servicio especializado en gestión de aparatos."""
    
    def __init__(self, aparato_model, reserva_model):
        """Inicializa el servicio de aparatos."""
        self.aparato_model = aparato_model
        self.reserva_model = reserva_model
    
    def obtener_aparatos(self) -> List[Dict]:
        """Obtiene la lista de todos los aparatos disponibles."""
        try:
            aparatos = self.aparato_model.obtener_todos()
            logger.info(f"Se obtuvieron {len(aparatos)} aparatos")
            return aparatos
        except Exception as e:
            logger.error(f"Error al obtener aparatos: {e}")
            return []
    
    def crear_aparato(self, nombre: str, tipo: str, descripcion: str = "") -> Tuple[bool, str]:
        """Crea un nuevo aparato en el gimnasio.
        
        Args:
            nombre: Nombre del aparato
            tipo: Tipo/categoría del aparato
            descripcion: Descripción opcional del aparato
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Validar campos
            ValidadorAparato.validar_datos_aparato(nombre, tipo)
            
            # Crear aparato
            id_aparato = self.aparato_model.crear_aparato(nombre, tipo, descripcion)
            if id_aparato > 0:
                logger.info(f"Aparato creado exitosamente: {nombre}")
                return True, f"Aparato '{nombre}' creado exitosamente"
            else:
                raise BusinessLogicError("No se pudo crear el aparato")
                
        except (ValidationError, BusinessLogicError) as e:
            logger.warning(f"Error al crear aparato: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al crear aparato: {e}")
            return False, "Error al crear el aparato"
    
    def eliminar_aparato(self, id_aparato: int) -> Tuple[bool, str]:
        """Elimina un aparato del gimnasio.
        
        Solo puede eliminarse si no tiene reservas futuras.
        
        Args:
            id_aparato: ID del aparato a eliminar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Verificar que el aparato existe
            aparato = self.aparato_model.obtener_por_id(id_aparato)
            if not aparato:
                raise NotFoundError(f"El aparato con ID {id_aparato} no existe")
            
            # Verificar que no tiene reservas futuras
            reservas_futuras = self.reserva_model.obtener_reservas_por_aparato(id_aparato)
            if reservas_futuras:
                raise BusinessLogicError(
                    f"No se puede eliminar: el aparato tiene {len(reservas_futuras)} reservas"
                )
            
            # Eliminar aparato
            success = self.aparato_model.eliminar_aparato(id_aparato)
            if success:
                logger.info(f"Aparato eliminado exitosamente: {id_aparato}")
                return True, f"Aparato '{aparato['nombre']}' eliminado exitosamente"
            else:
                raise BusinessLogicError("No se pudo eliminar el aparato")
                
        except (ValidationError, NotFoundError, BusinessLogicError) as e:
            logger.warning(f"Error al eliminar aparato: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al eliminar aparato: {e}")
            return False, "Error al eliminar el aparato"
