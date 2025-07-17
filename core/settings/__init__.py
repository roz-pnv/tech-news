import environ

env = environ.Env()
environ.Env.read_env('.env')

SECRET_KEY = env('SECRET_KEY')

if env('PROD', cast=bool):
    from .prod import *
else:
    from .dev import *
    