# Lecture League Backend
## Created By: [Andrew Burton](https://github.com/andrewBurrr), [Kyle West](https://github.com/KyleOnTheWorldWideWeb)
### Started on: March 6, 2024
#### Description: ...

## Pre-requisites
Before you begin, ensure you have met the following requirements:
- [Docker](https://docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/)@3.10.13
## Get started
1. **Clone the repository**
```bash
git clone https://github.com/andrewBurrr/LectureLeagueBackend.git
```
2. **Create a Virtual Environment for Python**
   This will help encapsulate any dependencies, and ensure that the projects requirements are as slim as possible
    ```bash
    # Create a virtual environment
    python -m venv venv
        
    # Activate the virtual environment (Windows)
    venv\Scripts\activate
       
    # Activate the virtual environment (macOS/Linux)
    source venv/bin/activate  
    ```
    Now if this is a fresh install you will need to download your backend python dependences.
    ```bash
    # Install Python environment dependences after activating your venv
    # change directory to ~/core/ 
    pip install -r requirements.txt
    ``` 
    This will install all dependencies listed in the requirements file.
3. **Generate Sample Data**
    From the root of the project run the following command to generate sample data.
    ```bash
    python manage.py shell
    >>> from django.contrib.auth.hashers import make_password
    >>> make_password('password')
    ```
    Copy this password into the password variable in the scraper program in order to generate hashed passwords for the sample data.
4. **Run the scraper**
    From the root of the project run the following command to generate sample data.
    ```bash
    python manage.py shell
    >>> from django.contrib.auth.hashers import make_password
    >>> make_password('password')
    ```
    Copy this password into the password variable in the scraper program in order to generate hashed passwords for the sample data. From the Scraper directory run the following command to generate sample data.
    ```bash
    python ucalgary_scraper.py
    ```
   This will create three files in the root of the project. These files are `courses.json`, `institutions.json`, and `users.json`. These files will be used to populate the database with sample data.
5. **Migrate the database**
    From the root of the project run the following command to migrate the database.
    ```bash
    python manage.py makemigrations users && python manage.py migrate
    python manage.py makemigrations institutions && python manage.py migrate
    python manage.py makemigrations && python manage.py migrate
    ```
    This will create the database and apply the migrations to the database.
6. **Run the server**
    From the root of the project run the following command to start the server.
    ```bash
    docker-compose up -d --build
    ```
    This will start the server on `http://localhost:8080/`
6. **Stop the server**
    From the root of the project run the following command to stop the server.
    ```bash
    docker-compose down
    ```
    This will stop the server.
