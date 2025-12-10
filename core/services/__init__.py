"""
Módulo de Servicios - Componentes de lógica de negocio separados por dominio.

Contiene servicios especializados para cada área funcional del sistema:
- AuthService: Autenticación y autorización
- ClientService: Gestión de clientes
- ApparatusService: Gestión de aparatos
- ReservationService: Gestión de reservas
- PaymentService: Gestión de pagos y recibos
"""

from core.services.auth_service import AuthService
from core.services.client_service import ClientService
from core.services.apparatus_service import ApparatusService
from core.services.reservation_service import ReservationService
from core.services.payment_service import PaymentService

__all__ = [
    'AuthService',
    'ClientService',
    'ApparatusService',
    'ReservationService',
    'PaymentService'
]
