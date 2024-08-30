python -m venv .venv
pip install flask psycopg2-binary
pip install debugpy python-dotenv



## Build and run the container in production

You can build the container with the following command:
```bash
./build.sh
```
To run the container, you need to set the following environment variables:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`: database credentials
- `POSTGRES_HOST`: database host, from the viewpoint of the app container. You can add the database host using the `--add-host` option when running the container.
- `POSTGRES_PORT`: database port, defaults to 5432
- `POSTGRES_DB`: database name
- `CORRECTOMATIC_API_SERVER`: URL of the correctomatic API server from the viewpoint of the app container
- `CALLBACK_HOST`: host and port of this app from the correctomatic viewpoint. You will probably need to set this to `http://host.docker.internal:5000` when running the app in a container.
- `UPLOAD_FOLDER`: folder where uploaded files are stored. Correctomatic doesn't need access to this folder (it makes a copy of the file), so you can set it to any value.

Example of running the container:
```bash
docker run --rm --name correctomatic-app \
    -e POSTGRES_USER=correctomatic \
    -e POSTGRES_PASSWORD=correctomatic \
    -e POSTGRES_HOST=host.docker.internal \
    -e POSTGRES_PORT=5432 \
    -e POSTGRES_DB=correctomatic \
    -e CORRECTOMATIC_API_SERVER=http://host.docker.internal:8080 \
    -e CALLBACK_HOST=http://host.docker.internal:5000 \
    -e UPLOAD_FOLDER=/uploads \
    -v /path/to/uploads:/uploads \
    -p 5000:5000 \
    --add-host=host.docker.internal:host-gateway \
    correctomatic/app
```

## Run the app in development mode

Very important: listen on all hosts, so correctomatic notifier can access this app:

```bash
flask run --debugger --reload --host=0.0.0.0
```

- `.env` contents are loaded automatically by Flask when the app is run in development mode.
- You can open a shell with the app context by running `flask shell`.



Interesant things to check:
- [Custom commands](https://flask.palletsprojects.com/en/3.0.x/cli/#custom-commands)

```sh
flask shell

from app import create_app
app = create_app()
app.url_map
```
