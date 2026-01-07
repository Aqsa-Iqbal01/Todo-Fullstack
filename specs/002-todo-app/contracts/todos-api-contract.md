# API Contracts: Full-Stack Secure Todo Web Application

## Authentication Endpoints

### POST /api/auth/register
**Description**: Register a new user account
**Authentication**: None (public endpoint)

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created)**:
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  }
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "error": "Email already exists"
}
```

### POST /api/auth/login
**Description**: Authenticate user and return JWT token
**Authentication**: None (public endpoint)

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "token": "jwt-token-string",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  }
}
```

**Response (401 Unauthorized)**:
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

### POST /api/auth/logout
**Description**: Logout user and invalidate session
**Authentication**: JWT required

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

## Todo Endpoints

### GET /api/todos
**Description**: Get all todos for the authenticated user
**Authentication**: JWT required

**Response (200 OK)**:
```json
{
  "success": true,
  "todos": [
    {
      "id": "uuid-string",
      "title": "Complete project",
      "description": "Finish the todo app implementation",
      "completed": false,
      "due_date": "2026-02-01T10:00:00Z",
      "user_id": "user-uuid",
      "created_at": "2026-01-06T10:00:00Z",
      "updated_at": "2026-01-06T10:00:00Z"
    }
  ]
}
```

### POST /api/todos
**Description**: Create a new todo for the authenticated user
**Authentication**: JWT required

**Request**:
```json
{
  "title": "New todo",
  "description": "Description of the new todo",
  "due_date": "2026-02-01T10:00:00Z"
}
```

**Response (201 Created)**:
```json
{
  "success": true,
  "todo": {
    "id": "uuid-string",
    "title": "New todo",
    "description": "Description of the new todo",
    "completed": false,
    "due_date": "2026-02-01T10:00:00Z",
    "user_id": "user-uuid",
    "created_at": "2026-01-06T10:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z"
  }
}
```

### PUT /api/todos/{id}
**Description**: Update an existing todo for the authenticated user
**Authentication**: JWT required

**Request**:
```json
{
  "title": "Updated todo title",
  "description": "Updated description",
  "completed": true,
  "due_date": "2026-02-01T10:00:00Z"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "todo": {
    "id": "uuid-string",
    "title": "Updated todo title",
    "description": "Updated description",
    "completed": true,
    "due_date": "2026-02-01T10:00:00Z",
    "user_id": "user-uuid",
    "created_at": "2026-01-06T10:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z"
  }
}
```

### DELETE /api/todos/{id}
**Description**: Delete a todo for the authenticated user
**Authentication**: JWT required

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Todo deleted successfully"
}
```

### PATCH /api/todos/{id}/toggle
**Description**: Toggle the completed status of a todo
**Authentication**: JWT required

**Response (200 OK)**:
```json
{
  "success": true,
  "todo": {
    "id": "uuid-string",
    "title": "Todo title",
    "description": "Todo description",
    "completed": true,
    "due_date": "2026-02-01T10:00:00Z",
    "user_id": "user-uuid",
    "created_at": "2026-01-06T10:00:00Z",
    "updated_at": "2026-01-06T10:00:00Z"
  }
}
```