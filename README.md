# keeps-updates
Google Keepをリスト形式で表示するためのスクリプトです。<br>
現状では、過去１週間以内のNoteからURLを抜き出して、リスト形式で表示できます。<br>

~~Google Keep APIが一般ユーザでも使用可能になるまで保留~~<br>
[gkeepapi](https://gkeepapi.readthedocs.io/en/latest/#)で代用することにした。

---

## Setup Login Account:
Create `.env` File and Set `USERNAME` and `PASSWORD`:
```.env
USERNAME = ""
PASSWORD = ""
```

**NOTE**
You can generate an app password(for this app) on [apppasswords](https://myaccount.google.com/apppasswords).

## Run locally:
Setup Local Python Environment:
```
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Run the server locally:
```
FLASK_APP=main.py flask run
```

Check it out: http://127.0.0.1:5000/

Run Locally with Buildpacks & Docker:
```
pack build --builder=gcr.io/buildpacks/builder keeps-updates
docker run -it -ePORT=8080 -p8080:8080 keeps-updates
```

Check it out: http://127.0.0.1:8080/

## Run on Cloud Run:
Deploy from source using the following command:
```
gcloud run deploy
```

**NOTE**
If you have any questions, please check [deploy quickstarts](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python#deploy).

[Setup login account](#setup-login-account) and Click this:

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)
