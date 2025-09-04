import logging.config
from pathlib import Path


def init_logging(file_path: Path):
    logging.config.fileConfig(
        file_path
    )


init_logging(Path(__file__).parent.parent.parent / "logging.conf")
