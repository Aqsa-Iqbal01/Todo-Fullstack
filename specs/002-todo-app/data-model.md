# Data Model: Full-Stack Secure Todo Web Application

## Entity: User

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for each user
- `email`: String (Unique, Indexed) - User's email address for login
- `password_hash`: String - Hashed password using secure algorithm
- `created_at`: DateTime - Timestamp when user account was created
- `updated_at`: DateTime - Timestamp when user account was last updated
- `is_active`: Boolean - Flag indicating if the account is active

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet security requirements (minimum length, complexity)

**Relationships**:
- One-to-Many: A user can have many todos (user.id → todo.user_id)

## Entity: Todo

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for each todo
- `title`: String (Required) - Brief title/description of the todo
- `description`: Text (Optional) - Detailed description of the todo
- `completed`: Boolean - Flag indicating if the todo is completed
- `due_date`: DateTime (Optional) - Deadline for completing the todo
- `user_id`: UUID (Foreign Key) - Reference to the user who owns this todo
- `created_at`: DateTime - Timestamp when todo was created
- `updated_at`: DateTime - Timestamp when todo was last updated

**Validation Rules**:
- Title must be provided and not empty
- User_id must reference an existing user
- Due date must be in the future if provided

**State Transitions**:
- Incomplete (completed = False) → Complete (completed = True) when user marks as done
- Complete (completed = True) → Incomplete (completed = False) when user unmarks as done

**Relationships**:
- Many-to-One: Each todo belongs to one user (todo.user_id → user.id)

## Database Constraints

**Foreign Key Constraints**:
- todo.user_id must reference an existing user.id
- Prevents orphaned todos without associated users

**Unique Constraints**:
- user.email must be unique across all users
- Prevents duplicate registrations with same email

**Indexing**:
- Index on user.email for fast authentication lookups
- Index on todo.user_id for efficient filtering by user
- Index on todo.completed for efficient status-based queries