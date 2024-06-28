# nlp-sql
Proof of concept implementation of low-code/no-code data insgiht extractor


# ROADMAP

- [x] Text encoding and decoding 
- [x] Schema scraping
- [x] Simple form for schema submition (htmx, maybe)
- [x] Schema embedding insertion to vector storage
- [x] Implement vector search for schemas with cosine sim
- [x] Connect OpenAI model(s) to create a SQL prompt with respect to retrieved tables
- [x] (OPITONAL) Containerization (server) (+ command: python src/main.py)


## Requirements

Ensure that Docker and Docker Compose are installed on your system.

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running the Project

1. **Clone this repository:**

   ```bash
   git clone https://github.com/your-username/nlp-sql.git
   cd nlp-sql
   ```

2. **Set up environment variables:**

   Create two `.env` files, one in the `src/db/` directory and one in the `src/utils/` directory, and add the following variables:

   **`src/db/.env`:**

   ```env
   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```

   **`src/utils/.env`:**

   ```env
   OPENAI_API_KEY=
   OPENAI_MODEL=
   OPENAI_EMB_MODEL=
   ```

3. **Build and start the containers using Docker Compose from nlp-sql directory:**

   ```bash
   docker-compose up 
   ```

3. **Access the FastAPI application:**

   After successful startup, the FastAPI application will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Loading CSV Data into PostgreSQL

To load data from a CSV file into the PostgreSQL database, follow these steps:

1. **Ensure the CSV file is included in the repository:**

   The `backup.csv` file should be located in the root of the repository.

2. **Access the PostgreSQL container:**

   ```bash
   docker exec -it nlp-sql-db-1 bash
   ```

3. **Load the CSV data into the database:**

   Inside the PostgreSQL container, run the following command to load the CSV data into the desired table:

   ```bash
   psql -U testuser -d vectordb -c "\COPY db_embeddings FROM '/backup.csv' CSV HEADER;"
   ```

## Project Structure

- `Dockerfile`: Contains instructions to build the Docker image for the FastAPI application.
- `docker-compose.yml`: Defines the services that will be run by Docker Compose, including the FastAPI application and PostgreSQL database.
- `start.sh`: Script for initializing the database and starting the FastAPI server.
- `src/`: Directory containing the FastAPI application source code.

## Commands

### Start the Application

```bash
docker-compose up 
```

### Stop the Application

```bash
docker-compose down
```

## Note

- Ensure that port 8000 is not occupied by other applications.
