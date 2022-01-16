# Match predictor

A few different predictors for English football results.

## Backend

### Run tests

1.  Create a virtual environment.
    ```shell
    cd backend
    python3 -m venv env
    ```

1.  Activate the virtual environment.
    ```shell
    source env/bin/activate
    ```

1.  Install dependencies.
    ```shell
    pip install -r requirements.txt
    ```

1.  Run tests
    ```shell
    python -m unittest
    ```

### Run an accuracy report

```shell
python -m matchpredictor
```

## Frontend

### Run tests

```shell
cd frontend
npm test
```

### Run server

```shell
cd frontend
npm start
```

## Integration tests

```shell
cd integration-tests
npm test
```