## YT Music Search

Search musics, get music mix and manage playlists 

## Requirements

* Python 3
* Git
* Visual Studio Code (is not required but recommended)

## Dependencies

* [Flask](https://github.com/pallets/flask)
* [ytmusicapi](https://github.com/sigma67/ytmusicapi)
* [Flask-CORS](https://github.com/corydolphin/flask-cors)
* [PyJWT](https://github.com/jpadilla/pyjwt)

## Common setup

Clone the repo and install the dependencies.

```bash
git clone https://github.com/kharkovdenys/ytmusicsearch.git
cd ytmusicsearch
```

**Windows**

```bash
python -m venv .venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux**

```bash
python3 -m venv .venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Configure authentication

Create ***headers_auth.json*** use this [manual](https://ytmusicapi.readthedocs.io/en/latest/setup.html)

## Steps for read-only access

**VS Code**

Select Run and Debug on the Debug start view or press F5

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) and take a look around.

## Deploy project to App Service

**VS Code**

* Install [Azure App Service](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureappservice)
* Sign in to Azure
* Select the Azure icon on the left pane
* Create New Web App
* Deploy project
* [Change](https://portal.azure.com/) Startup Command to `gunicorn --bind=0.0.0.0 --timeout 600 app:myapi`