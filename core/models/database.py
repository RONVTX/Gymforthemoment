import sqlite3
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Database:
    """Clase para gestionar la conexión y la inicialización de la base de datos.
    
    Responsable de crear las tablas necesarias y mantener la conexión
    con SQLite.
    """

    def __init__(self, db_name: str = "gimnasio.db"):
        """Inicializa la conexión a la base de datos.
        
        Args:
            db_name: Nombre del archivo de base de datos
        """
        self.db_name = db_name
        self.initialize_database()
        logger.info(f"Base de datos inicializada: {db_name}")

    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos.
        
        Returns:
            Conexión a SQLite
        """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
        return conn

    def initialize_database(self):
        """Crea las tablas si no existen"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Tabla Clientes
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS clientes
                       (
                           id_cliente
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           nombre
                           TEXT
                           NOT
                           NULL,
                           apellido
                           TEXT
                           NOT
                           NULL,
                           dni
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           telefono
                           TEXT,
                           email
                           TEXT,
                           tipo_usuario
                           TEXT
                           NOT
                           NULL
                           CHECK (
                           tipo_usuario
                           IN
                       (
                           'cliente',
                           'admin'
                       )),
                           password TEXT NOT NULL,
                           fecha_registro DATE DEFAULT CURRENT_DATE
                           )
                       ''')

        # Tabla Aparatos
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS aparatos
                       (
                           id_aparato
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           nombre
                           TEXT
                           NOT
                           NULL,
                           tipo
                           TEXT
                           NOT
                           NULL,
                           descripcion
                           TEXT
                       )
                       ''')

        # Tabla Reservas
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS reservas
                       (
                           id_reserva
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           id_cliente
                           INTEGER
                           NOT
                           NULL,
                           id_aparato
                           INTEGER
                           NOT
                           NULL,
                           dia_semana
                           TEXT
                           NOT
                           NULL
                           CHECK (
                           dia_semana
                           IN
                       (
                           'Lunes',
                           'Martes',
                           'Miércoles',
                           'Jueves',
                           'Viernes'
                       )),
                           hora_inicio TEXT NOT NULL,
                           hora_fin TEXT NOT NULL,
                           fecha_reserva DATE DEFAULT CURRENT_DATE,
                           estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'aceptada', 'rechazada')),
                           FOREIGN KEY
                       (
                           id_cliente
                       ) REFERENCES clientes
                       (
                           id_cliente
                       ) ON DELETE CASCADE,
                           FOREIGN KEY
                       (
                           id_aparato
                       ) REFERENCES aparatos
                       (
                           id_aparato
                       )
                         ON DELETE CASCADE
                           )
                       ''')

        # Tabla Recibos
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS recibos
                       (
                           id_recibo
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           id_cliente
                           INTEGER
                           NOT
                           NULL,
                           mes
                           INTEGER
                           NOT
                           NULL,
                           anio
                           INTEGER
                           NOT
                           NULL,
                           monto
                           REAL
                           NOT
                           NULL
                           DEFAULT
                           50.0,
                           fecha_emision
                           DATE
                           DEFAULT
                           CURRENT_DATE,
                           estado
                           TEXT
                           NOT
                           NULL
                           DEFAULT
                           'pendiente'
                           CHECK (
                           estado
                           IN
                       (
                           'pendiente',
                           'pagado'
                       )),
                           FOREIGN KEY
                       (
                           id_cliente
                       ) REFERENCES clientes
                       (
                           id_cliente
                       ) ON DELETE CASCADE,
                           UNIQUE
                       (
                           id_cliente,
                           mes,
                           anio
                       )
                           )
                       ''')

        # Tabla Pagos
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS pagos
                       (
                           id_pago
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           id_recibo
                           INTEGER
                           NOT
                           NULL,
                           fecha_pago
                           DATE
                           DEFAULT
                           CURRENT_DATE,
                           monto
                           REAL
                           NOT
                           NULL,
                           metodo_pago
                           TEXT,
                           FOREIGN
                           KEY
                       (
                           id_recibo
                       ) REFERENCES recibos
                       (
                           id_recibo
                       ) ON DELETE CASCADE
                           )
                       ''')

        # Tabla Notificaciones
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS notificaciones
                       (
                           id_notificacion
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           id_cliente
                           INTEGER
                           NOT
                           NULL,
                           id_reserva
                           INTEGER,
                           tipo
                           TEXT
                           NOT
                           NULL
                           CHECK (
                           tipo
                           IN
                       (
                           'aceptada',
                           'rechazada'
                       )),
                           mensaje
                           TEXT
                           NOT
                           NULL,
                           leida
                           BOOLEAN
                           DEFAULT
                           0,
                           fecha_creacion
                           DATETIME
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           FOREIGN KEY
                       (
                           id_cliente
                       ) REFERENCES clientes
                       (
                           id_cliente
                       ) ON DELETE CASCADE,
                           FOREIGN KEY
                       (
                           id_reserva
                       ) REFERENCES reservas
                       (
                           id_reserva
                       ) ON DELETE CASCADE
                           )
                       ''')

        conn.commit()

        # Crear usuario admin por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE tipo_usuario = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                           INSERT INTO clientes (nombre, apellido, dni, telefono, email, tipo_usuario, password)
                           VALUES ('Admin', 'Sistema', 'admin123', '000000000', 'admin@gym.com', 'admin', 'admin123')
                           ''')
            conn.commit()

        conn.close()
        
        # Ejecutar migraciones
        self._execute_migrations()

    def _execute_migrations(self):
        """Ejecuta migraciones necesarias para actualizar la base de datos existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Migración 1: Agregar columna 'estado' a la tabla reservas si no existe
            cursor.execute("PRAGMA table_info(reservas)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'estado' not in columns:
                logger.info("Agregando columna 'estado' a tabla reservas...")
                cursor.execute('''
                    ALTER TABLE reservas 
                    ADD COLUMN estado TEXT NOT NULL DEFAULT 'pendiente' 
                    CHECK (estado IN ('pendiente', 'aceptada', 'rechazada'))
                ''')
                conn.commit()
                logger.info("Columna 'estado' agregada exitosamente")
            
            # Migración 2: Verificar que existe la tabla notificaciones
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notificaciones'")
            if not cursor.fetchone():
                logger.info("Creando tabla notificaciones...")
                cursor.execute('''
                    CREATE TABLE notificaciones
                    (
                        id_notificacion INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL,
                        id_reserva INTEGER,
                        tipo TEXT NOT NULL CHECK (tipo IN ('aceptada', 'rechazada')),
                        mensaje TEXT NOT NULL,
                        leida BOOLEAN DEFAULT 0,
                        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
                        FOREIGN KEY(id_reserva) REFERENCES reservas(id_reserva) ON DELETE CASCADE
                    )
                ''')
                conn.commit()
                logger.info("Tabla notificaciones creada exitosamente")
                
        except Exception as e:
            logger.error(f"Error ejecutando migraciones: {e}")
        finally:
            conn.close()
