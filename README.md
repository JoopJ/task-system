# Task System

## Description
A Flask application that allows the user to create tasks, and be reminded to complete them each day.

## Prerequisites
- Python.3.x
- MySQL 5.x or higher

## Installation
Install the necessary packages listed in `requirements.txt.`

Create a MySQL database. 

Update the `.env` file with your MySQL credentials.

## Environment Variables
The application uses the following environment variables:
 - `DB_HOST`: The hostname of your MySQL server.
 - `DB_USER`: Your MySQL username.
 - `DB_PASSWORD`: Your MySQL password.
 - `DB_NAME`: The name of your MySQL database.


## Usage

1. Run `restart.py` to remove any existing tables and create the necessary tables with a few example tasks.

2. Run `app.py` to start the Flask website. Access locally through http://127.0.0.1:5000. 

3. Stop the application with `Ctrl+C`


## Future Work
- Testing
- End of day check-off of completed tasks
- Mobile device interaction:
    - View today's tasks
- Display point score

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature/bugfix.
3. Commit your changes.
4. Push to your fork and submit a pull request.