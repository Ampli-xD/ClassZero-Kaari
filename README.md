# Kaari - Presentation and Content Management System

## Overview
Kaari, developed by ClassZero team, is a desktop application built with Python and CustomTkinter, designed for creating, editing, and managing mathematical and educational presentations. Featuring a modern, customizable user interface, Kaari enables users to input natural language queries to generate high-quality slides and animations effortlessly. The application provides tools for organizing presentations, previewing content, and reusing stored assets from a searchable knowledge base. Kaari connects to a backend server powered by microservices, including n8n for workflow automation, PostgreSQL for data persistence, and MinIO for scalable asset storage. This integration ensures seamless processing, rendering, and retrieval of content, making Kaari a practical solution for educators, content creators, and institutions seeking efficient presentation management.

## Demo Video 
<h2 align="center">📺 Demo Video</h2>
<p align="center">
  <a href="https://youtu.be/gdAw2bSv0mk" target="_blank">
    <img src="https://img.youtube.com/vi/gdAw2bSv0mk/0.jpg" alt="Watch the video" width="560" />
  </a>
</p>


## Backend Architecture

The backend consists of several microservices that work together to provide the necessary functionality. The system uses Docker volumes for persistent data storage across services.

### Core Services
1. **PostgreSQL Database**
   - Primary data storage for presentations, users, and metadata
   - Accessible on port `29112`
   - Default database: `ClassZero`
   - Default credentials: `admin/admin@2911`

2. **Redis**
   - Used for caching and real-time features
   - Accessible on port `29111`

3. **MinIO**
   - Object storage for media files and assets
   - Accessible on port `29113`

4. **n8n**
   - Workflow automation and integration
   - Accessible on port `29114`
   - Data stored in `n8n_data` volume

### Data Volumes

The system uses the following named volumes for persistent data storage:

1. **PostgreSQL Data (`pgdata_vector`)**
   - Location in container: `/var/lib/postgresql/data`
   - Contains: Database tables, indexes, and vector data
   - Backup file: `pgdata_vector.tar.gz`

2. **MinIO Data (`minio-data`)**
   - Location in container: `/data`
   - Contains: Uploaded media files, presentation assets
   - Backup file: `minio-data.tar.gz`

3. **n8n Data (`n8n_data`)**
   - Location in container: `/home/node/.n8n`
   - Contains: Workflow configurations, credentials, and execution data
   - Backup file: `n8n_data.tar.gz`

4. **Manim Outputs (`manim-output`)**
   - Location in container: `/app/outputs`
   - Contains: Rendered animations and media files
   - Managed automatically by the system

### API Endpoints
The desktop application communicates with the backend through RESTful APIs. Key endpoints include:
- Authentication and user management
- Presentation CRUD operations
- Media upload and management
- Real-time collaboration features

## Project Structure

### Desktop Application (`/app`)
A Python application using CustomTkinter for the GUI.

Key Features:
- Modern, customizable UI with dark/light theme support
- Presentation creation and management
- Slide editing with rich content support
- User authentication and session management

Main Components:
- `app_main.py`: Main application entry point
- `app_editor.py`: Presentation editor interface
- `app_login.py`: User authentication
- `app_presentations_list.py`: Presentation management
- `app_editor_*.py`: Specialized editor components

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Redis 6+
- MinIO
- n8n (for workflow automation)
- Required Python packages (install with `pip install -r requirements.txt`)
  - customtkinter
  - psycopg2-binary
  - redis
  - minio
  - requests
  - python-dotenv

### Volume Management

#### Creating Backups
To create backups of all volumes, run the following command from the `backend` directory:
```bash
# On Windows
.\volumes\volume_creator_script.ps1

# On Linux/macOS
chmod +x ./volumes/volume_restore_script.sh
./volumes/volume_restore_script.sh
```

#### Restoring from Backups
To restore volumes from existing backups, place the backup files in the `volumes` directory and run:
```bash
# On Windows
# Run PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
.\volumes\volume_restore_script.ps1

# On Linux/macOS
chmod +x ./volumes/volume_restore_script.sh
./volumes/volume_restore_script.sh
```

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd KaariMain/app
   ```

2. Set up the database:
   ```sql
   CREATE DATABASE ClassZero;
   CREATE USER admin WITH PASSWORD 'admin@2911';
   GRANT ALL PRIVILEGES ON DATABASE ClassZero TO admin;
   ```

3. Configure the backend services:
   - Update `app/HostPortMapping.py` with your server IP and ports
   - Ensure all services (PostgreSQL, Redis, MinIO, n8n) are running

4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python app_main.py
   ```

## Development

### Environment Setup
1. Clone the repository and navigate to the project directory
2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt  # If available
   ```

### Configuration
Edit `app/HostPortMapping.py` to match your environment:
```python
# Server configuration
host_server = "your_server_ip"  # Update this to your server's IP

# Service ports
redis_port = 29111
postgre_port = 29112
minio_port = 29113
n8n_port = 29114
```

### Running the Application
From the `/app` directory:
```bash
python app_main.py
```

### Database Migrations
When the database schema changes, you'll need to create and apply migrations:
```bash
# Example using Alembic (if configured)
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Dependencies
Main dependencies:
- `customtkinter`: Modern UI components
- `psycopg2-binary`: PostgreSQL database adapter
- `redis`: Redis client for caching
- `minio`: MinIO client for object storage
- `requests`: HTTP client for API communication
- `python-dotenv`: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
