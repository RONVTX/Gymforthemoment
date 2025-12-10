from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime
import logging

# Import models
from core.models import Database, Cliente, Aparato, Reserva, Recibo, Notificacion

# Import services
from core.services import (
    AuthService, ClientService, ApparatusService,
    ReservationService, PaymentService
)

# Import infrastructure exceptions (for controller-level checks)
from infrastructure.exceptions import (
    GymException, AuthenticationError, AuthorizationError,
    ValidationError, NotFoundError, BusinessLogicError
)
from infrastructure.dtos import (
    UsuarioDTO, ResponseDTO, EstadisticasDTO
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GymController:
    """Controlador principal que orquesta los servicios de negocio.

    Este controlador actúa como orquestador y punto de integración con las vistas.
    Toda la lógica de negocio está delegada a servicios especializados.
    """

    MESES = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    def __init__(self):
        try:
            # Inicializar base de datos y modelos
            self.db = Database()
            self.cliente_model = Cliente(self.db)
            self.aparato_model = Aparato(self.db)
            self.reserva_model = Reserva(self.db)
            self.recibo_model = Recibo(self.db)
            self.notificacion_model = Notificacion(self.db)

            # Inicializar servicios
            self.auth_service = AuthService(self.cliente_model)
            self.client_service = ClientService(self.cliente_model)
            self.apparatus_service = ApparatusService(self.aparato_model, self.reserva_model)
            self.reservation_service = ReservationService(
                self.reserva_model, self.aparato_model, self.cliente_model, self.notificacion_model
            )
            self.payment_service = PaymentService(self.recibo_model, self.cliente_model)

            logger.info("GymController inicializado correctamente con todos los servicios")
        except Exception as e:
            logger.error(f"Error al inicializar GymController: {e}")
            raise

    # Compatibility proxy for previous code that accessed `controller.usuario_actual`
    @property
    def usuario_actual(self) -> Optional[Dict]:
        try:
            return self.auth_service.obtener_usuario_actual()
        except Exception:
            return None

    @usuario_actual.setter
    def usuario_actual(self, value: Optional[Dict]):
        try:
            self.auth_service.usuario_actual = value
        except Exception:
            pass

    # Authentication
    def login(self, dni: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        return self.auth_service.login(dni, password)

    def logout(self) -> None:
        self.auth_service.logout()

    def registrar_usuario(self, nombre: str, apellido: str, dni: str,
                         telefono: str, email: str, password: str) -> Tuple[bool, str]:
        return self.client_service.registrar_usuario(nombre, apellido, dni, telefono, email, password)

    def es_admin(self) -> bool:
        return self.auth_service.es_admin()

    def es_cliente(self) -> bool:
        return self.auth_service.es_cliente()

    def hay_sesion_activa(self) -> bool:
        return self.auth_service.hay_sesion_activa()

    def obtener_usuario_actual(self) -> Optional[Dict]:
        return self.auth_service.obtener_usuario_actual()

    # Clients
    def obtener_clientes(self) -> List[Dict]:
        if not self.es_admin():
            logger.warning("Acceso denegado: obtener_clientes requiere admin")
            return []
        return self.client_service.obtener_clientes()

    def crear_cliente_admin(self, nombre: str, apellido: str, dni: str, telefono: str, email: str, password: str, tipo: str = 'cliente') -> Tuple[bool, str]:
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        return self.client_service.crear_cliente_admin(nombre, apellido, dni, telefono, email, password, tipo)

    def eliminar_cliente_admin(self, id_cliente: int) -> Tuple[bool, str]:
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        return self.client_service.eliminar_cliente(id_cliente)

    # Apparatus
    def obtener_aparatos(self) -> List[Dict]:
        return self.apparatus_service.obtener_aparatos()

    def crear_aparato(self, nombre: str, tipo: str, descripcion: str = "") -> Tuple[bool, str]:
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        return self.apparatus_service.crear_aparato(nombre, tipo, descripcion)

    def eliminar_aparato(self, id_aparato: int) -> Tuple[bool, str]:
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        return self.apparatus_service.eliminar_aparato(id_aparato)

    # Reservations
    def crear_reserva(self, id_aparato: int, dia_semana: str, hora_inicio: str) -> Tuple[bool, str]:
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return False, "Debe iniciar sesión"
        return self.reservation_service.crear_reserva(usuario, id_aparato, dia_semana, hora_inicio)

    def obtener_mis_reservas(self) -> List[Dict]:
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return []
        return self.reservation_service.obtener_mis_reservas(usuario)

    def obtener_todas_reservas(self) -> List[Dict]:
        if not self.es_admin():
            logger.warning("Acceso denegado: obtener_todas_reservas requiere admin")
            return []
        return self.reservation_service.obtener_todas_reservas()

    def obtener_reservas_pendientes(self) -> List[Dict]:
        """Obtiene las reservas pendientes de aprobación"""
        if not self.es_admin():
            logger.warning("Acceso denegado: obtener_reservas_pendientes requiere admin")
            return []
        return self.reservation_service.obtener_reservas_pendientes()

    def aceptar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        """Admin acepta una reserva pendiente"""
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        return self.reservation_service.aceptar_reserva(id_reserva)

    def rechazar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        """Admin rechaza una reserva pendiente"""
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        return self.reservation_service.rechazar_reserva(id_reserva)

    def obtener_ocupacion_dia(self, dia_semana: str) -> List[Dict]:
        return self.reservation_service.obtener_ocupacion_dia(dia_semana)

    def eliminar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return False, "Debe iniciar sesión"
        return self.reservation_service.eliminar_reserva(id_reserva, usuario)

    def eliminar_reserva_admin(self, id_reserva: int) -> Tuple[bool, str]:
        """Admin puede eliminar cualquier reserva sin restricciones."""
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        # Crear un usuario fake para la eliminación (el admin está eliminando por eso)
        admin_user = self.obtener_usuario_actual()
        return self.reservation_service.eliminar_reserva(id_reserva, admin_user)

    def crear_reserva_admin(self, id_cliente: int, id_aparato: int, dia_semana: str, hora_inicio: str) -> Tuple[bool, str]:
        """Admin puede crear reserva para cualquier cliente."""
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        
        try:
            # Obtener cliente
            cliente = self.cliente_model.obtener_por_id(id_cliente)
            if not cliente:
                return False, f"Cliente con ID {id_cliente} no encontrado"
            
            # Convertir a usuario dict
            usuario_dict = {
                'id': cliente['id'],
                'nombre': cliente['nombre'],
                'dni': cliente['dni']
            }
            
            return self.reservation_service.crear_reserva(usuario_dict, id_aparato, dia_semana, hora_inicio)
        except Exception as e:
            logger.error(f"Error al crear reserva para cliente: {e}")
            return False, str(e)

    def verificar_disponibilidad(self, id_aparato: int, dia_semana: str, hora_inicio: str) -> bool:
        return self.reservation_service.verificar_disponibilidad(id_aparato, dia_semana, hora_inicio)

    # Notificaciones
    def obtener_mis_notificaciones(self) -> List[Dict]:
        """Obtiene las notificaciones del usuario actual"""
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return []
        return self.notificacion_model.obtener_por_cliente(usuario.get('id'))

    def obtener_notificaciones_no_leidas(self) -> int:
        """Obtiene el número de notificaciones no leídas del usuario actual"""
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return 0
        return self.notificacion_model.contar_no_leidas(usuario.get('id'))

    def marcar_notificacion_leida(self, id_notificacion: int) -> Tuple[bool, str]:
        """Marca una notificación como leída"""
        try:
            success = self.notificacion_model.marcar_como_leida(id_notificacion)
            if success:
                return True, "Notificación marcada como leída"
            else:
                return False, "No se pudo marcar la notificación"
        except Exception as e:
            logger.error(f"Error al marcar notificación: {e}")
            return False, "Error al marcar notificación"

    def eliminar_notificacion(self, id_notificacion: int) -> Tuple[bool, str]:
        """Elimina una notificación del usuario actual"""
        try:
            usuario = self.obtener_usuario_actual()
            if not usuario:
                return False, "Debe iniciar sesión"
            # Opcional: comprobar que la notificación pertenece al usuario
            notifs = self.notificacion_model.obtener_por_cliente(usuario.get('id'))
            if not any(n['id'] == id_notificacion for n in notifs):
                return False, "Notificación no encontrada o no pertenece al usuario"

            success = self.notificacion_model.eliminar_notificacion(id_notificacion)
            if success:
                return True, "Notificación eliminada"
            else:
                return False, "No se pudo eliminar la notificación"
        except Exception as e:
            logger.error(f"Error al eliminar notificación: {e}")
            return False, "Error al eliminar notificación"

    # Payments
    def pagar_recibo(self, id_recibo: int) -> Tuple[bool, str]:
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return False, "Debe iniciar sesión"
        return self.payment_service.pagar_recibo(id_recibo)

    def pagar_recibo_admin(self, id_recibo: int) -> Tuple[bool, str]:
        """Admin puede marcar recibos como pagados sin restricciones."""
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        return self.payment_service.pagar_recibo(id_recibo)

    def generar_recibos_mes(self, mes: int, anio: int) -> Tuple[bool, str]:
        if not self.es_admin():
            return False, "Se requieren permisos de administrador"
        return self.payment_service.generar_recibos_mes(mes, anio)

    def obtener_mis_recibos(self) -> List[Dict]:
        usuario = self.obtener_usuario_actual()
        if not usuario:
            return []
        return self.payment_service.obtener_mis_recibos(usuario)

    def obtener_mis_recibos_pendientes(self) -> List[Dict]:
        """Obtiene los recibos pendientes del usuario actual."""
        recibos = self.obtener_mis_recibos()
        return [r for r in recibos if r.get('estado') == 'pendiente']

    def obtener_todos_recibos(self) -> List[Dict]:
        if not self.es_admin():
            logger.warning("Acceso denegado: obtener_todos_recibos requiere admin")
            return []
        return self.payment_service.obtener_todos_recibos()

    def obtener_estadisticas_financieras(self) -> Dict:
        if not self.es_admin():
            logger.warning("Acceso denegado: obtener_estadisticas_financieras requiere admin")
            return {}
        return self.payment_service.obtener_estadisticas_financieras()

    def obtener_estadisticas_generales(self) -> Dict:
        """Obtiene estadísticas generales del gimnasio para el dashboard admin."""
        if not self.es_admin():
            logger.warning("Acceso denegado: obtener_estadisticas_generales requiere admin")
            return {}
        
        try:
            clientes = self.obtener_clientes()
            aparatos = self.obtener_aparatos()
            todas_reservas = self.obtener_todas_reservas()
            todos_recibos = self.obtener_todos_recibos()
            
            # Calcular estadísticas
            total_clientes = len(clientes)
            total_aparatos = len(aparatos)
            total_reservas = len(todas_reservas)
            total_recibos = len(todos_recibos)
            
            # Recibos por estado
            recibos_pagados = len([r for r in todos_recibos if r.get('estado') == 'pagado'])
            recibos_pendientes = len([r for r in todos_recibos if r.get('estado') == 'pendiente'])
            
            # Financiero
            total_ingresos = sum(r.get('monto', 0) for r in todos_recibos if r.get('estado') == 'pagado')
            deuda_total = sum(r.get('monto', 0) for r in todos_recibos if r.get('estado') == 'pendiente')
            
            # Clientes morosos
            morosos = self.obtener_morosos()
            total_morosos = len(morosos)
            
            return {
                'total_clientes': total_clientes,
                'total_aparatos': total_aparatos,
                'total_reservas': total_reservas,
                'total_recibos': total_recibos,
                'recibos_pagados': recibos_pagados,
                'recibos_pendientes': recibos_pendientes,
                'total_morosos': total_morosos,
                'total_ingresos': total_ingresos,
                'deuda_total': deuda_total
            }
        except Exception as e:
            logger.error(f"Error al obtener estadísticas generales: {e}")
            return {}

    def obtener_morosos(self) -> List[Dict]:
        """Obtiene lista de clientes con recibos pendientes."""
        if not self.es_admin():
            logger.warning("Acceso denegado: obtener_morosos requiere admin")
            return []
        
        try:
            clientes = self.obtener_clientes()
            todos_recibos = self.obtener_todos_recibos()
            
            morosos = []
            for cliente in clientes:
                recibos_pendientes = [r for r in todos_recibos 
                                     if r.get('id_cliente') == cliente['id'] and r.get('estado') == 'pendiente']
                
                if recibos_pendientes:
                    deuda_total = sum(r.get('monto', 0) for r in recibos_pendientes)
                    morosos.append({
                        'id': cliente['id'],
                        'nombre': cliente['nombre'],
                        'apellido': cliente['apellido'],
                        'dni': cliente['dni'],
                        'telefono': cliente['telefono'],
                        'email': cliente['email'],
                        'recibos_pendientes': len(recibos_pendientes),
                        'deuda_total': deuda_total
                    })
            
            return morosos
        except Exception as e:
            logger.error(f"Error al obtener clientes morosos: {e}")
            return []

    # Utilities
    def generar_horarios_disponibles(self) -> List[str]:
        horarios = []
        for hora in range(24):
            horarios.append(f"{hora:02d}:00")
            horarios.append(f"{hora:02d}:30")
        return horarios

    def obtener_nombre_mes(self, mes: int) -> str:
        return self.MESES.get(mes, "Desconocido")
