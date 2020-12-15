# SecureWeb

SecureWeb is a Python command for automating schedule and paystub retrieval for **only those that have a valid SecureWeb account**. This command-line utility allows you to store paystubs and schedules in PNG and ICS format. Schedule Screenshots are stored as ```Schedule.png``` and ICS files are stored as ```Schedule.ics``` within the ```SecureWeb``` directory. 

  

## Installation

Install pipenv if not installed on system, assuming pip3 is installed:
```bash
pip3 install pipenv
```

Now that pipenv is installed, navigate to this project's folder, or wherever you've installed it:
```bash
cd /path/to/SecureWeb
```

Execute the following Pipenv command to install the dependencies needed for this project found within the Pipfile:
```bash
pipenv install
```

If Pipenv isn't installing properly, edit the Pipfile, and change the python version in the Pipfile:
```bash
# Find Python3 version
python3 --version

# Edit this part of the Pipfile to whatever python version you have. 
[requires]
# Set python_version to 3.9 ONLY if you have version 3.9. If you have 3.8 or 3.7 set it to that
python_version = "3.9"
```
  

## Configuring Credentials for SecureWeb login

  

First, navigate to the directory where you downloaded the project:

```bash
cd /path/to/SecureWeb
```

Create a file named "creds.env" to store credentials:

```bash
touch creds.env
```

Use your favorite text editor to edit the file you just created:
```bash
nano creds.env
```

Create two environment variables, and set them equal to your credentials

```bash
USER="yourusernamegoeshere"
PASS="yourpasswordgoeshere"
```

  

## Usage

```bash
# If you want to get a screenshot of your schedule
python3 SecureWeb.py schedule

# If you want to get your most recent paystub
python3 SecureWeb.py pay --week 0

# If you want to get a paystub from 1 pay period BEFORE your most recent paystub
python3 SecureWeb.py pay --week 1

# If you want to get your paystub from 2 pay periods BEFORE your most recent paystub
python3 SecureWeb.py pay --week 2

# If you want to get all consecutive paystubs ranging from your most recent to 5 pay periods BEFORE your most recent paystub
python3 SecureWeb.py paybulk --week 5
```

  

## License

[MIT](https://choosealicense.com/licenses/mit/)
