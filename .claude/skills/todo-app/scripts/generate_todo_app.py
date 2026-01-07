#!/usr/bin/env python3
"""
Todo App Generator

This script helps generate a basic Todo application structure with both frontend (Next.js) and backend (FastAPI).
"""

import os
import argparse
from pathlib import Path


def create_todo_app(project_name):
    """Create a basic Todo app project structure."""
    project_path = Path(project_name)

    if project_path.exists():
        print(f"Error: Directory {project_name} already exists!")
        return

    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)

    # Create directory structure
    dirs = [
        project_path / "backend",
        project_path / "backend" / "models",
        project_path / "backend" / "schemas",
        project_path / "backend" / "database",
        project_path / "backend" / "auth",
        project_path / "backend" / "api",
        project_path / "backend" / "api" / "routes",
        project_path / "app",
        project_path / "app" / "src",
        project_path / "app" / "src" / "app",
        project_path / "app" / "src" / "components",
        project_path / "app" / "src" / "lib",
        project_path / "app" / "src" / "contexts",
        project_path / "app" / "src" / "types",
        project_path / "app" / "public",
    ]

    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    # Create __init__.py files for backend
    init_files = [
        project_path / "backend" / "__init__.py",
        project_path / "backend" / "models" / "__init__.py",
        project_path / "backend" / "schemas" / "__init__.py",
        project_path / "backend" / "database" / "__init__.py",
        project_path / "backend" / "auth" / "__init__.py",
        project_path / "backend" / "api" / "__init__.py",
        project_path / "backend" / "api" / "routes" / "__init__.py",
    ]

    for init_file in init_files:
        init_file.touch(exist_ok=True)

    # Create basic backend files
    main_py_content = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import todo_router, auth_router
from .database.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(todo_router, prefix="/api/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Todo App API"}
'''
    (project_path / "backend" / "main.py").write_text(main_py_content)

    # Create database configuration
    database_py_content = '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
    (project_path / "backend" / "database" / "database.py").write_text(database_py_content)

    # Create requirements.txt for backend
    backend_requirements = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
alembic==1.13.1
python-multipart==0.0.6
'''
    (project_path / "backend" / "requirements.txt").write_text(backend_requirements)

    # Create frontend files
    # Create app router pages
    (project_path / "app" / "src" / "app" / "layout.tsx").write_text('''import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Todo App',
  description: 'A simple todo application',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
''')

    (project_path / "app" / "src" / "app" / "page.tsx").write_text('''export default function HomePage() {
  return (
    <main>
      <h1>Welcome to the Todo App</h1>
      <p>Please <a href="/login">login</a> or <a href="/register">register</a> to continue.</p>
    </main>
  )
}
''')

    (project_path / "app" / "src" / "app" / "globals.css").write_text('''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}
''')

    # Create package.json for frontend
    frontend_package_json = '''{
  "name": "todo-app-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18",
    "react-dom": "^18",
    "next": "14.0.1",
    "axios": "^1.6.0",
    "react-icons": "^4.12.0"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10",
    "postcss": "^8",
    "tailwindcss": "^3",
    "eslint": "^8",
    "eslint-config-next": "14.0.1"
  }
}
'''
    (project_path / "app" / "package.json").write_text(frontend_package_json)

    # Create tsconfig.json for frontend
    frontend_tsconfig = '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
'''
    (project_path / "app" / "tsconfig.json").write_text(frontend_tsconfig)

    # Create tailwind.config.js
    tailwind_config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
'''
    (project_path / "app" / "tailwind.config.js").write_text(tailwind_config)

    # Create next.config.js
    next_config = '''/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
}

module.exports = nextConfig
'''
    (project_path / "app" / "next.config.js").write_text(next_config)

    # Create README.md
    readme_content = f'''# {project_name}

A full-stack Todo application with FastAPI backend and Next.js frontend.

## Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at [http://localhost:8000](http://localhost:8000).

## Frontend Setup (Next.js)

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The app will be available at [http://localhost:3000](http://localhost:3000).

## Project Structure

```
{project_name}/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── database/           # Database configuration
│   ├── auth/               # Authentication logic
│   └── api/                # API routes
├── app/                    # Next.js frontend
│   ├── src/
│   │   ├── app/            # App Router pages
│   │   ├── components/     # Reusable components
│   │   ├── lib/            # Utility functions
│   │   ├── contexts/       # React contexts
│   │   └── types/          # TypeScript types
│   ├── public/
│   └── package.json
└── README.md
```
'''
    (project_path / "README.md").write_text(readme_content)

    print(f"✅ Todo app project '{project_name}' has been created successfully!")
    print(f"📁 Project structure:")
    print(f"   {project_name}/")
    print(f"   ├── backend/")
    print(f"   │   ├── main.py")
    print(f"   │   ├── models/")
    print(f"   │   ├── schemas/")
    print(f"   │   ├── database/")
    print(f"   │   ├── auth/")
    print(f"   │   └── api/")
    print(f"   ├── app/")
    print(f"   │   ├── src/")
    print(f"   │   │   ├── app/")
    print(f"   │   │   ├── components/")
    print(f"   │   │   ├── lib/")
    print(f"   │   │   ├── contexts/")
    print(f"   │   │   └── types/")
    print(f"   │   ├── package.json")
    print(f"   │   └── tsconfig.json")
    print(f"   └── README.md")


def main():
    parser = argparse.ArgumentParser(description="Todo App Generator")
    parser.add_argument("project_name", help="Name of the Todo app project to create")

    args = parser.parse_args()

    create_todo_app(args.project_name)


if __name__ == "__main__":
    main()