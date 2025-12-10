# 📋 Guía: Integración de DTOs en Respuestas del Controlador

## Objetivo
Modernizar todas las respuestas del controlador para usar `ResponseDTO` en lugar de tuplas simples `(bool, str)`.

## Estado Actual vs. Objetivo

### ACTUAL (Tuplas simples)
```python
def crear_cliente_admin(self, ...) -> Tuple[bool, str]:
    try:
        # ... lógica ...
        return True, "Cliente creado exitosamente"
    except ValidationError as e:
        return False, str(e)
```

### OBJETIVO (DTOs)
```python
def crear_cliente_admin(self, ...) -> ResponseDTO:
    try:
        # ... lógica ...
        cliente_dto = UsuarioDTO(...)
        return ResponseDTO(
            exito=True,
            mensaje="Cliente creado exitosamente",
            datos=asdict(cliente_dto),  # Convertir a dict
            error_code="OK"
        )
    except ValidationError as e:
        return ResponseDTO(
            exito=False,
            mensaje=str(e),
            datos=None,
            error_code="VALIDATION_ERROR"
        )
```

## Códigos de Error Estandarizados

```python
# Códigos de éxito
"OK"                     # Operación exitosa

# Códigos de validación
"VALIDATION_ERROR"       # Error de validación general
"INVALID_DNI"            # DNI inválido
"INVALID_EMAIL"          # Email inválido
"INVALID_PHONE"          # Teléfono inválido
"EMPTY_FIELDS"           # Campos vacíos

# Códigos de autenticación
"AUTHENTICATION_ERROR"   # Fallo de autenticación
"INVALID_CREDENTIALS"    # Credenciales inválidas

# Códigos de autorización
"AUTHORIZATION_ERROR"    # Falta de permisos
"ADMIN_REQUIRED"         # Se requiere permisos de admin

# Códigos de recurso
"NOT_FOUND"              # Recurso no encontrado
"USER_NOT_FOUND"         # Usuario no encontrado
"APARATO_NOT_FOUND"      # Aparato no encontrado

# Códigos de lógica de negocio
"BUSINESS_ERROR"         # Error de lógica de negocio
"DUPLICATE_ENTRY"        # Entrada duplicada
"ALREADY_PAID"           # Ya está pagado
"INVALID_STATE"          # Estado inválido

# Códigos de base de datos
"DATABASE_ERROR"         # Error de base de datos
"OPERATION_FAILED"       # Operación fallida
```

## Metodología de Migración

### Paso 1: Actualizar Importaciones
```python
from dtos import ResponseDTO, UsuarioDTO, AparatoDTO, ReservaDTO, ReciboDTO
from dataclasses import asdict
```

### Paso 2: Actualizar Firma del Método
```python
# ANTES
def crear_cliente_admin(self, ...) -> Tuple[bool, str]:

# DESPUÉS
def crear_cliente_admin(self, ...) -> ResponseDTO:
```

### Paso 3: Actualizar Returns con Éxito
```python
# ANTES
return True, "Cliente creado exitosamente"

# DESPUÉS
cliente_dto = UsuarioDTO(
    id=id_cliente,
    nombre=nombre,
    apellido=apellido,
    dni=dni,
    email=email,
    telefono=telefono,
    tipo=tipo,
    fecha_registro=datetime.now().strftime("%Y-%m-%d")
)
return ResponseDTO(
    exito=True,
    mensaje="Cliente creado exitosamente",
    datos=asdict(cliente_dto),
    error_code="OK"
)
```

### Paso 4: Actualizar Returns de Error
```python
# ANTES
except ValidationError as e:
    return False, str(e)

# DESPUÉS
except ValidationError as e:
    logger.warning(f"Error de validación: {e}")
    return ResponseDTO(
        exito=False,
        mensaje=str(e),
        datos=None,
        error_code="VALIDATION_ERROR"
    )
```

## Métodos a Migrar Fase 1 (Con datos)

Estos métodos retornan datos y deben usar DTOs:

### Gestión de Usuarios
- [ ] `login()` → Retorna UsuarioDTO
- [ ] `registrar_usuario()` → Retorna UsuarioDTO
- [ ] `crear_cliente_admin()` → Retorna UsuarioDTO
- [ ] `obtener_clientes()` → Retorna List[UsuarioDTO]
- [ ] `obtener_morosos()` → Retorna List[UsuarioDTO]

### Gestión de Aparatos
- [ ] `crear_aparato()` → Retorna AparatoDTO
- [ ] `obtener_aparatos()` → Retorna List[AparatoDTO]

### Gestión de Reservas
- [ ] `crear_reserva()` → Retorna ReservaDTO
- [ ] `obtener_mis_reservas()` → Retorna List[ReservaDTO]
- [ ] `obtener_todas_reservas()` → Retorna List[ReservaDTO]
- [ ] `obtener_ocupacion_dia()` → Retorna List con data estructura

### Gestión de Pagos
- [ ] `pagar_recibo()` → Retorna ReciboDTO actualizado
- [ ] `obtener_mis_recibos()` → Retorna List[ReciboDTO]
- [ ] `obtener_todos_recibos()` → Retorna List[ReciboDTO]
- [ ] `obtener_estadisticas_generales()` → Retorna EstadisticasDTO

## Métodos a Migrar Fase 2 (Sin datos)

Estos métodos retornan solo estado y deben usar ResponseDTO básico:

### Operaciones de Eliminación
- [ ] `eliminar_aparato()` → ResponseDTO con OK/ERROR
- [ ] `eliminar_reserva()` → ResponseDTO con OK/ERROR

