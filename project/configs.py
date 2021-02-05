from logging.config import dictConfig
from pathlib import Path

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{Path(__file__).resolve().parent}/logs/board.log",
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})

db = {
    'USER': 'flask',
    'DATABASE': 'flaskboard',
    'PASSWORD': '1234',
    'PORT': '3306',
    'HOST': 'localhost'
}
