# Автоматизация работы с файлами в проектах Gitlab

- update-repositories-file.py - update previously created files in repositories
- create-files-in-repositories.py - create files in repositories

Algorithms:
- Upload the uploaded file to the directory `scripts`
- Create in `scripts/config.py` the `.env` file from the example below
- Install `requirements.txt` 
- Start script `scripts/update-repositories-file.py`
- At the exit, you will receive links with the created merge requests.

## Credentials

`config/.env`

```
URL=https://gitlab.com/
GROUP_NAME=test
PRIVATE_TOKEN=TOKEN
GROUP_ID=1111
REPOSITORIES_NAME=['test']
REF_BRANCH_NAME=master
BRANCH_NAME=fix/update-file
MR_NAME="ci(TICKET): update file"
MR_DESCRIPTION="ci(TICKET): update file"
COMMIT_MESSAGE="ci(TICKET): update file"
FILE_PATH="test.txt"
AUTHOR_EMAIL=gmail.com
AUTHOR_NAME="Ivan Ivanov"
```

PRIVATE_TOKEN=[TOKEN](https://gitlab.com/-/profile/personal_access_tokens)

REPOSITORIES_NAME=['test'] send as a text array

## App list
```
REPOSITORIES_NAME = []
```
