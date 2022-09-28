# Match predictor

The Match Predictor codebase contains an app with several predictors for football results.

## Local development

Follow the instructions below to get the app up and running on your machine.

1.  Install Python 3.10 and a recent version of NPM.
1.  Install dependencies and run tests.
    ```shell
    make install test
    ```
1.  View the list of available tasks
    ```shell
    make
    ```

## Backend

Here are a few tasks that are useful when running the backend app.
Make sure they all run on your machine.

1.  Run tests
    ```shell
    make backend/test

1.  Run model measurement tests
    ```shell
    make backend/measure
    ```

1.  Run server
    ```shell
    make backend/run
    ```

1.  Run an accuracy report
    ```shell
    make backend/report
    ```

## Frontend

Here are a few tasks that are useful when running the frontend app.
Make sure they all run on your machine.

1.  Run tests
    ```shell
    make frontend/test
    ```

1.  Run server
    ```shell
    make frontend/run
    ```

## Integration tests

If it's helpful, you may want to run integration tests during development.
Do so with the tasks below.

1.  Run tests
    ```shell
    make integration/test
    ```

1.  Interactive mode
    ```shell
    make integration/run
    ```
