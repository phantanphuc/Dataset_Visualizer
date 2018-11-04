# Dataset Visualizer


## Prerequisite

+ Programming language: [python3](https://realpython.com/installing-python/)

## Instruction

### Install requirement package

- Install virtual env (optional)

```bash
 $ pip install virtualenv
 ```

- Create virtual env

```bash
$ virtualenv --python={path to python3 executable file} {directory name}
```

- Load virtual env

```bash
$ source {env_directory}/bin/activate
```

- Install Requirement package

```bash
$ pip3 install -r requirements.txt
```

### Running Server

- Make migrations

```bash
$ python ./web/manage.py makemigrations
```

- Migrate Db

```bash
$ python ./web/manage.py migrate
```

- Runserver

```bash
$ python ./web/manage.py runserver
```