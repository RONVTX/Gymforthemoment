"""
Servicio de Pagos - Gestiona operaciones de pagos y recibos.
Responsabilidad única: Gestión de pagos, recibos e historial financiero.
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import logging
from infrastructure.exceptions import (
    ValidationError, NotFoundError, BusinessLogicError
)

logger = logging.getLogger(__name__)


class PaymentService:
    """Servicio especializado en gestión de pagos y recibos."""
    
    # Constantes
    PRECIO_MENSUALIDAD = 50.0  # Precio base de la mensualidad
    MESES = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    
    def __init__(self, recibo_model, cliente_model):
        """Inicializa el servicio de pagos."""
        self.recibo_model = recibo_model
        self.cliente_model = cliente_model
    
    def pagar_recibo(self, id_recibo: int) -> Tuple[bool, str]:
        """Marca un recibo como pagado.
        
        Args:
            id_recibo: ID del recibo a pagar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Obtener recibo
            recibo = self.recibo_model.obtener_por_id(id_recibo)
            if not recibo:
                raise NotFoundError(f"El recibo con ID {id_recibo} no existe")
            
            # Verificar si ya está pagado
            if recibo.get('estado') == 'pagado':
                raise BusinessLogicError("El recibo ya ha sido pagado")
            
            # Marcar como pagado
            success = self.recibo_model.marcar_pagado(id_recibo)
            if success:
                logger.info(f"Recibo pagado: {id_recibo}")
                return True, "Pago registrado exitosamente"
            else:
                raise BusinessLogicError("No se pudo procesar el pago")
                
        except (NotFoundError, BusinessLogicError) as e:
            logger.warning(f"Error al pagar recibo: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al pagar recibo: {e}")
            return False, "Error al procesar el pago"
    
    def generar_recibos_mes(self, mes: int, año: int) -> Tuple[bool, str]:
        """Genera recibos para todos los clientes activos de un mes.
        
        Args:
            mes: Número del mes (1-12)
            año: Año
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Validar mes y año
            if not (1 <= mes <= 12):
                raise ValidationError("El mes debe estar entre 1 y 12")
            if año < 2000 or año > 2100:
                raise ValidationError("Año inválido")
            
            # Obtener todos los clientes activos
            clientes = self.cliente_model.obtener_todos()
            clientes_activos = [c for c in clientes if c.get('rol') == 'cliente']
            
            recibos_generados = 0
            
            for cliente in clientes_activos:
                # Verificar si ya existe recibo para este mes
                recibo_existente = self.recibo_model.obtener_por_cliente_mes(
                    cliente['dni'], mes, año
                )
                
                if not recibo_existente:
                    # Crear nuevo recibo
                    monto = self.PRECIO_MENSUALIDAD
                    mes_nombre = self.MESES.get(mes, f"Mes {mes}")
                    descripcion = f"Mensualidad {mes_nombre} {año}"
                    
                    success = self.recibo_model.crear(
                        cliente['dni'],
                        monto,
                        descripcion,
                        mes,
                        año
                    )
                    
                    if success:
                        recibos_generados += 1
            
            logger.info(f"Se generaron {recibos_generados} recibos para {mes}/{año}")
            return True, f"Se generaron {recibos_generados} recibos para {self.MESES[mes]} {año}"
            
        except ValidationError as e:
            logger.warning(f"Error al generar recibos: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al generar recibos: {e}")
            return False, "Error al generar recibos"
    
    def obtener_mis_recibos(self, usuario_actual: Dict) -> List[Dict]:
        """Obtiene los recibos del usuario actual.
        
        Args:
            usuario_actual: Usuario autenticado
            
        Returns:
            Lista de recibos del usuario
        """
        try:
            id_cliente = usuario_actual.get('id')
            if not id_cliente:
                logger.warning("Usuario sin ID en obtener_mis_recibos")
                return []
            recibos = self.recibo_model.obtener_recibos_cliente(id_cliente)
            logger.info(f"Se obtuvieron {len(recibos)} recibos para cliente {id_cliente}")
            return recibos
        except Exception as e:
            logger.error(f"Error al obtener recibos del cliente: {e}")
            return []
    
    def obtener_todos_recibos(self) -> List[Dict]:
        """Obtiene todos los recibos del sistema."""
        try:
            recibos = self.recibo_model.obtener_todos_recibos()
            logger.info(f"Se obtuvieron {len(recibos)} recibos totales")
            return recibos
        except Exception as e:
            logger.error(f"Error al obtener todos los recibos: {e}")
            return []
    
    def obtener_estadisticas_financieras(self) -> Dict:
        """Obtiene estadísticas financieras del gimnasio.
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            recibos = self.recibo_model.obtener_todos_recibos()
            
            total_recibos = len(recibos)
            recibos_pagados = len([r for r in recibos if r.get('estado') == 'pagado'])
            recibos_pendientes = total_recibos - recibos_pagados
            
            monto_total = sum(float(r.get('monto', 0)) for r in recibos)
            monto_pagado = sum(
                float(r.get('monto', 0)) for r in recibos if r.get('estado') == 'pagado'
            )
            monto_pendiente = monto_total - monto_pagado
            
            estadisticas = {
                'total_recibos': total_recibos,
                'recibos_pagados': recibos_pagados,
                'recibos_pendientes': recibos_pendientes,
                'monto_total': monto_total,
                'monto_pagado': monto_pagado,
                'monto_pendiente': monto_pendiente,
                'porcentaje_pago': (monto_pagado / monto_total * 100) if monto_total > 0 else 0
            }
            
            logger.info("Estadísticas financieras calculadas")
            return estadisticas
            
        except Exception as e:
            logger.error(f"Error al calcular estadísticas: {e}")
            return {}
