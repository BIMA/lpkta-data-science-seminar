deploy:
	gcloud functions deploy hello_lpkta \
	--region=asia-southeast2 \
	--source=. \
	--runtime=python311 \
	--entry-point=main \
	--trigger-http \
	--allow-unauthenticated