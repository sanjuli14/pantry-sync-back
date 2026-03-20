# Pantry-Sync API

API REST para compartir alimentos y objetos cercanos.

## Stack Tecnológico

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Base de datos:** SQLite
- **Autenticación:** JWT (python-jose) + bcrypt
- **Validación:** Pydantic

## Requisitos

```bash
pip install fastapi uvicorn sqlalchemy python-jose passlib bcrypt python-multipart
```

## Iniciar el servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

---

## Autenticación

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer <token>
```

---

## Endpoints de Autenticación

### Registro

Registra un nuevo usuario.

```http
POST /auth/register
```

**Body:**
```json
{
  "alias": "usuario123",
  "phone": "+56912345678",
  "password": "micontraseña"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "alias": "usuario123",
  "phone": "+56912345678",
  "created_at": "2024-01-01T12:00:00"
}
```

---

### Login

Inicia sesión y obtiene un token JWT.

```http
POST /auth/login
```

**Body (form-data):**
```
username: usuario123
password: micontraseña
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

---

### Obtener perfil actual

Obtiene la información del usuario autenticado.

```http
GET /auth/me
```

**Respuesta:**
```json
{
  "id": 1,
  "alias": "usuario123",
  "phone": "+56912345678",
  "created_at": "2024-01-01T12:00:00"
}
```

---

### Actualizar perfil

Actualiza el alias y/o teléfono del usuario.

```http
PUT /auth/profile
```

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "alias": "nuevoalias",
  "phone": "+56987654321"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "alias": "nuevoalias",
  "phone": "+56987654321",
  "created_at": "2024-01-01T12:00:00"
}
```

---

### Cambiar contraseña

Cambia la contraseña del usuario.

```http
PUT /auth/password
```

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "current_password": "contraseñaactual",
  "new_password": "nuevacontraseña"
}
```

**Respuesta:**
```json
{
  "message": "Contraseña actualizada correctamente"
}
```

---

## Endpoints de Items

### Crear item

Crea un nuevo item. Requiere autenticación.

```http
POST /items/
```

**Headers:**
```
Authorization: Bearer <token>
```

**Body:**
```json
{
  "title": "Manzanas frescas",
  "description": "Manzanas rojas del fundo",
  "zone": "Providencia",
  "category": "Frutas/Vegetales",
  "contact": "+56912345678",
  "latitude": -33.4569,
  "longitude": -70.6483
}
```

**Categorías disponibles:**
- `Frutas/Vegetales` (expira en 48h)
- `Panadería` (expira en 24h)
- `Lácteos` (expira en 72h)
- `Enlatados` (expira en 720h)
- `Higiene` (expira en 2160h)
- `Otros` (expira en 48h)

**Respuesta:**
```json
{
  "id": 1,
  "title": "Manzanas frescas",
  "description": "Manzanas rojas del fundo",
  "zone": "Providencia",
  "category": "Frutas/Vegetales",
  "contact": "+56912345678",
  "image_url": null,
  "latitude": -33.4569,
  "longitude": -70.6483,
  "user_id": 1,
  "created_at": "2024-01-01T12:00:00",
  "expires_at": "2024-01-03T12:00:00"
}
```

---

### Listar todos los items

Obtiene todos los items activos (no expirados).

```http
GET /items/
```

**Respuesta:** Array de items.

---

### Listar mis items

Obtiene los items del usuario autenticado.

```http
GET /items/mine
```

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:** Array de items del usuario.

---

### Listar items por zona

Obtiene items activos filtrados por zona.

```http
GET /items/zone/{zone}
```

**Ejemplo:** `GET /items/zone/Providencia`

**Respuesta:** Array de items.

---

### Listar items cercanos

Obtiene items cercanos a una ubicación.

```http
GET /items/nearby
```

**Query parameters:**
- `lat` (requerido): Latitud
- `lng` (requerido): Longitud
- `radius` (opcional): Radio en km (default: 0.5, max: 10)

**Ejemplo:** `GET /items/nearby?lat=-33.4569&lng=-70.6483&radius=2`

**Respuesta:**
```json
[
  {
    "item": { ... },
    "distance_km": 0.5
  }
]
```

---

### Actualizar item

Actualiza un item existente. Solo el dueño puede editarlo.

```http
PUT /items/{item_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Body:** Campos opcionales a actualizar.
```json
{
  "title": "Nuevo título",
  "description": "Nueva descripción",
  "zone": "Nueva zona",
  "category": "Otros",
  "contact": "+56987654321",
  "latitude": -33.5,
  "longitude": -70.6
}
```

**Respuesta:** Item actualizado.

---

### Subir imagen de item

Sube una imagen para un item.

```http
POST /items/{item_id}/image
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Body (form-data):**
```
file: [seleccionar imagen]
```

**Formatos permitidos:** JPG, PNG, WebP

**Respuesta:**
```json
{
  "image_url": "/uploads/abc123.jpg",
  "item_id": 1
}
```

---

### Eliminar item

Elimina un item. Solo el dueño puede eliminarlo.

```http
DELETE /items/{item_id}
```

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "message": "Item eliminado"
}
```

---

## Endpoints de Sistema

### Cleanup de items expirados

Elimina todos los items expirados (uso administrativo).

```http
DELETE /items/system/cleanup
```

**Respuesta:**
```json
{
  "message": "Se eliminaron 5 productos expirados."
}
```

---

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o expirado |
| 403 | Forbidden - No tienes permisos para esta acción |
| 404 | Not Found - Recurso no encontrado |
| 422 | Validation Error - Error de validación de datos |

---

## Ejemplo de Uso con cURL

### Registrar usuario
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"alias":"usuario1","phone":"+56912345678","password":"pass123"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -d "username=usuario1&password=pass123"
```

### Crear item
```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Pan","description":"Pan integral","zone":"Santiago","category":"Panadería","contact":"+56912345678"}'
```

### Actualizar item
```bash
curl -X PUT "http://localhost:8000/items/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Pan integral fresco"}'
```

### Actualizar perfil
```bash
curl -X PUT "http://localhost:8000/auth/profile" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"alias":"nuevouser"}'
```

### Cambiar contraseña
```bash
curl -X PUT "http://localhost:8000/auth/password" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"current_password":"pass123","new_password":"newpass456"}'
```
