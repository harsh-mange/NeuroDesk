#!/usr/bin/env python3
"""
NeuroDesk Setup Script
This script helps you set up the NeuroDesk project for development.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_prerequisites():
    """Check if required tools are installed."""
    print("Checking prerequisites...")
    
    # Check Python
    python_version = run_command("python --version")
    if python_version:
        print(f"✓ Python: {python_version.strip()}")
    else:
        print("✗ Python not found. Please install Python 3.8+")
        return False
    
    # Check Flutter
    flutter_version = run_command("flutter --version")
    if flutter_version:
        print("✓ Flutter found")
    else:
        print("✗ Flutter not found. Please install Flutter SDK")
        return False
    
    return True

def setup_backend():
    """Set up the FastAPI backend."""
    print("\nSetting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("✗ Backend directory not found")
        return False
    
    # Install Python dependencies
    print("Installing Python dependencies...")
    result = run_command("pip install -r requirements.txt", cwd=backend_dir)
    if not result:
        print("✗ Failed to install Python dependencies")
        return False
    
    print("✓ Backend setup complete")
    return True

def setup_frontend():
    """Set up the Flutter frontend."""
    print("\nSetting up frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("✗ Frontend directory not found")
        return False
    
    # Get Flutter dependencies
    print("Getting Flutter dependencies...")
    result = run_command("flutter pub get", cwd=frontend_dir)
    if not result:
        print("✗ Failed to get Flutter dependencies")
        return False
    
    print("✓ Frontend setup complete")
    return True

def create_env_files():
    """Create environment files if they don't exist."""
    print("\nCreating environment files...")
    
    # Backend .env
    backend_env = Path("backend/.env")
    if not backend_env.exists():
        backend_env.write_text("""# NeuroDesk Backend Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./neurodesk.db
""")
        print("✓ Created backend/.env")
    
    # Frontend .env
    frontend_env = Path("frontend/.env")
    if not frontend_env.exists():
        frontend_env.write_text("""# NeuroDesk Frontend Environment Variables
API_BASE_URL=http://localhost:8000
""")
        print("✓ Created frontend/.env")

def main():
    """Main setup function."""
    print("🧠 NeuroDesk Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\nPlease install the missing prerequisites and run this script again.")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\nBackend setup failed. Please check the errors above.")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\nFrontend setup failed. Please check the errors above.")
        sys.exit(1)
    
    # Create environment files
    create_env_files()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Update the API keys in backend/.env")
    print("2. Run the backend: cd backend && python main.py")
    print("3. Run the frontend: cd frontend && flutter run")
    print("\nHappy coding! 🚀")

if __name__ == "__main__":
    main() 