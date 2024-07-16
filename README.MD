
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
```
This command will also automatically migrate the necessary database changes and create a Django superuser.

## Usage
Access the application in your web browser at http://localhost:8000.
As this is only a demonstration project, an admin login is automatically set up:
Username: admin
Password: data_upload_tool

## License
This project is licensed under the MIT License.