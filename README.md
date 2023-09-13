# LPKTA materials seminar

## How to install library using pip?

```commandline
pip install -r requirements.txt
```

## How to deploy to Cloud Function

```commandline
make deploy
```

or 

```commandline
gcloud functions deploy hello_lpkta \
	--region=asia-southeast2 \
	--source=. \
	--runtime=python311 \
	--entry-point=main \
	--trigger-http \
	--allow-unauthenticated
```