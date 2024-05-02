
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                # "maxBytes": 1000000,
                # "backupCount": 5,
                "filename": "flask.log",
                "formatter": "default",
            },
        },
        "root": {"level": "ERROR", "handlers": ["console", "file"]},
    }
)
