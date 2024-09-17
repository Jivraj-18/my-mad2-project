import os 
class Config:
    path = os.path.join(os.getcwd(), 'database','database.sqlite3')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '386addc430a047042628509dd582f957d9f06dce'
    DEBUG = True
  
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 7777
    CACHE_REDIS_DB = 3
    CORS_HEADERS = 'Content-Type'
