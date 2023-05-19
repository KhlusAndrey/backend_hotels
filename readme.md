# Hotel Bookng API 
---

### Backend Hotels is a scalable backend solution designed to power hotel management systems. This project provides a comprehensive set of APIs and services that enable seamless integration with various frontend applications, making it ideal for developing modern hotel booking platforms.

## Key Features

* User Management: The backend system offers secure user authentication and authorization mechanisms, allowing hotel administrators and guests to create accounts, log in, and manage their profiles.

* Booking Management: The project offers powerful booking management capabilities, allowing users to search for available rooms, make reservations, and view booking details. Hotel administrators can track and manage bookings efficiently.

* API Documentation: Detailed API documentation is provided, making it easy for frontend developers to understand and interact with the backend services. The documentation includes information on request/response formats, authentication, and available endpoints.
---

## Technologies Used


[FastAPI](https://fastapi.tiangolo.com/):  The project is built on FastAPI, leveraging its scalability and architecture foundation for building RESTful APIs.

[PostgreSQL](https://www.postgresql.org/): The backend utilizes PostgreSQL, a powerful SQL database, to store and manage hotel, user, bookings and booking data.

[Pydantic](https://docs.pydantic.dev/latest/): Pydantic is data validation and settings management using Python type annotations, simplifying data validation, query building, and schema management.

[JWT Authentication](https://jwt.io/): JSON Web Tokens (JWT) are utilized for secure user authentication and authorization.

[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html): Celery is a simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system. For a Celery broker using [Redis](https://redis.io/) as a message transport or as a result backend.

[Flower](https://flower.readthedocs.io/en/latest/): Flower is a web based tool for monitoring and administrating Celery clusters.

[SQLAdmin](https://aminalaee.dev/sqladmin/): For administration using SQLAdmin is a flexible Admin interface for SQLAlchemy models.

[Pytest](https://docs.pytest.org/en/7.3.x/): For unit, integration app tests using pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications.

[Sentry](https://sentry.io/welcome/): Sentry is a developer-first error tracking and performance monitoring platform that helps developers see what actually matters, solve quicker, and learn continuously about their applications.

[Prometheus FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator): A modular approach to metrics that should instrument all FastAPI endpoints. You can either choose from a set of already existing metrics or create your own. And every metric function by itself can be configured as well.

[Grafana](https://grafana.com/): Grafana is a multi-platform open source analytics and interactive visualization web application in this case connected to Prometheus FastAPI Instrumentator metrics. It provides charts, graphs, and alerts for the web when connected to supported data sources.

[FastAPI versioning](https://github.com/DeanWay/fastapi-versioning): API versioning for fastapi web applications.

[Docker](https://www.docker.com/): Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. 

---

## Getting Started

To get started with Backend Hotels, follow these steps:

1. Clone the repository: git clone `https://github.com/KhlusAndrey/backend_hotels.git`.
2. Configure the environment variables by creating a `.env` file based on the provided `.env.example` file.
3. Build and run Docker Compose. It should run 7 services.
4. The backend will be accessible at `http://localhost:7777/v1/` or the port you set in the `.env` file.

For detailed API documentation and usage examples, please refer to the API Documentation file `openapi.json`.

---
## Tips and tricks

* For generating JWT Secret key use OpenSSL in command line:
```sh
openssl rand -base 64 32
or
openssl rand -hex 32 
``` 
* For checking your database is creating? you could see all databases in container:
```sh
psql -U <DB_USER> -h 127.0.0.0 -p 5432 -l
```
if you don't see your database, create it:
```sh
psql -U <DB_USER> -h 127.0.0.0 -p 5432 -c "CREATE DATABASE <DB_NAME>"
```
restart Docker compose for alembic can make migration and check your tabels in database:
```sh
psql -U <DB_USER> -h 127.0.0.0 -p 5432 <DB_NAME>
# SELECT table_name FROM information_schema.tables WHERE table_schema = "public";
```

* For creating first administrator user, register user, and chenge user's role to admin:
```sh
psql -U <DB_USER> -h 127.0.0.0 -p 5432 <DB_NAME>
# SELECT * FROM users;
# UPDATE users SET role="admin" WHERE id=<user_id>
```
After this setting you'd use administration panel: http://localhost:7777/admin/.

---

## Contributing

Contributions to Backend Hotels are welcome! If you encounter any bugs or have suggestions for improvements, please submit an issue on the GitHub repository. If you'd like to contribute code, please create a pull request.

## License

Backend Hotels is released under the MIT License. Feel free to use, modify, and distribute the code as needed.

Enjoy building your hotel management system with Backend Hotels! If you have any questions or need further assistance, please don't hesitate to reach out.