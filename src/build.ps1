## I built my app in powershell, using pyinstaller is not cross platform, so you can run this script in your intended environment


python3.exe
pyinstaller --hidden-import google --hidden-import google.auth --hidden-import google.auth.transport.requests --hidden-import google.oauth2.credentials --hidden-import googleapiclient --hidden-import googleapiclient.errors --hidden-import googleapiclient.discovery_cache --hidden-import googleapiclient.discovery --hidden-import google_auth_oauthlib --hidden-import google_auth_oauthlib.flow --hidden-import google_auth_oauthlib.flow --onefile main.py
