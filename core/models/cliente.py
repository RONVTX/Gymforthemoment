import sqlite3
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Cliente:
    """Modelo para la entidad Cliente.
    
    Gestiona todas las operaciones relacionadas con clientes,
    incluyendo autenticación y registro.
    """

    def __init__(self, db):
        self.db = db

    def crear_cliente(self, nombre: str, apellido: str, dni: str, telefono: str,
                      email: str, password: str, tipo_usuario: str = 'cliente') -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO clientes (nombre, apellido, dni, telefono, email, tipo_usuario, password)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           ''', (nombre, apellido, dni, telefono, email, tipo_usuario, password))
            conn.commit()
            conn.close()
            logger.info(f"Cliente creado: {dni} ({tipo_usuario})")
            return True
        except sqlite3.IntegrityError as e:
            logger.warning(f"Error al crear cliente (DNI duplicado?): {dni}")
            return False
        except Exception as e:
            logger.error(f"Error al crear cliente: {e}")
            return False

    def dni_existe(self, dni: str) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM clientes WHERE dni = ?', (dni,))
            existe = cursor.fetchone()[0] > 0
            conn.close()
            return existe
        except Exception as e:
            logger.error(f"Error al verificar DNI: {e}")
            return False

    def autenticar(self, dni: str, password: str) -> Optional[Dict]:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT id_cliente, nombre, apellido, dni, tipo_usuario
                           FROM clientes
                           WHERE dni = ?
                             AND password = ?
                           ''', (dni, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                logger.info(f"Autenticación exitosa: {dni}")
                return {
                    'id': result[0],
                    'nombre': result[1],
                    'apellido': result[2],
                    'dni': result[3],
                    'tipo': result[4]
                }
            else:
                logger.warning(f"Fallo de autenticación: {dni}")
                return None
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            return None

    def obtener_todos(self) -> List[Dict]:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT id_cliente,
                                  nombre,
                                  apellido,
                                  dni,
                                  telefono,
                                  email,
                                  tipo_usuario,
                                  fecha_registro
                           FROM clientes
                           ORDER BY apellido, nombre
                           ''')
            clientes = []
            for row in cursor.fetchall():
                clientes.append({
                    'id': row[0],
                    'nombre': row[1],
                    'apellido': row[2],
                    'dni': row[3],
                    'telefono': row[4],
                    'email': row[5],
                    'tipo': row[6],
                    'fecha_registro': row[7]
                })
            conn.close()
            return clientes
        except Exception as e:
            logger.error(f"Error al obtener clientes: {e}")
            return []

    def obtener_por_id(self, id_cliente: int) -> Optional[Dict]:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT id_cliente, nombre, apellido, dni, telefono, email, tipo_usuario
                           FROM clientes
                           WHERE id_cliente = ?
                           ''', (id_cliente,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'id': result[0],
                    'nombre': result[1],
                    'apellido': result[2],
                    'dni': result[3],
                    'telefono': result[4],
                    'email': result[5],
                    'tipo': result[6]
                }
            return None
        except Exception as e:
            logger.error(f"Error al obtener cliente por ID: {e}")
            return None
