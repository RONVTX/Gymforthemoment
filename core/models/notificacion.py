import sqlite3
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class Notificacion:
    """Modelo para la entidad Notificación"""

    def __init__(self, db):
        self.db = db

    def crear_notificacion(self, id_cliente: int, id_reserva: int, tipo: str, mensaje: str) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO notificaciones (id_cliente, id_reserva, tipo, mensaje)
                           VALUES (?, ?, ?, ?)
                           ''', (id_cliente, id_reserva, tipo, mensaje))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error al crear notificación: {e}")
            return False

    def obtener_por_cliente(self, id_cliente: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id_notificacion, id_reserva, tipo, mensaje, leida, fecha_creacion
                       FROM notificaciones
                       WHERE id_cliente = ?
                       ORDER BY fecha_creacion DESC
                       ''', (id_cliente,))

        notificaciones = []
        for row in cursor.fetchall():
            notificaciones.append({
                'id': row[0],
                'id_reserva': row[1],
                'tipo': row[2],
                'mensaje': row[3],
                'leida': bool(row[4]),
                'fecha': row[5]
            })
        conn.close()
        return notificaciones

    def marcar_como_leida(self, id_notificacion: int) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           UPDATE notificaciones
                           SET leida = 1
                           WHERE id_notificacion = ?
                           ''', (id_notificacion,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error al marcar notificación como leída: {e}")
            return False

    def contar_no_leidas(self, id_cliente: int) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT COUNT(*)
                       FROM notificaciones
                       WHERE id_cliente = ? AND leida = 0
                       ''', (id_cliente,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def eliminar_notificacion(self, id_notificacion: int) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM notificaciones WHERE id_notificacion = ?', (id_notificacion,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error al eliminar notificación: {e}")
            return False
