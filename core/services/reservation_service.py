"""
Servicio de Reservas - Gestiona operaciones de reservas de aparatos.
Responsabilidad única: Gestión de reservas y disponibilidad.
"""

from typing import List, Dict, Tuple
from datetime import datetime
import logging
from infrastructure.exceptions import (
    ValidationError, NotFoundError, BusinessLogicError
)
from infrastructure.validators import ValidadorReserva

logger = logging.getLogger(__name__)


class ReservationService:
    """Servicio especializado en gestión de reservas."""
    
    def __init__(self, reserva_model, aparato_model, cliente_model, notificacion_model=None):
        """Inicializa el servicio de reservas."""
        self.reserva_model = reserva_model
        self.aparato_model = aparato_model
        self.cliente_model = cliente_model
        self.notificacion_model = notificacion_model
    
    def crear_reserva(self, usuario_actual: Dict, id_aparato: int, 
                     dia_semana: str, hora_inicio: str) -> Tuple[bool, str]:
        """Crea una nueva reserva de aparato.
        
        Args:
            usuario_actual: Usuario autenticado realizando la reserva
            id_aparato: ID del aparato a reservar
            dia_semana: Día de la semana (lunes-domingo)
            hora_inicio: Hora de inicio (HH:MM)
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Validar campos
            ValidadorReserva.validar_datos_reserva(id_aparato, dia_semana, hora_inicio)
            
            # Verificar que el aparato existe
            aparato = self.aparato_model.obtener_por_id(id_aparato)
            if not aparato:
                raise NotFoundError(f"El aparato con ID {id_aparato} no existe")
            
            # Verificar disponibilidad
            if not self.verificar_disponibilidad(id_aparato, dia_semana, hora_inicio):
                raise BusinessLogicError(
                    f"El aparato no está disponible en {dia_semana} a las {hora_inicio}"
                )
            
            # Crear reserva
            id_cliente = usuario_actual.get('id')
            success, message = self.reserva_model.crear_reserva(id_cliente, id_aparato, dia_semana, hora_inicio)
            
            if success:
                logger.info(f"Reserva creada: Cliente {id_cliente} - Aparato {id_aparato}")
                return True, f"Reserva confirmada para {aparato['nombre']} el {dia_semana}"
            else:
                raise BusinessLogicError(message)
                
        except (ValidationError, NotFoundError, BusinessLogicError) as e:
            logger.warning(f"Error al crear reserva: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al crear reserva: {e}")
            return False, "Error al crear la reserva"
    def obtener_mis_reservas(self, usuario_actual: Dict) -> List[Dict]:
        """Obtiene las reservas del usuario actual."""
        try:
            id_cliente = usuario_actual.get('id')
            if not id_cliente:
                logger.warning("Usuario sin ID en obtener_mis_reservas")
                return []
            reservas = self.reserva_model.obtener_reservas_cliente(id_cliente)
            logger.info(f"Se obtuvieron {len(reservas)} reservas para cliente {id_cliente}")
            return reservas
        except Exception as e:
            logger.error(f"Error al obtener reservas del cliente: {e}")
            return []
    
    def obtener_todas_reservas(self) -> List[Dict]:
        """Obtiene todas las reservas del sistema."""
        try:
            reservas = self.reserva_model.obtener_todas()
            logger.info(f"Se obtuvieron {len(reservas)} reservas totales")
            return reservas
        except Exception as e:
            logger.error(f"Error al obtener todas las reservas: {e}")
            return []
    
    def obtener_ocupacion_dia(self, dia_semana: str) -> List[Dict]:
        """Obtiene la ocupación de aparatos para un día específico.
        
        Args:
            dia_semana: Día de la semana
            
        Returns:
            Lista de aparatos con su ocupación
        """
        try:
            ValidadorReserva.validar_dia_semana(dia_semana)
            
            # Obtener ocupación directamente del modelo
            resultado = self.reserva_model.obtener_ocupacion_dia(dia_semana)
            logger.debug(f"Ocupación para {dia_semana}: {len(resultado)} registros")
            return resultado
            
        except ValidationError as e:
            logger.warning(f"Error al obtener ocupación: {e}")
            return []
    
    def eliminar_reserva(self, id_reserva: int, usuario_actual: Dict) -> Tuple[bool, str]:
        """Elimina una reserva existente.
        
        Args:
            id_reserva: ID de la reserva a eliminar
            usuario_actual: Usuario realizando la eliminación
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Por ahora, permitir eliminación sin verificar propietario
            # (más adelante se puede refinar con acceso directo a la BD para verificar)
            success = self.reserva_model.eliminar_reserva(id_reserva)
            if success:
                logger.info(f"Reserva eliminada: {id_reserva}")
                return True, "Reserva eliminada exitosamente"
            else:
                raise BusinessLogicError("No se pudo eliminar la reserva")
                
        except BusinessLogicError as e:
            logger.warning(f"Error al eliminar reserva: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al eliminar reserva: {e}")
            return False, "Error al eliminar la reserva"
    
    def verificar_disponibilidad(self, id_aparato: int, dia_semana: str, 
                                 hora_inicio: str) -> bool:
        """Verifica si un aparato está disponible en un horario específico.
        
        Args:
            id_aparato: ID del aparato
            dia_semana: Día de la semana
            hora_inicio: Hora de inicio
            
        Returns:
            True si está disponible, False en caso contrario
        """
        try:
            # Obtener ocupación del día
            ocupacion = self.reserva_model.obtener_ocupacion_dia(dia_semana)
            # Verificar si hay conflicto para este aparato y horario
            for item in ocupacion:
                if item.get('id_aparato') == id_aparato and item.get('hora_inicio') == hora_inicio:
                    return False  # No disponible
            return True  # Disponible
        except Exception as e:
            logger.error(f"Error al verificar disponibilidad: {e}")
            return False
    
    def aceptar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        """Acepta una reserva pendiente.
        
        Args:
            id_reserva: ID de la reserva a aceptar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            success, message = self.reserva_model.aceptar_reserva(id_reserva)
            if success:
                logger.info(f"Reserva aceptada: {id_reserva}")
                
                # Obtener detalles de la reserva para la notificación
                if self.notificacion_model:
                    try:
                        # Obtener información de la reserva aceptada
                        reservas_pendientes = self.reserva_model.obtener_todas()
                        for reserva in reservas_pendientes:
                            if reserva['id'] == id_reserva:
                                # Crear notificación
                                self.notificacion_model.crear_notificacion(
                                    id_cliente=self._obtener_id_cliente_por_reserva(id_reserva),
                                    id_reserva=id_reserva,
                                    tipo='aceptada',
                                    mensaje=f"Tu reserva para {reserva['aparato']} el {reserva['dia']} a las {reserva['hora_inicio']} ha sido ACEPTADA ✅"
                                )
                                break
                    except Exception as e:
                        logger.error(f"Error al crear notificación de aceptación: {e}")
                
                return True, message
            else:
                raise BusinessLogicError(message)
        except BusinessLogicError as e:
            logger.warning(f"Error al aceptar reserva: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al aceptar reserva: {e}")
            return False, "Error al aceptar la reserva"
    
    def rechazar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        """Rechaza una reserva pendiente.
        
        Args:
            id_reserva: ID de la reserva a rechazar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            success, message = self.reserva_model.rechazar_reserva(id_reserva)
            if success:
                logger.info(f"Reserva rechazada: {id_reserva}")
                
                # Crear notificación
                if self.notificacion_model:
                    try:
                        # Obtener información de la reserva rechazada
                        reservas = self.reserva_model.obtener_todas()
                        for reserva in reservas:
                            if reserva['id'] == id_reserva:
                                # Crear notificación
                                self.notificacion_model.crear_notificacion(
                                    id_cliente=self._obtener_id_cliente_por_reserva(id_reserva),
                                    id_reserva=id_reserva,
                                    tipo='rechazada',
                                    mensaje=f"Tu reserva para {reserva['aparato']} el {reserva['dia']} a las {reserva['hora_inicio']} ha sido RECHAZADA ❌"
                                )
                                break
                    except Exception as e:
                        logger.error(f"Error al crear notificación de rechazo: {e}")
                
                return True, message
            else:
                raise BusinessLogicError(message)
        except BusinessLogicError as e:
            logger.warning(f"Error al rechazar reserva: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al rechazar reserva: {e}")
            return False, "Error al rechazar la reserva"
    
    def _obtener_id_cliente_por_reserva(self, id_reserva: int) -> int:
        """Obtiene el ID del cliente de una reserva"""
        try:
            return self.reserva_model.obtener_id_cliente_por_reserva(id_reserva)
        except Exception as e:
            logger.error(f"Error al obtener id_cliente: {e}")
            return None
    
    def obtener_reservas_pendientes(self) -> List[Dict]:
        """Obtiene todas las reservas pendientes.
        
        Returns:
            Lista de reservas pendientes
        """
        try:
            reservas = self.reserva_model.obtener_reservas_pendientes()
            logger.info(f"Se obtuvieron {len(reservas)} reservas pendientes")
            return reservas
        except Exception as e:
            logger.error(f"Error al obtener reservas pendientes: {e}")
            return []

