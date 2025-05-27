# StudyBuddy Production Deployment Guide

This guide explains how to deploy the StudyBuddy Django application to production using Docker and Docker Compose with PostgreSQL and WhiteNoise for static files.

## Prerequisites

- Docker and Docker Compose installed
- Basic understanding of Django and Docker
- Access to your production server

## Project Structure

The project now includes:
- **Multi-environment settings**: `ProjStudyBuddy/settings/` with `base.py`, `development.py`, and `production.py`
- **Docker configuration**: `Dockerfile` and `docker-compose.yml`
- **Static files handling**: WhiteNoise middleware for serving static files
- **Database migration**: Scripts to migrate from SQLite to PostgreSQL
- **Security**: Production-ready security settings

## Quick Start

### 1. Environment Setup

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your production values:
   ```bash
   # Required settings
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=postgresql://studybuddy_user:your_password@db:5432/studybuddy_db
   
   # Email configuration
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # Security
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

### 2. Data Migration (if you have existing data)

If you have existing data in SQLite, migrate it before deploying:

1. Export data from SQLite:
   ```bash
   python scripts/migrate_data.py export
   ```

2. This creates a `fixtures/data_export.json` file with your data.

### 3. Deploy with Docker Compose

1. Build and start the services:
   ```bash
   docker-compose up -d --build
   ```

2. The application will be available at `http://localhost:8000`

### 4. Import Data (if migrating)

If you exported data in step 2:

1. Import data to PostgreSQL:
   ```bash
   docker-compose exec web python scripts/migrate_data.py import
   ```

## Detailed Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | - |
| `DEBUG` | Debug mode | No | False |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Yes | - |
| `DATABASE_URL` | PostgreSQL connection URL | Yes | - |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF | Yes | - |
| `EMAIL_HOST_USER` | SMTP username | No | - |
| `EMAIL_HOST_PASSWORD` | SMTP password | No | - |
| `SECURE_SSL_REDIRECT` | Force HTTPS redirect | No | True |

### Database Configuration

The production setup uses PostgreSQL with the following default configuration:
- **Database**: `studybuddy_db`
- **User**: `studybuddy_user`
- **Port**: `5432`

You can customize these in the `docker-compose.yml` file.

### Static Files

Static files are handled by WhiteNoise middleware, which:
- Serves static files directly from Django
- Compresses files for better performance
- Adds proper cache headers
- Works well in containerized environments

### Security Features

The production settings include:
- HTTPS enforcement
- Secure cookies
- XSS protection
- Content type sniffing protection
- HSTS headers
- Secure referrer policy

## Docker Services

### Web Service (Django)
- Runs the Django application with Gunicorn
- Uses multi-stage build for smaller image size
- Runs as non-root user for security
- Includes health checks

### Database Service (PostgreSQL)
- PostgreSQL 15 Alpine image
- Persistent data storage
- Health checks
- Automatic initialization

## Management Commands

### Development
```bash
# Run with development settings
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Production (Docker)
```bash
# View logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Access Django shell
docker-compose exec web python manage.py shell
```

## Backup and Restore

### Database Backup
```bash
# Create backup
docker-compose exec db pg_dump -U studybuddy_user studybuddy_db > backup.sql

# Restore backup
docker-compose exec -T db psql -U studybuddy_user studybuddy_db < backup.sql
```

### Volume Backup
```bash
# Backup volumes
docker run --rm -v studybuddy_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

## Monitoring and Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Health Checks
- Web service: `http://localhost:8000/health/`
- Database: Built-in PostgreSQL health check

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

2. **Database Connection Issues**
   ```bash
   # Check database logs
   docker-compose logs db
   
   # Verify database is running
   docker-compose exec db pg_isready -U studybuddy_user
   ```

3. **Static Files Not Loading**
   ```bash
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

4. **Migration Issues**
   ```bash
   # Reset migrations (careful!)
   docker-compose exec web python manage.py migrate --fake-initial
   ```

### Performance Optimization

1. **Increase Gunicorn Workers**
   Edit `docker-compose.yml` and adjust the `--workers` parameter.

2. **Add Redis for Caching**
   Uncomment the Redis configuration in `production.py`.

3. **Use Nginx for Static Files**
   Uncomment the Nginx service in `docker-compose.yml`.

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Configure CSRF_TRUSTED_ORIGINS
- [ ] Use strong database passwords
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

## Production Deployment

For production deployment:

1. Use a reverse proxy (Nginx) for SSL termination
2. Set up proper domain and SSL certificates
3. Configure email backend for notifications
4. Set up monitoring and alerting
5. Implement backup strategies
6. Use environment-specific secrets management

## Support

For issues or questions:
1. Check the logs: `docker-compose logs -f`
2. Verify environment variables in `.env`
3. Ensure all required services are running
4. Check Django documentation for specific errors 