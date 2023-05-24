# Self Tracker Application

# Description

This is a Quantified Self application that allows users to create trackers and log events into them. It provides full CRUD (Create, Read, Update, Delete) operations for trackers and logs. The application is built using Flask for the backend and Vue.js for the frontend, with both components running on separate servers. All server calls are made through API requests, and the results are displayed using Vue.js templates.

In addition to the core functionality, the application includes advanced features such as asynchronous tasks and server-side events. These features enable the application to send daily log reminders and monthly reports to users. Celery workers and a Redis database are utilized to accomplish these tasks efficiently.

# Technologies Used

## Frontend Technologies

* HTML: Used as a markup language for documents
* CSS: Applied for styling
* Vanilla JS: Employed for reactivity
* Vue.js: Utilized for reactivity and client-side computations

## Backend Technologies

* Flask: Selected as the framework for backend logic and server implementation
* Gunicorn: Employed to handle multiple HTTP requests concurrently
* SQLite: Utilized as the database for data storage
* Flask SQLAlchemy: Employed as the ORM (Object-Relational Mapping) to interact with the database
* Celery: Utilized for handling asynchronous tasks
* Redis: Employed for message queues and message storage

# Database Schema Design

## Tables

### User
Attributes:

* id (unique identifier for each user)
* username
* email (unique email address for each user)
* password (passwords are securely hashed using bcrypt)
* trackers (points to the tracker table)
* report_format (user preference for monthly reports)

### Tracker
Attributes:

* id (unique identifier for each tracker)
* name
* description
* tracker_type
* settings (points to the settings table)
* logs (points to the logs table)
* user_id (foreign key that points to the user table)
* last_logged

### Logs
Attributes:

* id (unique identifier for each log)
* tracker_id (points to the tracker table)
* note
* value
* user_timestamp
* db_timestamp (timestamp for when the log was added to the database)

### Settings
Attributes:

* name (name of the setting)

### Options (a many-to-many relationship table between tracker and settings)
Attributes:

* tracker_id
* settings_name

## Architecture and Features
The codebase is structured into two folders: backend-code and frontend-code. The backend-code folder contains all server-side files, with main.py serving as the entry point. Within the app folder, you'll find application-related files such as API endpoints, templates, and static files.

The frontend-code folder contains the Vue.js files, specifically inside the tracku folder. The main HTML file (index.html) is located in the public folder, while the main JavaScript file (main.js) and App.vue file are found in the src folder. Components and views are organized within their respective folders.

## Features Implemented

* JWT authentication (implemented using Flask JWT-Extended)
* APIs using Flask-RESTful
* Charts and graphs using Vue-chartjs
* Add-to-desktop feature using vue-pwa
* Notifications using vue-notify
* Daily evening reminders using Celery, Celery Beat, Redis, and Google Chat API (Webhooks)
* Monthly reports using Celery, Celery Beat, and Redis
* Export CSV on every page using Event Stream

Video link - https://youtu.be/O0F12PAFcuo
