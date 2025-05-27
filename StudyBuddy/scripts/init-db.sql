-- PostgreSQL initialization script for StudyBuddy application
-- This script runs when the PostgreSQL container starts for the first time

-- Create the database if it doesn't exist (handled by POSTGRES_DB env var)
-- Create the user if it doesn't exist (handled by POSTGRES_USER env var)

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON DATABASE studybuddy_db TO studybuddy_user;

-- Create extensions that might be useful
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'UTC'; 