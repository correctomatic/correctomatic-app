python -m venv .venv
pip install flask psycopg2-binary
pip install debugpy python-dotenv


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