### Operaciones de Generación
- [ ] `generar_recibos_mes()` → ResponseDTO con mensaje de éxito

### Utilidades
- [ ] `obtener_mis_recibos_pendientes()` → Retorna List[ReciboDTO]

## Ejemplo Completo: Migración de `login()`

### ANTES
```python
def login(self, dni: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
    """Autentica un usuario."""
    try:
        Validador.validar_campos_no_vacios(dni, password)
        Validador.validar_dni(dni)
        
        usuario = self.cliente_model.autenticar(dni, password)
        if usuario:
            self.usuario_actual = usuario
            logger.info(f"Login exitoso: {usuario['dni']}")
            return True, "Inicio de sesión exitoso", usuario
        else:
            logger.warning(f"Intento de login fallido con DNI: {dni}")
            raise AuthenticationError("DNI o contraseña incorrectos")
            
    except ValidationError as e:
        logger.warning(f"Error de validación en login: {e}")
        return False, str(e), None
    except AuthenticationError as e:
        logger.warning(f"Error de autenticación: {e}")
        return False, str(e), None
    except Exception as e:
        logger.error(f"Error en login: {e}")
        return False, "Error en la autenticación", None
```

### DESPUÉS
```python
def login(self, dni: str, password: str) -> ResponseDTO:
    """Autentica un usuario con respuesta estructurada."""
    try:
        Validador.validar_campos_no_vacios(dni, password)
        Validador.validar_dni(dni)
        
        usuario_dict = self.cliente_model.autenticar(dni, password)
        if usuario_dict:
            self.usuario_actual = usuario_dict
            
            # Crear DTO del usuario
            usuario_dto = UsuarioDTO(
                id=usuario_dict['id'],
                nombre=usuario_dict['nombre'],
                apellido=usuario_dict['apellido'],
                dni=usuario_dict['dni'],
                email=usuario_dict['email'],
                telefono=usuario_dict['telefono'],
                tipo=usuario_dict['tipo'],
                fecha_registro=usuario_dict['fecha_registro']
            )
            
            logger.info(f"Login exitoso: {usuario_dict['dni']}")
            return ResponseDTO(
                exito=True,
                mensaje="Inicio de sesión exitoso",
                datos=asdict(usuario_dto),
                error_code="OK"
            )
        else:
            logger.warning(f"Intento de login fallido con DNI: {dni}")
            raise AuthenticationError("DNI o contraseña incorrectos")
            
    except ValidationError as e:
        logger.warning(f"Error de validación en login: {e}")
        return ResponseDTO(
            exito=False,
            mensaje=str(e),
            datos=None,
            error_code="VALIDATION_ERROR"
        )
    except AuthenticationError as e:
        logger.warning(f"Error de autenticación: {e}")
        return ResponseDTO(
            exito=False,
            mensaje=str(e),
            datos=None,
            error_code="AUTHENTICATION_ERROR"
        )
    except Exception as e:
        logger.error(f"Error en login: {e}")
        return ResponseDTO(
            exito=False,
            mensaje="Error en la autenticación",
            datos=None,
            error_code="DATABASE_ERROR"
        )
```

## Utilidades Helper

### Convertir modelo Dict a DTO
```python
def _dict_a_usuario_dto(self, usuario_dict: Dict) -> UsuarioDTO:
    """Convierte un diccionario de usuario a DTO."""
    return UsuarioDTO(
        id=usuario_dict.get('id'),
        nombre=usuario_dict.get('nombre'),
        apellido=usuario_dict.get('apellido'),
        dni=usuario_dict.get('dni'),
        email=usuario_dict.get('email'),
        telefono=usuario_dict.get('telefono'),
        tipo=usuario_dict.get('tipo'),
        fecha_registro=usuario_dict.get('fecha_registro')
    )

def _lista_dict_a_usuarios_dto(self, usuarios: List[Dict]) -> List[UsuarioDTO]:
    """Convierte una lista de diccionarios a DTOs."""
    return [self._dict_a_usuario_dto(u) for u in usuarios]
```

## Testing DTOs

```python
def test_login_success():
    """Test de login exitoso con DTO."""
    response = controller.login("12345678", "password123")
    
    assert response.exito == True
    assert response.error_code == "OK"
    assert response.datos is not None
    assert 'nombre' in response.datos

def test_login_invalid_credentials():
    """Test de login con credenciales inválidas."""
    response = controller.login("12345678", "wrongpassword")
    
    assert response.exito == False
    assert response.error_code == "AUTHENTICATION_ERROR"
    assert response.datos is None
```

## Beneficios de la Migración

✅ **Type Safety**: IDE entiende la estructura de respuestas
✅ **Consistencia**: Todas las respuestas tienen el mismo formato
✅ **Debugging**: `error_code` facilita identificar errores
✅ **Documentación**: DTOs autodocumentan la estructura
✅ **Serialización**: Fácil conversión a JSON para APIs REST
✅ **Testing**: Assertions más claras y específicas

## Checklist de Migración

- [ ] Actualizar importaciones en controller.py
- [ ] Migrar métodos Fase 1 (con datos)
- [ ] Migrar métodos Fase 2 (sin datos)
- [ ] Actualizar vistas para trabajar con ResponseDTO
- [ ] Crear tests para nuevas respuestas
- [ ] Validar que todas las vistas funcionen
- [ ] Documentar cambios en README
- [ ] Crear migration guide para usuarios

---

**Próximo Paso**: Comenzar con `login()` como prueba de concepto
