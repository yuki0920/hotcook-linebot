# hotcook-linebot

## Run

```
# setup
poetry config virtualenvs.in-project true --local

# install dependencies
poetry install

# run
poetry run python hotcook-linebot/main.py
```

## Deploy

```
gcloud run deploy hootcook-linebot \
  --source=. \
  --no-cpu-throttling \
  --project=$GCP_PROJECT_ID \
  --region=asia-east1 \
  --set-env-vars=GCP_PROJECT_ID=$GCP_PROJECT_ID \
  --set-env-vars=LINE_CHANNEL_ACCESS_TOKEN=$LINE_CHANNEL_ACCESS_TOKEN \
  --set-env-vars=LINE_CHANNEL_SECRET=$LINE_CHANNEL_SECRET \
  --set-env-vars=OPENAI_API_KEY=$OPENAI_API_KEY \
  --set-env-vars=PINECONE_API_KEY=$PINECONE_API_KEY \
  --set-env-vars=PINECONE_INDEX=$PINECONE_INDEX \
  --set-env-vars=PINECONE_ENV=$PINECONE_ENV
```

### Error

Flaskサーバーの起動時にHost '0.0.0.0' を指定したら治った
その他には、環境変数の`PORT`をポートに指定していないケースもある

```
The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable. Logs for this revision might contain more information.
```
