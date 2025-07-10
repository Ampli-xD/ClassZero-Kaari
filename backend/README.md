# ClassZero Backend Documentation

## Overview
The ClassZero backend is a microservices-based architecture designed to handle various tasks including video rendering, workflow automation, and data storage. The system is containerized using Docker and orchestrated with Docker Compose.

## System Architecture

### Services
1. **HAProxy**
   - Acts as a reverse proxy and load balancer
   - Routes traffic to appropriate services
   - Provides statistics dashboard on port 29110
   - Configuration: `haproxy/haproxy.cfg`

2. **Redis**
   - Message broker for inter-service communication
   - Used for task queuing and pub/sub
   - Accessible on port 29111

3. **MinIO**
   - Object storage service (S3-compatible)
   - Used for storing rendered videos and other assets
   - Accessible on port 29113
   - Default credentials: minioadmin/minioadmin

4. **PostgreSQL**
   - Primary database service
   - Used for both relational and vector data
   - Accessible on port 29112

5. **n8n**
   - Workflow automation service
   - Used for orchestrating complex workflows
   - Accessible on port 29114
   - Data persisted in `n8n_data` volume

6. **Manim Processor**
   - Custom service for processing Manim animations
   - Listens for rendering tasks from Redis
   - Stores output in MinIO
   - Source code: `manim_processor/`

## Port Configuration

| Service     | Port  | Protocol | Description                     |
|-------------|-------|----------|---------------------------------|
| HAProxy     | 29110 | HTTP     | Statistics dashboard            |
| Redis       | 29111 | TCP      | Message broker                  |
| PostgreSQL  | 29112 | TCP      | Database access                 |
| MinIO       | 29113 | TCP      | Object storage                  |
| n8n         | 29114 | TCP      | Workflow automation interface   |

## Volumes

1. `minio-data`: Stores MinIO object storage data
2. `pgdata_vector`: PostgreSQL database files
3. `n8n_data`: n8n workflow and configuration data
4. `manim-outputs`: Temporary storage for rendered Manim animations

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Installation

1. Clone the repository
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Start the services:
   ```bash
   docker-compose up -d
   ```

### Accessing Services

- **HAProxy Stats**: http://localhost:29110/stats
- **MinIO Console**: http://localhost:9001 (default credentials: minioadmin/minioadmin)
- **n8n Interface**: http://localhost:5678 (when running n8n on host network)

## Manim Processor

The Manim processor is a custom service that handles the rendering of mathematical animations. It listens for rendering tasks from Redis, processes them using Manim, and stores the output in MinIO.

### Features
- Asynchronous task processing
- Distributed rendering with multiple workers
- Automatic retry on failure
- Progress tracking via Redis

### Configuration
Configuration can be done through environment variables in the `docker-compose.yml` file or by modifying the `manim_processor.py` script directly.

## Monitoring

### Logs
View logs for all services:
```bash
docker-compose logs -f
```

View logs for a specific service:
```bash
docker-compose logs -f <service_name>
```

### Metrics
HAProxy provides detailed metrics and monitoring through its statistics interface at http://localhost:29110/stats

## Backup and Restore

### Backing Up Volumes
Use the provided scripts in the `volumes` directory to back up and restore your data.

1. **Backup**:
   ```bash
   ./volumes/volume_creator_script.ps1
   ```

2. **Restore**:
   ```bash
   ./volumes/volume_restore_script.sh
   ```

## Troubleshooting

### Common Issues
1. **Port Conflicts**: Ensure the required ports (29110-29114) are not in use by other services.
2. **Volume Permissions**: If services fail to start due to permission issues, ensure Docker has the necessary permissions to write to the volumes.
3. **Service Dependencies**: Some services depend on others (e.g., n8n depends on Redis and PostgreSQL). Ensure all services are running and healthy.

### Logs
Check the logs for specific error messages:
```bash
docker-compose logs <service_name>
```

## Security Considerations

1. **Default Credentials**: Change the default credentials for MinIO and other services in production.
2. **Network Security**: Ensure proper network segmentation and firewall rules are in place.
3. **Data Encryption**: Consider enabling TLS for inter-service communication in production.

## License
[Specify your license here]

## Support
For support, please contact [your support email or contact information]
