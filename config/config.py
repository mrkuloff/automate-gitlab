from os import getenv
from os.path import join, dirname
import ast

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

URL = getenv("URL")
GROUP_NAME = getenv("GROUP_NAME")
PRIVATE_TOKEN = getenv("PRIVATE_TOKEN")
GROUP_ID = int(getenv("GROUP_ID"))
REPOSITORIES_NAME = ast.literal_eval(getenv("REPOSITORIES_NAME"))
REF_BRANCH_NAME = getenv("REF_BRANCH_NAME")

BRANCH_NAME = getenv("BRANCH_NAME")
MR_NAME = getenv("MR_NAME")
MR_DESCRIPTION = getenv("MR_DESCRIPTION")

COMMIT_MESSAGE = getenv("COMMIT_MESSAGE")
FILE_PATH = getenv("FILE_PATH")

AUTHOR_EMAIL = getenv("AUTHOR_EMAIL")
AUTHOR_NAME = getenv("AUTHOR_NAME")