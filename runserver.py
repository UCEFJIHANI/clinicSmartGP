from waitress import serve

from clinicSmart.wsgi import application


if __name__ == '__main__':
    serve(application, host = 'DB_HOST', port='8080')
