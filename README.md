# OAuth2.0

# Dependencies
Python 3 (>= 3.6)

# Set up

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Client App
```
OAUTHLIB_INSECURE_TRANSPORT=true FLASK_ENV=development FLASK_APP=client_app/app.py flask run --cert=adhoc --port=5001
```

## Auth Server 
```
OAUTHLIB_INSECURE_TRANSPORT=true FLASK_ENV=development FLASK_APP=oauth_server/app.py flask run --cert=adhoc --port=5002
```

## Resource Server
```
OAUTHLIB_INSECURE_TRANSPORT=true FLASK_ENV=development FLASK_APP=resource_server/app.py flask run --cert=adhoc --port=5003
```

