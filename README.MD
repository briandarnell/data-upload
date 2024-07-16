
# Data Upload Demonstration Project

Purpose: Demonstrate simple data upload functionality


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Docker installed on your machine
- Docker Compose installed on your machine

## Installation

1. Clone this repository to your local machine:
```bash
git clone https://github.com/briandarnell/data-upload.git
cd data-upload
```

2. Build and start the Docker containers:
```bash
docker-compose up --build
Run database migrations and create a superuser:
```
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

3. Usage
Access the application in your web browser at http://localhost:8000.

4. License
This project is licensed under the MIT License.