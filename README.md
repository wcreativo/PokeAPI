# PokeAPI

Poke-berries statistics API.

## Environment Setup

### Prerequisites

- Docker
- Docker Compose

### Steps to Run the Project

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/wcreativo/poke-api
   cd poke-api
   ```

2. **Environment Configuration:**

    Create a .env file based on the .env.example template and fill in the necessary environment variables.

3. **Build and Launch Containers:**

    ```bash
    docker-compose up --build
    ```

### Testing

```bash
docker exec -it django pytest
```

### Access Information

* The server will be available at http://localhost:8000
* API Documentation: http://localhost:8000/api/docs/
* Admin Interface Documentation: http://localhost:8000/admin/

### Technologies

* DRF
* Docker
* Postgres
* Redis
* Numpy
