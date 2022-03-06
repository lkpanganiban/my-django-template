# Django Template
A reference repo for my Django Projects

## Services to be Configured
- Django + Django Rest Framework
- Redis
- Celery
- Elasticsearch
- Kibana
- Logstash
- Filebeat
- Prometheus
- Nginx
- PostgreSQL
- Ansible

## Sample Modules
1. Upload
2. Permissions
3. Login with JWT

# Initial Setup
1. Create a `.env.dev` and `.env-db.dev` files. Use the `.env` and `.env-db` as reference

## Setup for Operations
1. Build a Dockerfile for dev and production
2. Create a docker-compose.yml for dev and production
3. Configure docker-elk
   - repo came from https://github.com/deviantony/docker-elk
   - in the `elasticsearch/config/elasticsearch.yml` set the `xpack.license.self_generated.type` from `trial` to `basic`
   - tutorial: https://gonzalo123.com/2020/08/10/monitoring-django-applications-with-grafana-and-kibana-using-prometheus-and-elasticsearch/
4. Configure Prometheus:
   - reference repo came from https://github.com/dotja/django-prometheus-docker
   - refer to the following link: https://www.youtube.com/watch?v=86js4POzTV4

# Endpoints
1. Users
2. Files
