# 🔍 Referencia Rápida - MVC Avanzado

## 📚 Documentación del Proyecto

| Archivo | Propósito | Mejor para |
|---------|-----------|-----------|
| README.md | Descripción general | Nuevos desarrolladores |
| ESTRUCTURA.md | Estructura actual | Entender directorios |
| MEJORAS.md | Ideas futuras | Planificación |
| **RESUMEN_EJECUTIVO.md** | Overview completo | Gestores/Leads |
| **REFACTOREO_MVC_AVANZADO.md** | Detalle técnico del refactoreo | Desarrolladores |
| **GUIA_INTEGRACION_DTOS.md** | Cómo integrar DTOs | Próxima fase |
| **ESTADO_PROYECTO.md** | Estado actual y roadmap | Planificación |
| **Este archivo** | Referencia rápida | Todos |

## 🎯 Módulos Principales

### `exceptions.py` (Manejo de Errores)
```python
# Jerárquía
GymException (base)
├── AuthenticationError      # Fallo de login
├── AuthorizationError       # Falta de permisos
├── ValidationError          # Input inválido
├── NotFoundError            # Recurso no existe
├── BusinessLogicError       # Violación de regla
└── DatabaseError            # Error BD

# Uso
try:
    # código
except ValidationError as e:
    logger.warning(f"Validación: {e}")
except NotFoundError as e:
    logger.warning(f"No encontrado: {e}")
```

### `validators.py` (Validación Centralizada)
```python
# Base - Métodos estáticos
Validador.validar_dni(dni)
Validador.validar_email(email)
Validador.validar_telefono(telefono)
Validador.validar_nombre(nombre)
Validador.validar_password(password)
Validador.validar_tipo_usuario(tipo)
Validador.validar_dia_semana(dia)
Validador.validar_hora(hora)
Validador.validar_mes(mes)
Validador.validar_anio(anio)
Validador.validar_monto(monto)
Validador.validar_campos_no_vacios(*campos)

# Especializadas
ValidadorCliente.validar_datos_registro(...)
ValidadorReserva.validar_datos_reserva(...)
ValidadorAparato.validar_datos_aparato(...)

# Uso
try:
    Validador.validar_email("test@example.com")
    ValidadorCliente.validar_datos_registro(nombre, apellido, dni, password, email, tel)
except ValidationError as e:
    print(f"Error: {e}")
```

### `dtos.py` (Data Transfer Objects)
```python
# Estructuras de datos
@dataclass
UsuarioDTO(id, nombre, apellido, dni, email, telefono, tipo, fecha_registro)
AparatoDTO(id, nombre, tipo, descripcion)
ReservaDTO(id, cliente, aparato, dia, hora_inicio, hora_fin, fecha_reserva)
ReciboDTO(id, cliente, mes, anio, monto, estado, fecha_emision)
EstadisticasDTO(total_clientes, total_admins, total_aparatos, ...)
ResponseDTO(exito, mensaje, datos, error_code)

# Uso
usuario = UsuarioDTO(
    id=1, nombre="Juan", apellido="Pérez", dni="12345678",
    email="juan@example.com", telefono="555-1234",
    tipo="cliente", fecha_registro="2024-01-15"
)
print(usuario.get_nombre_completo())  # "Juan Pérez"

# Convertir a dict (para JSON)
from dataclasses import asdict
dict_data = asdict(usuario)
```

## 🔧 Métodos Refactorizados del Controlador

### Patrón Establecido
```python
def metodo(self, param1, param2) -> ReturnType:
    """Descripción."""
    # 1. Validar permisos (si aplica)
    if not self._requiere_admin():
        return error_response()
    
    # 2. Try-except principal
    try:
        # 3. Validar inputs
        Validador.validar_xxx(param1)
        ValidadorXXX.validar_datos_xxx(param1, param2)
        
        # 4. Verificar existencia de recursos
        recurso = self.model.buscar(id)
        if not recurso:
            raise NotFoundError("Mensaje")
        
        # 5. Lógica de negocio
        resultado = self.model.operacion()
        if resultado:
            logger.info("Éxito")
            return True, "Mensaje exitoso"
        else:
            raise DatabaseError("Error")
    
    # 6. Manejo de excepciones (ORDEN IMPORTA)
    except ValidationError as e:
        logger.warning(f"Validación: {e}")
        return False, str(e)
    except NotFoundError as e:
        logger.warning(f"No encontrado: {e}")
        return False, str(e)
    except BusinessLogicError as e:
        logger.warning(f"Negocio: {e}")
        return False, str(e)
    except DatabaseError as e:
        logger.error(f"BD: {e}")
        return False, "Error en la operación"
    except Exception as e:
        logger.error(f"Inesperado: {e}")
        return False, "Error inesperado"
```

