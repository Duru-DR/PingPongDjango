PingPong Platform - Backend System

**Group Project | My Role: Backend, Security & DevOps Lead**  
*Django | PostgreSQL | Docker | Nginx | WebSockets | OAuth/JWT*

## 🔧 My Contributions
*Containerized Services with Docker & Docker Compose:*
Django backend
PostgreSQL with persistent volumes
Redis for WebSocket messaging
Nginx reverse proxy with SSL termination
*Production-Grade Nginx Configuration:*
Load balancing
Static file serving
WebSocket proxy (/ws/ route)

🐳 Deployment Guide
Prerequisites
Docker 20.10+
Docker Compose 2.5+

Production Setup
Clone repository:
```
git clone https://github.com/Duru-DR/PingPongDjango.git
cd PingPongDjango/Manage_services
make
```

### 📈 System Architecture
```mermaid
graph TD
  classDef component fill:#f9f,stroke:#333;
  classDef database fill:#bbf,stroke:#333;
  
  A[Client] -->|HTTPS| B[Nginx:443]
  B -->|Proxy| C[Django:8000]
  B -->|WS| D[WebSockets]
  C --> E[(PostgreSQL)]
  C --> F[Redis]
  D --> F
  
  class B,C,D component;
  class E,F database;
```
