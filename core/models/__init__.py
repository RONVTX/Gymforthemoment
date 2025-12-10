"""Package `core.models` re-exports model classes.

Use `from core.models import Cliente, Reserva, ...` as before.
"""

from .database import Database
from .cliente import Cliente
from .aparato import Aparato
from .reserva import Reserva
from .recibo import Recibo
from .notificacion import Notificacion

__all__ = [
    'Database', 'Cliente', 'Aparato', 'Reserva', 'Recibo', 'Notificacion'
]
