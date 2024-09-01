This is a HabitTracker project consist is a few models - habits, notifications(special model with task for a sending notifications by TG Bot), users. More detail  about API endpoints in swagger docs.
Вот как будет выглядеть README файл с инструкциями по запуску проекта:


Habit Tracker Project

This project is a habit tracking system built with Django, Celery, Redis, and PostgreSQL. The project is containerized using Docker and managed with Docker Compose.

Prerequisites

Make sure you have the following installed on your machine:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

To check if Docker and Docker Compose are installed, run:

docker --version
docker-compose --version


Setup

1. Clone the repository:

   
   git clone https://github.com/SilverAnton/HabitTracker.git
   
   

2. Environment Configuration:

   Create a .env file in the root directory of the project and configure the necessary environment variables:

   .env
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   CELERY_BROKER_URL=redis://redis:6379/0
   

3. Build and Run the Containers:

   To build and start all services (Django, PostgreSQL, Redis, Celery, Celery Beat), run:

   
   docker-compose up --build
   

   This command will build and start all containers as defined in the docker-compose.yml file.

4. Check Service Status:

   After running docker-compose up, you can check the status of the containers:

   
   docker-compose ps
   

   You should see all services running with the status - Up.

5. Accessing the Application:

   The Django application will be accessible at [http://localhost:8000](http://localhost:8000).

6. Running Management Commands:

   To run management commands like migrations or creating a superuser, you can execute them inside the `app` container:

   
   docker-compose exec app sh -c "python manage.py createsuperuser"
   

7. Stopping the Containers:

   To stop all running containers, use:

   
   docker-compose down
   

   This will stop and remove the containers defined in the docker-compose.yml.



8. Viewing Logs:
   To see detailed logs for all containers, run:

  
   docker-compose logs -f
   

