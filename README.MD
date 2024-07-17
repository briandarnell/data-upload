
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

Use the navigation bar to explore the features. Data can be uploaded and downloaded. Currently JSON and CSV file formats are supported. A default field mapping is provided and other mappings can be added through the Django admin.

The data and file uploads can be managed further using the Django admin menu. As this is only a demonstration project, an admin login is automatically set up:
* Username: admin
* Password: data_upload_tool
In any product environment, admin credentials should be kept secure and not shared.

## License
This project is licensed under the MIT License.
