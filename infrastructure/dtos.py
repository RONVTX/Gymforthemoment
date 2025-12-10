"""
Data Transfer Objects (DTOs) para transferencia segura de datos entre capas.
Los DTOs ayudan a mantener la separación de responsabilidades y validar datos.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class UsuarioDTO:
    """DTO para datos de usuario"""
    id: int
    nombre: str
    apellido: str
    dni: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    tipo: str = 'cliente'
    fecha_registro: Optional[str] = None

    def get_nombre_completo(self) -> str:
        """Obtiene el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"


@dataclass
class AparatoDTO:
    """DTO para datos de aparato"""
    id: int
    nombre: str
    tipo: str
    descripcion: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.nombre} ({self.tipo})"


@dataclass
class ReservaDTO:
    """DTO para datos de reserva"""
    id: int
    cliente: str
    aparato: str
    dia: str
    hora_inicio: str
    hora_fin: Optional[str] = None
    fecha_reserva: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.cliente} - {self.aparato} ({self.dia} {self.hora_inicio})"


@dataclass
class ReciboDTO:
    """DTO para datos de recibo"""
    id: int
    cliente: str
    mes: int
    anio: int
    monto: float
    estado: str = 'pendiente'
    fecha_emision: Optional[str] = None

    def __str__(self) -> str:
        return f"Recibo {self.id} - €{self.monto:.2f} ({self.estado})"


@dataclass
class EstadisticasDTO:
    """DTO para datos de estadísticas"""
    total_clientes: int
    total_admins: int
    total_aparatos: int
    total_reservas: int
    total_morosos: int
    total_recibos: int
    recibos_pagados: int
    recibos_pendientes: int
    total_ingresos: float
    deuda_total: float
    porcentaje_pago: float

    def get_resumen(self) -> str:
        """Obtiene un resumen de las estadísticas"""
        return f"""
        Estadísticas Generales
        ==================
        Clientes: {self.total_clientes}
        Aparatos: {self.total_aparatos}
        Reservas: {self.total_reservas}
        Ingresos: €{self.total_ingresos:.2f}
        Deuda: €{self.deuda_total:.2f}
        Tasa de Pago: {self.porcentaje_pago:.1f}%
        """


@dataclass
class ResponseDTO:
    """DTO para respuestas del controlador"""
    exito: bool
    mensaje: str
    datos: Optional[dict] = None
    error_code: Optional[str] = None

    def __str__(self) -> str:
        estado = "✅" if self.exito else "❌"
        return f"{estado} {self.mensaje}"
