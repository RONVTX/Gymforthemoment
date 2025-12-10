import sqlite3
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Recibo:
    """Modelo para la entidad Recibo"""

    MONTO_MENSUAL = 50.0

    def __init__(self, db):
        self.db = db

    def generar_recibos_mes(self, mes: int, anio: int) -> int:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_cliente FROM clientes WHERE tipo_usuario = 'cliente'")
        clientes = cursor.fetchall()

        generados = 0
        for (id_cliente,) in clientes:
            try:
                cursor.execute('''
                               INSERT INTO recibos (id_cliente, mes, anio, monto)
                               VALUES (?, ?, ?, ?)
                               ''', (id_cliente, mes, anio, self.MONTO_MENSUAL))
                generados += 1
            except sqlite3.IntegrityError:
                pass

        conn.commit()
        conn.close()
        return generados

    def obtener_recibos_cliente(self, id_cliente: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id_recibo, mes, anio, monto, fecha_emision, estado
                       FROM recibos
                       WHERE id_cliente = ?
                       ORDER BY anio DESC, mes DESC
                       ''', (id_cliente,))

        recibos = []
        for row in cursor.fetchall():
            recibos.append({
                'id': row[0],
                'mes': row[1],
                'anio': row[2],
                'monto': row[3],
                'fecha_emision': row[4],
                'estado': row[5]
            })
        conn.close()
        return recibos

    def obtener_por_id(self, id_recibo: int) -> Optional[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT id_recibo, id_cliente, mes, anio, monto, fecha_emision, estado
                       FROM recibos
                       WHERE id_recibo = ?
                       ''', (id_recibo,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'id': result[0],
                'id_cliente': result[1],
                'mes': result[2],
                'anio': result[3],
                'monto': result[4],
                'fecha_emision': result[5],
                'estado': result[6]
            }
        return None

    def marcar_pagado(self, id_recibo: int) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           UPDATE recibos
                           SET estado = 'pagado'
                           WHERE id_recibo = ?
                           ''', (id_recibo,))
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def registrar_pago(self, id_recibo: int, monto: float, metodo_pago: str = "Efectivo") -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                           INSERT INTO pagos (id_recibo, monto, metodo_pago)
                           VALUES (?, ?, ?)
                           ''', (id_recibo, monto, metodo_pago))

            cursor.execute('''
                           UPDATE recibos
                           SET estado = 'pagado'
                           WHERE id_recibo = ?
                           ''', (id_recibo,))

            conn.commit()
            conn.close()
            return True
        except:
            return False

    def obtener_morosos(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT DISTINCT c.id_cliente,
                                       c.nombre,
                                       c.apellido,
                                       c.dni,
                                       c.telefono,
                                       COUNT(r.id_recibo) as recibos_pendientes,
                                       SUM(r.monto)       as deuda_total
                       FROM clientes c
                                JOIN recibos r ON c.id_cliente = r.id_cliente
                       WHERE r.estado = 'pendiente'
                       GROUP BY c.id_cliente
                       ORDER BY deuda_total DESC
                       ''')

        morosos = []
        for row in cursor.fetchall():
            morosos.append({
                'id': row[0],
                'nombre': row[1],
                'apellido': row[2],
                'dni': row[3],
                'telefono': row[4],
                'recibos_pendientes': row[5],
                'deuda_total': row[6]
            })
        conn.close()
        return morosos

    def obtener_todos_recibos(self) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT r.id_recibo,
                              r.id_cliente,
                              c.nombre || ' ' || c.apellido,
                              r.mes,
                              r.anio,
                              r.monto,
                              r.estado,
                              r.fecha_emision
                       FROM recibos r
                                JOIN clientes c ON r.id_cliente = c.id_cliente
                       ORDER BY r.anio DESC, r.mes DESC, c.apellido
                       ''')

        recibos = []
        for row in cursor.fetchall():
            recibos.append({
                'id': row[0],
                'id_cliente': row[1],
                'cliente': row[2],
                'mes': row[3],
                'anio': row[4],
                'monto': row[5],
                'estado': row[6],
                'fecha': row[7]
            })
        conn.close()
        return recibos
