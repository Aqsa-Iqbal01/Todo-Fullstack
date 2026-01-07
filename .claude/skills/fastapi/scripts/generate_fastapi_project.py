#!/usr/bin/env python3
"""
FastAPI Project Generator

This script helps generate a basic FastAPI project structure.
"""

import os
import argparse
from pathlib import Path


def create_fastapi_project(project_name):
    """Create a basic FastAPI project structure."""
    project_path = Path(project_name)

    if project_path.exists():
        print(f"Error: Directory {project_name} already exists!")
        return

    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)

    # Create directory structure
    dirs = [
        project_path / "app",
        project_path / "app" / "api",
        project_path / "app" / "api" / "v1",
        project_path / "app" / "api" / "v1" / "endpoints",
        project_path / "app" / "models",
        project_path / "app" / "schemas",
        project_path / "app" / "database",
        project_path / "app" / "utils",
        project_path / "tests"
    ]

    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    init_files = [
        project_path / "app" / "__init__.py",
        project_path / "app" / "api" / "__init__.py",
        project_path / "app" / "api" / "v1" / "__init__.py",
        project_path / "app" / "api" / "v1" / "endpoints" / "__init__.py",
        project_path / "app" / "models" / "__init__.py",
        project_path / "app" / "schemas" / "__init__.py",
        project_path / "app" / "database" / "__init__.py",
        project_path / "app" / "utils" / "__init__.py",
    ]

    for init_file in init_files:
        init_file.touch(exist_ok=True)

    # Create main.py
    main_content = '''from fastapi import FastAPI

app = FastAPI(title="My FastAPI Project")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
'''
    (project_path / "app" / "main.py").write_text(main_content)

    # Create requirements.txt
    requirements_content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
'''
    (project_path / "requirements.txt").write_text(requirements_content)

    # Create README.md
    readme_content = f'''# {project_name}

A FastAPI project generated with FastAPI Project Generator.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
'''
    (project_path / "README.md").write_text(readme_content)

    print(f"✅ FastAPI project '{project_name}' has been created successfully!")
    print(f"📁 Project structure:")
    print(f"   {project_name}/")
    print(f"   ├── app/")
    print(f"   │   ├── __init__.py")
    print(f"   │   ├── main.py")
    print(f"   │   ├── api/")
    print(f"   │   ├── models/")
    print(f"   │   ├── schemas/")
    print(f"   │   ├── database/")
    print(f"   │   └── utils/")
    print(f"   ├── requirements.txt")
    print(f"   └── README.md")


def main():
    parser = argparse.ArgumentParser(description="FastAPI Project Generator")
    parser.add_argument("project_name", help="Name of the FastAPI project to create")

    args = parser.parse_args()

    create_fastapi_project(args.project_name)


if __name__ == "__main__":
    main()