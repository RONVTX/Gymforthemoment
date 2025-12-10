"""
Servicio de Notificaciones - Gestiona notificaciones para clientes.
Responsabilidad única: Gestión de notificaciones de reservas.
"""

from typing import List, Dict, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Servicio especializado en gestión de notificaciones."""
    
    def __init__(self, notification_model):
        """Inicializa el servicio de notificaciones."""
        self.notification_model = notification_model
    
    def crear_notificacion_reserva(self, id_cliente: int, id_reserva: int, 
                                   tipo: str, aparato_nombre: str, 
                                   dia_semana: str, hora: str) -> Tuple[bool, str]:
        """Crea una notificación cuando una reserva es aceptada o rechazada.
        
        Args:
            id_cliente: ID del cliente
            id_reserva: ID de la reserva
            tipo: 'aceptada' o 'rechazada'
            aparato_nombre: Nombre del aparato
            dia_semana: Día de la semana
            hora: Hora de la reserva
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            if tipo == 'aceptada':
                mensaje = f"Tu reserva para {aparato_nombre} el {dia_semana} a las {hora} ha sido ACEPTADA ✅"
            elif tipo == 'rechazada':
                mensaje = f"Tu reserva para {aparato_nombre} el {dia_semana} a las {hora} ha sido RECHAZADA ❌"
            else:
                return False, "Tipo de notificación inválido"
            
            success = self.notification_model.crear_notificacion(
                id_cliente, id_reserva, tipo, mensaje
            )
            
            if success:
                logger.info(f"Notificación creada para cliente {id_cliente}")
                return True, "Notificación enviada al cliente"
            else:
                raise Exception("No se pudo crear la notificación")
                
        except Exception as e:
            logger.error(f"Error al crear notificación: {e}")
            return False, f"Error al notificar al cliente: {str(e)}"
    
    def obtener_notificaciones_cliente(self, id_cliente: int) -> List[Dict]:
        """Obtiene las notificaciones de un cliente.
        
        Args:
            id_cliente: ID del cliente
            
        Returns:
            Lista de notificaciones
        """
        try:
            notificaciones = self.notification_model.obtener_por_cliente(id_cliente)
            logger.info(f"Se obtuvieron {len(notificaciones)} notificaciones para cliente {id_cliente}")
            return notificaciones
        except Exception as e:
            logger.error(f"Error al obtener notificaciones: {e}")
            return []
    
    def marcar_como_leida(self, id_notificacion: int) -> Tuple[bool, str]:
        """Marca una notificación como leída.
        
        Args:
            id_notificacion: ID de la notificación
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            success = self.notification_model.marcar_como_leida(id_notificacion)
            if success:
                logger.info(f"Notificación {id_notificacion} marcada como leída")
                return True, "Notificación marcada como leída"
            else:
                return False, "No se pudo marcar la notificación"
        except Exception as e:
            logger.error(f"Error al marcar notificación: {e}")
            return False, "Error al marcar notificación"
    
    def obtener_notificaciones_no_leidas(self, id_cliente: int) -> int:
        """Obtiene el número de notificaciones no leídas.
        
        Args:
            id_cliente: ID del cliente
            
        Returns:
            Número de notificaciones no leídas
        """
        try:
            count = self.notification_model.contar_no_leidas(id_cliente)
            return count
        except Exception as e:
            logger.error(f"Error al contar notificaciones no leídas: {e}")
            return 0
