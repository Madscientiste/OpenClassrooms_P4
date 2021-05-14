# Tournament Manager

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

### NOTE

Its recommended to set size of window at 1280x800 min

<hr />

## To Generate a flake report:

be sure to activate **venv** before doing so

```
flake8 --format=html --htmldir=flake-report --max-line-length=120 app
```
