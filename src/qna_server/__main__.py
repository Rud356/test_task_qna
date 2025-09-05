import argparse
from pathlib import Path

from qna_server.api.server import main
from qna_server.utils.config_schema import AppConfig, load_config

parser: argparse.ArgumentParser = argparse.ArgumentParser(
    prog="qna_server",
    add_help=True,
    description="Hosts a web server with demo questions and answers api"
)

config: AppConfig = load_config(Path("config.toml"))

main(config)
