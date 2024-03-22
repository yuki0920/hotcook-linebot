.PHONY: run
run:
	@poetry run python hotcook-linebot/main.py

.PHONY: deploy
deploy:
	@gcloud run deploy hotcook-linebot \
		--source=. \
		--no-cpu-throttling \
		--project=${GCP_PROJECT_ID} \
		--region=asia-east1 \
		--set-env-vars=GCP_PROJECT_ID=${GCP_PROJECT_ID} \
		--set-env-vars=LINE_CHANNEL_ACCESS_TOKEN=${LINE_CHANNEL_ACCESS_TOKEN} \
		--set-env-vars=LINE_CHANNEL_SECRET=${LINE_CHANNEL_SECRET} \
		--set-env-vars=OPENAI_API_KEY=${OPENAI_API_KEY} \
		--set-env-vars=PINECONE_API_KEY=${PINECONE_API_KEY} \
		--set-env-vars=PINECONE_INDEX=${PINECONE_INDEX} \
		--set-env-vars=PINECONE_ENV=${PINECONE_ENV}
