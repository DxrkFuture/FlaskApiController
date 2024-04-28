#  FlaskApiController

This is a web application for easy monitoring of system load, including:
- CPU utilization
- RAM usage
- Disk space usage

## Features

- Authorization to the system
- View system statistics

## Installation

Download the project via Git

```
git clone https://github.com/DxrkFuture/FlaskApiController.git
```
Navigate to the project folder
```
cd FlaskApiController
```
Create a workspace
```
python -m venv .venv
```
After you have created an environment, you must activate it:

- In Windows, you can do this by running (at the command line) the file

 ```
 .venv\Scripts\activate.bat
 ```

- In Linux/MacOS you need to run (again, in the terminal) the file using the source command:

```
source .venv/bin/activate
```

(!) The environment is deactivated every time the terminal (console, command line) is closed, so you must activate the environment every time you turn on the command line
If for some reason you want to manually deactivate the environment without closing the terminal, it is enough to call the `deactivate` command

# Install Python dependencies

```
pip install Flask psutil python-dotenv
```

# Startup

Then you can run the project with the command:
```
flask run
```

Verify the deployment by navigating to your server address in
your preferred browser.

```
127.0.0.1:5000
```

# Used in the project

- [Flask](https://flask.palletsprojects.com) - Web framework for creating web applications
- [Bootstrap](https://getbootstrap.com/) -  Web-framewerk for fast layout of adaptive website designs


## License

MIT