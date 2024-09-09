from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

# Google OAuth 설정
oauth.register(
    name='google',
    client_id='GOOGLE_CLIENT_ID',
    client_secret='GOOGLE_CLIENT_SECRET',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth/google/callback',
    client_kwargs={'scope': 'openid profile email'}
)

# Kakao OAuth 설정
oauth.register(
    name='kakao',
    client_id='KAKAO_CLIENT_ID',
    client_secret='KAKAO_CLIENT_SECRET',
    authorize_url='https://kauth.kakao.com/oauth/authorize',
    authorize_params=None,
    access_token_url='https://kauth.kakao.com/oauth/token',
    access_token_params=None,
    redirect_uri='http://localhost:8000/auth/kakao/callback',
    client_kwargs={'scope': 'profile'}
)

