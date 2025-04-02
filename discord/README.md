# UPSAIL AI Demo - Discord Integration

This project demonstrates the integration of UPSAIL AI capabilities with a Discord bot. The bot leverages various machine learning models and document retrieval systems to provide intelligent responses and recommendations based on user inputs.

## Features

- **Chat API**: Provides endpoints for sending messages and obtaining product recommendations.
- **Document Retrieval**: Uses a combination of vector stores and document stores to retrieve relevant documents based on user queries.
- **Embeddings**: Utilizes CLIP embeddings for text and image processing.
- **Document Splitting**: Splits product documents into sub-documents based on attributes like images, color, style, etc.
- **FastAPI**: The main application framework used for building the API.
- **Local File Store**: Stores documents locally for retrieval and processing.

## Project Structure

```
├── Dockerfile  
├── Makefile  
├── app   
│   ├── README.md  
│   ├── __init__.py  
│   ├── chat  
│   │   ├── __init__.py  
│   │   ├── chain.py                # ChainManager: access DB, Doc_Store and OpenAI Key
│   │   └── routes.py               # Chat API Routes, points de terminaison pour envoyer des messages et obtenir des recommandations de produits (@chat_router.post("/recommendations")
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py               # 1. Configuration: load environment variables into "settings"
│   ├── main.py                     # 3. FastAPI Application
│   ├── routes.py                   # Legacy code: maybe delete if not used!
│   └── utils
│       ├── __init__.py
│       └── logging.py              # 2. logging to stdout (console) of INFO, WARNING, ERROR, CRITICAL
├── bot
│   ├── __init__.py
│   ├── bot.py
│   ├── command.py
│   ├── config.py
│   ├── handlers
│   │   ├── __init__.py
│   │   ├── base_handler.py
│   │   ├── image_handler.py
│   │   └── text_handler.py
│   ├── healthcheck.py
│   ├── main.py
│   └── views.py
├── chains
│   ├── __init__.py
│   ├── chain_manager.py            # def class ChainManager: la récupération de produits, la génération de questions, et l'organisation des produits recommandés
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── suggestions.py
│   ├── modules
│   │   ├── __init__.py
│   │   ├── embeddings.py           # CLIPembeddings for text and image (get_image_features)
│   │   ├── splitter.py             # diviser un document produit en plusieurs sous-documents basés sur ses attributs (images, couleur, style, occasions, saisons, météo, description).
│   │   └── vectorstore.py          # class MultiModalChroma
│   ├── retriever.py                # load_retriever
│   ├── sale_assistant_chain.py
│   ├── stylist_chain.py
│   └── utils
│       ├── __init__.py
│       ├── formatter.py
│       └── util.py
├── requirements.txt
└── wsgi.py
```

## Deployment

Currently, the app is deployed on a compute engine on GCP.

The app can be found in `/home/fahyik/upsailai-demo`.

To deploy new code:
- Make sure you are on branch `feature/server`.
- Do a `git pull` to fetch updated code.
- Restart `sudo supervisorctl restart fastapi`.

- Stop `sudo supervisorctl stop fastapi`.
- Stop `sudo supervisorctl stop uvicorn`.
- Stop `sudo nginx`.
- `sudo systemctl stop nginx`.

### Installing Python 3.11.2

```sh
brew install pyenv
pyenv local 3.11.2
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/Users/markobriesemann/.local/bin:$PATH"
poetry add fastapi uvicorn
poetry env activate
poetry env info
poetry run pip install torch
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
poetry env use 3.11.2
streamlit run streamlit_backoffice_dashboard.py
```

### Exposing Local IP to the Internet

To expose the local IP to the internet and make it accessible to Vercel, use ngrok:

```sh
brew install ngrok
ngrok config add-authtoken <token>
ngrok http 8000
```

### Nginx Configuration

```sh
tech_it@demo-server:~$ cat /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;

        ##
        # Gzip Settings
        ##

        gzip on;

        # gzip_vary on;
        # gzip_proxied any;
        # gzip_comp_level 6;
        # gzip_buffers 16 8k;
        # gzip_http_version 1.1;
        # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}

#mail {
#       # See sample authentication script at:
#       # http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#       # auth_http localhost/auth.php;
#       # pop3_capabilities "TOP" "USER";
#       # imap_capabilities "IMAP4rev1" "UIDPLUS";
#
#       server {
#               listen     localhost:110;
#               protocol   pop3;
#               proxy      on;
#       }
#
#       server {
#               listen     localhost:143;
#               protocol   imap;
#               proxy      on;
#       }
#}

