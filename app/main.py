from src.presentation.app import create_app
from src.config.settings import Settings


if __name__ == '__main__':
    settings = Settings.load()
    app = create_app()
    app.run(
        host=settings.host,
        port=settings.port,
        debug=settings.debug
    )