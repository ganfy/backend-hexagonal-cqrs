# Proyecto Backend con Arquitectura Hexagonal y CQRS

Este proyecto es una implementación base de un servicio backend en Python, diseñado para demostrar un enfoque moderno de arquitectura de software aplicando patrones como Arquitectura Hexagonal, CQRS y Bundle-Contexts.

El objetivo principal es establecer una base sólida, mantenible y escalable para un sistema backend, priorizando la separación de responsabilidades y la independencia del dominio de negocio.

## Índice

- [Arquitectura y Decisiones de Diseño](#arquitectura-y-decisiones-de-diseño)
- [Tech Stack](#tech-stack)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Cómo Empezar](#cómo-empezar)
  - [Prerrequisitos](#prerrequisitos)
  - [Instalación y Ejecución](#instalación-y-ejecución)
- [Cómo Probar la API](#cómo-probar-la-api)
  - [1. Crear un Nuevo Usuario (Comando)](#1-crear-un-nuevo-usuario-comando)
  - [2. Obtener un Usuario por ID (Consulta)](#2-obtener-un-usuario-por-id-consulta)
  - [3. Iniciar Sesión (Contexto `auth`)](#3-iniciar-sesión-contexto-auth)
- [Ejecución de Pruebas](#ejecución-de-pruebas)
- [Decisiones Arquitectónicas](#decisiones-arquitectónicas)

## Arquitectura y Decisiones de Diseño

Este proyecto integra varios patrones arquitectónicos para lograr un sistema robusto y desacoplado:

1.  **Arquitectura Hexagonal (Puertos y Adaptadores):** El núcleo de la aplicación (dominio y casos de uso) es completamente independiente de tecnologías externas. La comunicación con el mundo exterior (API REST, bases de datos, colas de mensajes) se realiza a través de "Puertos" (interfaces) que son implementados por "Adaptadores" en la capa de infraestructura. Esto permite cambiar una base de datos o un framework web sin afectar la lógica de negocio.

2.  **CQRS (Command Query Responsibility Segregation):** Se separa estrictamente la lógica para modificar datos (Comandos) de la lógica para leer datos (Consultas).
    *   **Comandos:** Son asíncronos y se procesan a través de una cola de mensajes (`RabbitMQ`). La API responde inmediatamente con un `202 Accepted`, garantizando una alta disponibilidad y resiliencia.
    *   **Consultas:** Son síncronas y van directamente a la base de datos para obtener una respuesta rápida y optimizada para la lectura.

3.  **Bundle-Contexts:** El código está organizado en contextos lógicos (`users`, `auth`). Cada contexto es un módulo autocontenido con sus propias capas de dominio, aplicación e infraestructura. Esta estrategia facilita la escalabilidad, permitiendo añadir nuevas funcionalidades de forma aislada sin afectar al resto del sistema.

## Tech Stack

| Componente                | Tecnología                                   | Propósito                                      |
| ------------------------- | -------------------------------------------- | ---------------------------------------------- |
| Lenguaje                  | **Python 3.11+**                             | Lenguaje principal                             |
| Framework Web             | **FastAPI**                                  | Construcción de APIs REST de alto rendimiento  |
| Base de Datos             | **PostgreSQL**                               | Almacenamiento de datos relacional             |
| ORM                       | **SQLAlchemy (Asyncio)**                     | Mapeo objeto-relacional asíncrono              |
| Cola de Mensajes          | **RabbitMQ**                                 | Procesamiento asíncrono de comandos (CQRS)     |
| Gestión de Dependencias   | **uv / pip + venv**                          | Gestión de paquetes y entornos virtuales       |
| Contenedorización         | **Docker & Docker Compose**                  | Orquestación de servicios en desarrollo        |
| Pruebas                   | **Pytest**                                   | Framework para pruebas unitarias               |
| Calidad de Código         | **Black, Flake8, Isort**                     | Formateo y linting de código                   |

## Estructura del Proyecto

La estructura de carpetas refleja directamente la arquitectura elegida:

```
.
├── alembic/                    # Migraciones de base de datos
├── src/
│   ├── contexts/               # Contenedor de todos los contextos de negocio
│   │   ├── users/              # Contexto de Usuarios
│   │   │   ├── application/    # Casos de uso y puertos
│   │   │   ├── domain/         # Entidades, DTOs y lógica de negocio pura
│   │   │   └── infrastructure/ # Adaptadores (API, Repositorios, etc.)
│   │   └── auth/               # Contexto de Autenticación (similar estructura)
│   ├── core/                   # Lógica transversal (DB, config, excepciones)
│   ├── main.py                 # Punto de entrada de la API (FastAPI)
│   └── user_consumer.py        # Consumidor de RabbitMQ
├── tests/                      # Pruebas unitarias (espejo de la estructura de src/)
├── .env                        # Variables de entorno (no versionado)
├── .flake8                     # Configuración de Flake8
├── docker-compose.yml          # Orquestación de servicios
├── Dockerfile                  # Definición de la imagen de la aplicación
├── pytest.ini                  # Configuración de Pytest
└── requirements.txt            # Dependencias de la aplicación
```

## Cómo Empezar

### Prerrequisitos

-   Docker
-   Docker Compose

### Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/ganfy/backend-hexagonal-cqrs.git
    cd backend-hexagonal-cqrs
    ```

2.  **Crear el archivo de entorno:**
    Copia el archivo `.env.example` o crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
    ```
    # .env
    DATABASE_URL=postgresql+asyncpg://user:password@db:5432/cqrs_project_database
    RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
    ```
    _Nota: Los hostnames `db` y `rabbitmq` corresponden a los nombres de los servicios en `docker-compose.yml`._

3.  **Levantar los servicios con Docker Compose:**
    Este comando construirá la imagen de la aplicación, descargará las imágenes de PostgreSQL y RabbitMQ, y los iniciará.
    ```bash
    docker-compose up --build -d
    ```
    El flag `-d` ejecuta los contenedores en segundo plano.

4.  **Ejecutar las migraciones de la base de datos:**
    Con los servicios corriendo, necesitamos crear las tablas en la base de datos.
    ```bash
    # Primero, crea el entorno virtual local para usar alembic
    python3 -m venv .venv
    source .venv/bin/activate
    uv pip install -r requirements-dev.txt

    # Aplica las migraciones a la base de datos que corre en Docker
    alembic upgrade head
    ```

La aplicación ahora está corriendo y accesible en `http://localhost:8000`.

## Cómo Probar la API

Puedes usar `curl` o cualquier cliente de API (como Postman o Insomnia).

### 1. Crear un Nuevo Usuario (Comando)

Esta petición enviará un comando a RabbitMQ para su procesamiento asíncrono.

```bash
curl -X POST "http://localhost:8000/users/" \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "a_very_strong_password"
}'
```

**Respuesta Esperada (`202 Accepted`):**
```json
{"message":"User creation request accepted."}
```
Puedes ver los logs del consumidor con `docker-compose logs -f consumer` para confirmar que el usuario fue creado en la base de datos.

### 2. Obtener un Usuario por ID (Consulta)

Primero, necesitas obtener el ID de un usuario. Puedes hacerlo conectándote a la base de datos:

```bash
docker-compose exec db psql -U user -d mydatabase -c "SELECT id FROM users;"
```
Copia el UUID devuelto. Luego, úsalo en la siguiente petición (reemplaza `PASTE_YOUR_USER_ID_HERE`):

```bash
curl -X GET "http://localhost:8000/users/PASTE_YOUR_USER_ID_HERE"
```

**Respuesta Esperada (`200 OK`):**
```json
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

### 3. Iniciar Sesión (Contexto `auth`)

Usa las credenciales del usuario que creaste para simular un inicio de sesión.

```bash
curl -X POST "http://localhost:8000/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "password": "a_very_strong_password"
}'
```

**Respuesta Esperada (`200 OK`):**
```json
{
  "access_token": "dummy-jwt-for-John Doe",
  "token_type": "bearer"
}
```

## Ejecución de Pruebas

Las pruebas unitarias están diseñadas para ejecutarse localmente sin necesidad de Docker.

1.  **Asegúrate de tener el entorno virtual activado y las dependencias de desarrollo instaladas:**
    ```bash
    source .venv/bin/activate
    uv pip install -r requirements-dev.txt
    ```

2.  **Ejecuta Pytest:**
    Desde la raíz del proyecto, ejecuta:
    ```bash
    pytest
    ```
    Pytest descubrirá y ejecutará automáticamente todas las pruebas en la carpeta `tests/`.

## Decisiones Arquitectónicas

-   **Asincronía Total:** Se ha utilizado `asyncio` en todo el stack (FastAPI, SQLAlchemy, aio-pika) para un alto rendimiento y concurrencia.
-   **Inyección de Dependencias:** Se aprovecha el sistema `Depends` de FastAPI para inyectar las dependencias (como los casos de uso y las sesiones de base de datos) en la capa de API, promoviendo un bajo acoplamiento.
-   **Pruebas Unitarias vs. Integración:** El foco de este proyecto está en las pruebas unitarias del dominio y la aplicación, usando mocks para aislar la lógica de negocio. Las pruebas de los adaptadores (ej. `UserRepository`) se abordarían mejor con pruebas de integración que se conecten a una base de datos real, lo cual se considerría un siguiente paso.
-   **Seguridad de Contraseñas:** Las contraseñas se hashean utilizando `bcrypt` a través de la librería `passlib`, siguiendo buenas prácticas. Nunca se almacenan contraseñas en texto plano.
