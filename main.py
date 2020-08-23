# main.py
from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(ssl_context="adhoc")
    # app.run(
    #     host=app.config['APP_HOST'],
    #     port=app.config['APP_PORT'],
    #     debug=app.config['APP_DEBUG_FLASK'],
    #     ssl_context=app.config['APP_SSL_CONTEXT']
    # )