import logging
import logging.handlers


def setup_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    logging.getLogger('discord.http').setLevel(logging.WARNING)
    logging.getLogger('discord.player').setLevel(logging.ERROR)  # Only log errors

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    handler.setLevel(logging.WARNING)  # Set handler level to WARNING
    logger.addHandler(handler)

    return logger


