# Tournament Manager

<p align="center"> 
    <img 
        src="http://ForTheBadge.com/images/badges/made-with-python.svg" 
        width="160" 
        >
    <img 
        src="https://forthebadge.com/images/badges/powered-by-pull-requests.svg" 
        width="200" 
        >
</p>

## Screenshots

<img 
    src="https://raw.githubusercontent.com/Madscientiste/P4_openclassroom/main/screenshots/tournament_manager.png" 
    width="850" 
    title="Creating the tournament"
    >
<img 
    src="https://raw.githubusercontent.com/Madscientiste/P4_openclassroom/main/screenshots/tournament_manager_1.png" 
    width="850" 
    title="Tournament has been created"
    >

<img 
    src="https://raw.githubusercontent.com/Madscientiste/P4_openclassroom/main/screenshots/tournament_manager_2.png" 
    width="850" 
    title="In the tournament mode"
    >

<img 
    src="https://raw.githubusercontent.com/Madscientiste/P4_openclassroom/main/screenshots/tournament_manager_3.png" 
    width="850" 
    title="Main menu after quitting the tournament mode"
    >

# Installation & Usage

## Activate venv

### For Windows users:

create venv : `python -m venv .venv`

activate venv : `.\.venv\Scripts\activate`

<hr />

### For Unix users:

1 - create venv : `python3 -m venv .venv`

2 - activate venv : `source .\.venv\bin\activate`

<hr />

## Install the requriements

this will install the required packages for the application

```
pip install -r requirements.txt
```

<hr />

## Usage

after you isntalled everything you can now run the application :

```
python main.py
```

# IMPORTANT NOTES

## 1 - Its recommended to set size of window at 1280x800 minimum

## 2 - To get back to the main menu just press enter

<br />
<hr />

## To Generate a flake report:

be sure to activate **venv** before doing so

```
flake8 --format=html --htmldir=flake-report --max-line-length=120 app
```