### Lista de Métodos Refactorizados
1. ✅ `login()` - AuthenticationError
2. ✅ `registrar_usuario()` - ValidadorCliente
3. ✅ `crear_cliente_admin()` - ValidadorCliente + validar_tipo
4. ✅ `crear_aparato()` - ValidadorAparato
5. ✅ `crear_reserva()` - ValidadorReserva + NotFoundError
6. ✅ `obtener_ocupacion_dia()` - validar_dia_semana
7. ✅ `eliminar_reserva()` - DatabaseError
8. ✅ `verificar_disponibilidad()` - Validaciones
9. ✅ `pagar_recibo()` - Multi-exception
10. ✅ `generar_recibos_mes()` - validar_mes/anio
11. ✅ `eliminar_aparato()` - NotFoundError + BusinessLogicError

## 📋 Códigos de Error Estándar

**Éxito:**
- `"OK"` - Operación completada

**Validación:**
- `"VALIDATION_ERROR"` - Error general de validación
- `"INVALID_DNI"` - DNI inválido
- `"INVALID_EMAIL"` - Email inválido
- `"INVALID_PHONE"` - Teléfono inválido
- `"EMPTY_FIELDS"` - Campos vacíos

**Autenticación:**
- `"AUTHENTICATION_ERROR"` - Fallo de login
- `"INVALID_CREDENTIALS"` - Credenciales incorrectas

**Autorización:**
- `"AUTHORIZATION_ERROR"` - Falta de permisos
- `"ADMIN_REQUIRED"` - Se requiere admin

**Recurso:**
- `"NOT_FOUND"` - Recurso no encontrado
- `"USER_NOT_FOUND"` - Usuario no encontrado
- `"APARATO_NOT_FOUND"` - Aparato no encontrado

**Lógica de Negocio:**
- `"BUSINESS_ERROR"` - Error de lógica
- `"DUPLICATE_ENTRY"` - Entrada duplicada
- `"ALREADY_PAID"` - Ya pagado
- `"INVALID_STATE"` - Estado inválido

**Base de Datos:**
- `"DATABASE_ERROR"` - Error BD
- `"OPERATION_FAILED"` - Operación fallida

## 🚀 Cómo Agregar Funcionalidad Nueva

### 1. Crear Validador si no existe
```python
# En validators.py
class ValidadorNuevo(Validador):
    @staticmethod
    def validar_datos_nuevo(param1, param2):
        """Valida datos de nuevo."""
        Validador.validar_nombre(param1)
        if not param2 > 0:
            raise ValidationError("Param2 debe ser positivo")
```

### 2. Agregar Excepción si es necesaria
```python
# En exceptions.py
class NuevaExcepcion(GymException):
    """Nueva excepción específica."""
    pass
```

### 3. Crear DTO si hay nuevo dato
```python
# En dtos.py
@dataclass
class NuevoDTO:
    campo1: str
    campo2: int
    
    def metodo_helper(self):
        return f"{self.campo1}: {self.campo2}"
```

### 4. Refactorizar método en controller
```python
# En core/controller/gym_controller.py
def nuevo_metodo(self, param1: str, param2: int) -> Tuple[bool, str]:
    """Descripción completa."""
    try:
        ValidadorNuevo.validar_datos_nuevo(param1, param2)
        resultado = self.model.operacion(param1, param2)
        if resultado:
            logger.info(f"Operación exitosa")
            return True, "Mensaje de éxito"
        else:
            raise DatabaseError("Error BD")
    except ValidationError as e:
        logger.warning(f"Validación: {e}")
        return False, str(e)
    except DatabaseError as e:
        logger.error(f"BD: {e}")
        return False, "Error en la operación"
    except Exception as e:
        logger.error(f"Error: {e}")
        return False, "Error inesperado"
```

