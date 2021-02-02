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
            'maxBytes': 1024 * 1024 * 5,    # 2^2 - 4^2 - 16^2
            'backupCount': 5,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})
