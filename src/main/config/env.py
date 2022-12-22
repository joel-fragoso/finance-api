from distutils.util import strtobool
from os import environ, path

from dotenv import load_dotenv  # type: ignore

base_dir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(base_dir, "..", "..", "..", ".env"))


class Config:
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = strtobool(
        environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "True")
    )
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI", "")