## 🧪 Testing Rápido

### Test de Validador
```python
import unittest
from validators import Validador, ValidationError

class TestValidador(unittest.TestCase):
    def test_email_valido(self):
        # No debe lanzar excepción
        Validador.validar_email("test@example.com")
    
    def test_email_invalido(self):
        with self.assertRaises(ValidationError):
            Validador.validar_email("invalid-email")
    
    def test_dni_valido(self):
        Validador.validar_dni("12345678")
    
    def test_dni_invalido(self):
        with self.assertRaises(ValidationError):
            Validador.validar_dni("123")  # Muy corto
```

### Test de Método
```python
def test_login_exitoso(self):
    controller = Controlador()
    controller.cliente_model.autenticar = Mock(return_value={
        'id': 1, 'nombre': 'Juan', 'dni': '12345678',
        'email': 'juan@example.com', 'telefono': '555-1234',
        'tipo': 'cliente', 'fecha_registro': '2024-01-15'
    })
    
    success, msg, user = controller.login("12345678", "password123")
    assert success == True
    assert user['nombre'] == 'Juan'

def test_login_credenciales_invalidas(self):
    controller = Controlador()
    controller.cliente_model.autenticar = Mock(return_value=None)
    
    success, msg, user = controller.login("12345678", "wrongpass")
    assert success == False
    assert user is None
```

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| Métodos refactorizados | 11 |
| Excepciones nuevas | 7 |
| DTOs creados | 6 |
| Validadores | 4 clases |
| Métodos de validación | 15+ |
| Líneas de documentación | 100+ |
| Archivos nuevos | 3 |
| Archivos modificados | 1 |
| Compilación | ✅ PASS |

## 🐛 Debugging Común

**Problema**: `ValidationError: El DNI debe tener 8 dígitos`
```python
# Verificar input
print(f"DNI recibido: '{dni}' (tipo: {type(dni)})")
# Asegurarse que es string y tiene 8 caracteres
dni = str(dni).strip()
```

**Problema**: `NotFoundError: Usuario con ID X no encontrado`
```python
# Verificar que recurso existe antes de operación
usuario = self.modelo.buscar(id)
if not usuario:
    raise NotFoundError(f"Usuario {id} no existe")
```

**Problema**: `DatabaseError: Error al registrar en BD`
```python
# Revisar logs para error específico
logger.error(f"Error BD: {e}")  # Ver qué error específico es
# Verificar que modelo retorna True/False correctamente
```

## 🎓 Principios Aplicados

1. **SRP** (Single Responsibility Principle)
   - Cada clase/función tiene una responsabilidad

2. **DRY** (Don't Repeat Yourself)
   - Validación centralizada = cambio único

3. **SOLID**
   - Segregación de interfaces
   - Inversión de dependencias

4. **KISS** (Keep It Simple, Stupid)
   - Código claro y fácil de entender

5. **YAGNI** (You Aren't Gonna Need It)
   - No sobre-ingeniería

## 📚 Lectura Recomendada

- Clean Code (Robert C. Martin)
- Design Patterns (Gang of Four)
- Refactoring (Martin Fowler)
- Test Driven Development (Kent Beck)

## 🔗 Links Útiles

- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Python Exception Hierarchy](https://docs.python.org/3/tutorial/errors.html)
- [Type Hints](https://docs.python.org/3/library/typing.html)

## 📞 Soporte Rápido

**¿Cómo agrego un validador?**
→ Ver `validators.py` y crear método en Validador o subclase

**¿Cómo agrego una excepción?**
→ Ver `exceptions.py` y extender GymException

**¿Cómo creo un DTO?**
→ Ver `dtos.py` y usar @dataclass

**¿Cómo refactorizo un método?**
→ Seguir patrón en `core/controller/gym_controller.py` métodos refactorizados

**¿Dónde está la documentación?**
→ REFACTOREO_MVC_AVANZADO.md para detalles
→ GUIA_INTEGRACION_DTOS.md para próxima fase
→ ESTADO_PROYECTO.md para visión general

---

**Última actualización**: 2024
**Versión**: MVC Avanzado v1.0
