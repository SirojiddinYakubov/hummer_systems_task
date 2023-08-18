import getpass
import os
from pathlib import Path

from . import ConfigMeta

BASE_DIR = Path(__file__).resolve().parent.parent

if getpass.getuser() == "yakubov" or os.getenv("PRODUCTION") == "False":
    env_filename = ".env.dev"
else:
    env_filename = ".env.prod"

ENV_FILE_PATH = f"{BASE_DIR}/deploy/{env_filename}"


class Config(metaclass=ConfigMeta):
    """Set Django config variables."""

    # General Config
    SVC_PORT: int | str
    PRODUCTION: bool
    SECRET_KEY: str
    DEBUG: bool

    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_NAME: str
    DATABASE_HOST: str

    REDIS_HOST: str
    REDIS_PORT: str | int

    INFO_BIP_BASE_URL: str
    INFO_BIP_API_KEY: str

    class Meta:
        env_file = ENV_FILE_PATH


config = Config()
