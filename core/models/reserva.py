import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class Reserva:
    """Modelo para la entidad Reserva"""

    DIAS_SEMANA = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

    def __init__(self, db):
        self.db = db

    def crear_reserva(self, id_cliente: int, id_aparato: int, dia_semana: str,
                      hora_inicio: str) -> Tuple[bool, str]:
        if dia_semana not in self.DIAS_SEMANA:
            return False, "Día de la semana no válido"

        try:
            hora_obj = datetime.strptime(hora_inicio, "%H:%M")
            hora_fin_obj = hora_obj + timedelta(minutes=30)
            hora_fin = hora_fin_obj.strftime("%H:%M")
        except:
            return False, "Formato de hora inválido"

        if not self.verificar_disponibilidad(id_aparato, dia_semana, hora_inicio):
            return False, "El aparato no está disponible en ese horario"

        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO reservas (id_cliente, id_aparato, dia_semana, hora_inicio, hora_fin, estado)
                           VALUES (?, ?, ?, ?, ?, 'pendiente')
                           ''', (id_cliente, id_aparato, dia_semana, hora_inicio, hora_fin))
            conn.commit()
            conn.close()
            return True, "Solicitud de reserva enviada. El administrador la revisará"
        except Exception as e:
            return False, f"Error al crear reserva: {str(e)}"

    def verificar_disponibilidad(self, id_aparato: int, dia_semana: str, hora_inicio: str) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT COUNT(*)
                       FROM reservas
                       WHERE id_aparato = ?
                         AND dia_semana = ?
                         AND hora_inicio = ?
                         AND estado = 'aceptada'
                       ''', (id_aparato, dia_semana, hora_inicio))
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0

    def obtener_reservas_cliente(self, id_cliente: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT r.id_reserva, a.nombre, a.tipo, r.dia_semana, r.hora_inicio, r.hora_fin, r.fecha_reserva, r.estado
                       FROM reservas r
                                JOIN aparatos a ON r.id_aparato = a.id_aparato
                       WHERE r.id_cliente = ?
                       ORDER BY CASE r.dia_semana
                                    WHEN 'Lunes' THEN 1
                                    WHEN 'Martes' THEN 2
                                    WHEN 'Miércoles' THEN 3
                                    WHEN 'Jueves' THEN 4
                                    WHEN 'Viernes' THEN 5
                                    END,
                                r.hora_inicio
                       ''', (id_cliente,))

        reservas = []
        for row in cursor.fetchall():
            reservas.append({
                'id': row[0],
                'aparato': row[1],
                'tipo': row[2],
                'dia': row[3],
                'hora_inicio': row[4],
                'hora_fin': row[5],
                'fecha_reserva': row[6],
                'estado': row[7]
            })
        conn.close()
        return reservas

    def obtener_ocupacion_dia(self, dia_semana: str) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT a.nombre,
                              a.tipo,
                              r.hora_inicio,
                              r.hora_fin,
                              c.nombre || ' ' || c.apellido as cliente
                       FROM reservas r
                                JOIN aparatos a ON r.id_aparato = a.id_aparato
                                JOIN clientes c ON r.id_cliente = c.id_cliente
                       WHERE r.dia_semana = ?
                       ORDER BY a.nombre, r.hora_inicio
                       ''', (dia_semana,))

        ocupacion = []
        for row in cursor.fetchall():
            ocupacion.append({
                'aparato': row[0],
                'tipo': row[1],
                'hora_inicio': row[2],
                'hora_fin': row[3],
                'cliente': row[4]
            })
        conn.close()
        return ocupacion

    def obtener_todas(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT r.id_reserva,
                              c.nombre || ' ' || c.apellido,
                              a.nombre,
                              r.dia_semana,
                              r.hora_inicio,
                              r.hora_fin,
                              r.fecha_reserva,
                              r.estado
                       FROM reservas r
                                JOIN clientes c ON r.id_cliente = c.id_cliente
                                JOIN aparatos a ON r.id_aparato = a.id_aparato
                       ORDER BY r.fecha_reserva DESC, r.dia_semana, r.hora_inicio
                       ''')

        reservas = []
        for row in cursor.fetchall():
            reservas.append({
                'id': row[0],
                'cliente': row[1],
                'aparato': row[2],
                'dia': row[3],
                'hora_inicio': row[4],
                'hora_fin': row[5],
                'fecha': row[6],
                'estado': row[7]
            })
        conn.close()
        return reservas

    def obtener_reservas_por_aparato(self, id_aparato: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT r.id_reserva, r.id_aparato
                       FROM reservas r
                       WHERE r.id_aparato = ?
                       ''', (id_aparato,))

        reservas = []
        for row in cursor.fetchall():
            reservas.append({
                'id': row[0],
                'id_aparato': row[1]
            })
        conn.close()
        return reservas

    def eliminar_reserva(self, id_reserva: int) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM reservas WHERE id_reserva = ?', (id_reserva,))
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def aceptar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Obtener detalles de la reserva
            cursor.execute('''
                           SELECT id_cliente, id_aparato, dia_semana, hora_inicio, estado
                           FROM reservas
                           WHERE id_reserva = ?
                           ''', (id_reserva,))
            reserva = cursor.fetchone()
            
            if not reserva:
                conn.close()
                return False, "Reserva no encontrada"
            
            id_cliente, id_aparato, dia_semana, hora_inicio, estado = reserva
            
            if estado != 'pendiente':
                conn.close()
                return False, f"La reserva ya fue {estado}"
            
            # Verificar disponibilidad antes de aceptar
            if not self.verificar_disponibilidad(id_aparato, dia_semana, hora_inicio):
                conn.close()
                return False, "El aparato ya está reservado en ese horario"
            
            # Actualizar estado a aceptada
            cursor.execute('''
                           UPDATE reservas
                           SET estado = 'aceptada'
                           WHERE id_reserva = ?
                           ''', (id_reserva,))
            conn.commit()
            conn.close()
            
            return True, "Reserva aceptada exitosamente"
        except Exception as e:
            return False, f"Error al aceptar reserva: {str(e)}"

    def rechazar_reserva(self, id_reserva: int) -> Tuple[bool, str]:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Obtener detalles de la reserva
            cursor.execute('''
                           SELECT estado
                           FROM reservas
                           WHERE id_reserva = ?
                           ''', (id_reserva,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, "Reserva no encontrada"
            
            estado = result[0]
            
            if estado != 'pendiente':
                conn.close()
                return False, f"La reserva ya fue {estado}"
            
            # Actualizar estado a rechazada
            cursor.execute('''
                           UPDATE reservas
                           SET estado = 'rechazada'
                           WHERE id_reserva = ?
                           ''', (id_reserva,))
            conn.commit()
            conn.close()
            
            return True, "Reserva rechazada"
        except Exception as e:
            return False, f"Error al rechazar reserva: {str(e)}"

    def obtener_reservas_pendientes(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT r.id_reserva,
                              c.nombre || ' ' || c.apellido as cliente,
                              c.id_cliente,
                              a.nombre,
                              r.dia_semana,
                              r.hora_inicio,
                              r.hora_fin,
                              r.fecha_reserva
                       FROM reservas r
                                JOIN clientes c ON r.id_cliente = c.id_cliente
                                JOIN aparatos a ON r.id_aparato = a.id_aparato
                       WHERE r.estado = 'pendiente'
                       ORDER BY r.fecha_reserva ASC
                       ''')

        reservas = []
        for row in cursor.fetchall():
            reservas.append({
                'id': row[0],
                'cliente': row[1],
                'id_cliente': row[2],
                'aparato': row[3],
                'dia': row[4],
                'hora_inicio': row[5],
                'hora_fin': row[6],
                'fecha': row[7]
            })
        conn.close()
        return reservas

    def obtener_id_cliente_por_reserva(self, id_reserva: int) -> Optional[int]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id_cliente
                       FROM reservas
                       WHERE id_reserva = ?
                       ''', (id_reserva,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
