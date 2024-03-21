# hotcook-linebot

## Run

```
# setup
poetry config virtualenvs.in-project true --local

# install dependencies
poetry install

# run
make run
```

## Deploy

```
make deploy
```

### Error

Flaskサーバーの起動時にHost '0.0.0.0' を指定したら治った
その他には、環境変数の`PORT`をポートに指定していないケースもある

```
The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable. Logs for this revision might contain more information.
```
