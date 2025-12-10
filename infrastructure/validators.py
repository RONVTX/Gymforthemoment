"""
Validadores para garantizar integridad de datos.
Centraliza todas las reglas de validación del negocio.
"""

import re
from infrastructure.exceptions import ValidationError


class Validador:
    """Clase base para validadores"""

    @staticmethod
    def validar_dni(dni: str) -> bool:
        """Valida formato del DNI"""
        if not dni or len(dni) < 3:
            raise ValidationError("DNI inválido: debe tener al menos 3 caracteres")
        return True

    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida formato del email"""
        if not email:
            return True  # Email es opcional
        
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise ValidationError("Email inválido")
        return True

    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """Valida formato del teléfono"""
        if not telefono:
            return True  # Teléfono es opcional
        
        if not re.match(r'^\d{6,20}$', telefono.replace('+', '').replace('-', '').replace(' ', '')):
            raise ValidationError("Teléfono inválido")
        return True

    @staticmethod
    def validar_nombre(nombre: str, min_length: int = 2) -> bool:
        """Valida nombre"""
        if not nombre or len(nombre.strip()) < min_length:
            raise ValidationError(f"Nombre debe tener al menos {min_length} caracteres")
        return True

    @staticmethod
    def validar_password(password: str, min_length: int = 4) -> bool:
        """Valida contraseña"""
        if not password or len(password) < min_length:
            raise ValidationError(f"Contraseña debe tener al menos {min_length} caracteres")
        return True

    @staticmethod
    def validar_tipo_usuario(tipo: str) -> bool:
        """Valida tipo de usuario"""
        tipos_validos = ['cliente', 'admin']
        if tipo not in tipos_validos:
            raise ValidationError(f"Tipo de usuario inválido. Debe ser uno de: {', '.join(tipos_validos)}")
        return True

    @staticmethod
    def validar_dia_semana(dia: str) -> bool:
        """Valida día de la semana"""
        dias_validos = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        if dia not in dias_validos:
            raise ValidationError(f"Día no válido. Debe ser uno de: {', '.join(dias_validos)}")
        return True

    @staticmethod
    def validar_hora(hora: str) -> bool:
        """Valida formato de hora HH:MM"""
        if not re.match(r'^\d{2}:\d{2}$', hora):
            raise ValidationError("Hora inválida. Formato: HH:MM")
        
        try:
            horas, minutos = map(int, hora.split(':'))
            if horas < 0 or horas > 23 or minutos < 0 or minutos > 59:
                raise ValidationError("Hora fuera de rango (00:00 - 23:59)")
        except ValueError:
            raise ValidationError("Hora inválida")
        
        return True

    @staticmethod
    def validar_mes(mes: int) -> bool:
        """Valida número de mes"""
        if mes < 1 or mes > 12:
            raise ValidationError("Mes debe estar entre 1 y 12")
        return True

    @staticmethod
    def validar_anio(anio: int) -> bool:
        """Valida número de año"""
        if anio < 2020 or anio > 2100:
            raise ValidationError("Año debe estar entre 2020 y 2100")
        return True

    @staticmethod
    def validar_monto(monto: float) -> bool:
        """Valida monto de dinero"""
        if monto <= 0:
            raise ValidationError("Monto debe ser mayor a 0")
        return True

    @staticmethod
    def validar_campos_no_vacios(*campos) -> bool:
        """Valida que campos no estén vacíos"""
        for campo in campos:
            if not campo or (isinstance(campo, str) and not campo.strip()):
                raise ValidationError("Todos los campos son obligatorios")
        return True


class ValidadorCliente(Validador):
    """Validaciones específicas para clientes"""

    @staticmethod
    def validar_datos_registro(nombre: str, apellido: str, dni: str, 
                               password: str, email: str = None, telefono: str = None) -> bool:
        """Valida datos completos de registro"""
        Validador.validar_nombre(nombre)
        Validador.validar_nombre(apellido)
        Validador.validar_dni(dni)
        Validador.validar_password(password)
        
        if email:
            Validador.validar_email(email)
        if telefono:
            Validador.validar_telefono(telefono)
        
        return True


class ValidadorReserva(Validador):
    """Validaciones específicas para reservas"""

    @staticmethod
    def validar_datos_reserva(id_aparato: int, dia_semana: str, hora_inicio: str) -> bool:
        """Valida datos de reserva"""
        if not id_aparato or id_aparato <= 0:
            raise ValidationError("ID de aparato inválido")
        
        Validador.validar_dia_semana(dia_semana)
        Validador.validar_hora(hora_inicio)
        
        return True


class ValidadorAparato(Validador):
    """Validaciones específicas para aparatos"""

    @staticmethod
    def validar_datos_aparato(nombre: str, tipo: str, descripcion: str = None) -> bool:
        """Valida datos de aparato"""
        Validador.validar_nombre(nombre)
        
        if not tipo or len(tipo.strip()) < 2:
            raise ValidationError("Tipo debe tener al menos 2 caracteres")
        
        return True
