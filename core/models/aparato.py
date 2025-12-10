import sqlite3
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Aparato:
    """Modelo para la entidad Aparato.
    
    Gestiona todas las operaciones relacionadas con aparatos del gimnasio,
    incluyendo creación, obtención y eliminación.
    """

    def __init__(self, db):
        self.db = db

    def crear_aparato(self, nombre: str, tipo: str, descripcion: str = "") -> int:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO aparatos (nombre, tipo, descripcion)
                           VALUES (?, ?, ?)
                           ''', (nombre, tipo, descripcion))
            id_aparato = cursor.lastrowid
            conn.commit()
            conn.close()
            logger.info(f"Aparato creado: {nombre} (ID: {id_aparato})")
            return id_aparato
        except Exception as e:
            logger.error(f"Error al crear aparato: {e}")
            return 0

    def obtener_todos(self) -> List[Dict]:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT id_aparato, nombre, tipo, descripcion 
                           FROM aparatos 
                           ORDER BY tipo, nombre
                           ''')
            aparatos = []
            for row in cursor.fetchall():
                aparatos.append({
                    'id': row[0],
                    'nombre': row[1],
                    'tipo': row[2],
                    'descripcion': row[3]
                })
            conn.close()
            return aparatos
        except Exception as e:
            logger.error(f"Error al obtener aparatos: {e}")
            return []

    def obtener_por_id(self, id_aparato: int) -> Optional[Dict]:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT id_aparato, nombre, tipo, descripcion 
                           FROM aparatos 
                           WHERE id_aparato = ?
                           ''', (id_aparato,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'id': result[0],
                    'nombre': result[1],
                    'tipo': result[2],
                    'descripcion': result[3]
                }
            return None
        except Exception as e:
            logger.error(f"Error al obtener aparato: {e}")
            return None

    def eliminar_aparato(self, id_aparato: int) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM aparatos WHERE id_aparato = ?', (id_aparato,))
            conn.commit()
            conn.close()
            logger.info(f"Aparato eliminado: ID {id_aparato}")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar aparato: {e}")
            return False
