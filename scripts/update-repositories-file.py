import base64
from itertools import zip_longest
from typing import AnyStr, Optional

import gitlab

from gitlab.v4.objects import Group, Project

from config.config import URL, PRIVATE_TOKEN, REPOSITORIES_NAME, BRANCH_NAME, AUTHOR_EMAIL, AUTHOR_NAME, REF_BRANCH_NAME, FILE_PATH, COMMIT_MESSAGE, MR_NAME, MR_DESCRIPTION, GROUP_NAME, GROUP_ID


def get_projects_id(group: Group) -> list[int]:
    project_ids = list()
    for project in group.projects.list(iterator=True):
        if project.name in REPOSITORIES_NAME and GROUP_NAME is not None:
            project_ids.append(project.id)
        elif GROUP_NAME is None:
            project_ids.append(project.id)
    return project_ids

def get_all_names_in_project(project: Project) -> list[str]:
    items = project.repository_tree(path='/', ref=REF_BRANCH_NAME)
    return [item['name'] for item in items]

def get_file_content(config_file: str):
    try:
        with open(config_file, "r", encoding="utf8") as my_file:
            return my_file.read()
    except Exception as ex:
        print(f'Error occurred when opening {config_file} to read.\n\nException: \n{ex}')
        return None

def create_branch(project: Project) -> bool:
    try:
        if not BRANCH_NAME in [branches.name for branches in project.branches.list(iterator=True)]:
            project.branches.create({'branch': BRANCH_NAME,
                                              'ref': REF_BRANCH_NAME})
        return True
    except:
        return False


def add_file_in_repository(project: Project, file_content: AnyStr):
    f = project.files.create({'file_path': FILE_PATH,
                              'branch': BRANCH_NAME,
                              'content': file_content,
                              'author_email': AUTHOR_EMAIL,
                              'author_name': AUTHOR_NAME,
                              'commit_message': COMMIT_MESSAGE}
                             )

def create_merge_request(project: Project) -> bool:
    try:
        mr = project.mergerequests.create({'source_branch': BRANCH_NAME,
                                           'target_branch': REF_BRANCH_NAME,
                                           'title': MR_NAME,
                                           'description': MR_DESCRIPTION,
                                           'remove_source_branch': True,
                                           'squash': True
                                           })
        print(f'{URL}{GROUP_NAME}/{str(project.path)}/-/merge_requests/{mr.get_id()}')
        return True
    except:
        return False

def create_file_in_repository(project: Project, file_content: AnyStr) -> bool:
    create_branch(project)
    add_file_in_repository(project, file_content)
    create_merge_request(project)
    return True

def print_diff_files(content_one: AnyStr, content_two: AnyStr) -> bool:
    for line1, line2 in zip_longest(content_one, content_two, fillvalue=None):
        if line1 == line2:
            continue
        else:
            return False
    return True

def get_git_file_content(project: Project, file_path: str = FILE_PATH) -> Optional[AnyStr]:
    try:
        file = project.files.get(file_path=file_path, ref=REF_BRANCH_NAME)
        file_content = base64.b64decode(file.content).decode("utf-8")
        return file_content
    except gitlab.exceptions.GitlabGetError:
        return None

def create_commit(project: Project, content: AnyStr):
    data = {
        'branch': BRANCH_NAME,
        'commit_message': COMMIT_MESSAGE,
        'actions': [
            {
                'action': 'update',
                'file_path': FILE_PATH,
                'content': content,
            }
        ]
    }
    project.commits.create(data)

def change_file(project: Project, file_content: AnyStr) -> bool:
    git_file = get_git_file_content(project, FILE_PATH)
    diffs = print_diff_files(file_content, git_file)
    if not diffs:
        create_branch(project)
        create_commit(project, file_content)
        create_merge_request(project)
        return True
    return False

def gitlab_auth():
    file_content = get_file_content(FILE_PATH)
    gl = gitlab.Gitlab(url=URL,
                       private_token=PRIVATE_TOKEN)
    groups = gl.groups.get(GROUP_ID)
    project_ids = get_projects_id(groups)
    for project_path in project_ids:
        project = gl.projects.get(project_path)
        item_names = get_all_names_in_project(project)
        if not FILE_PATH in item_names:
            create_file_in_repository(project, file_content)
        else:
            change_file(project, file_content)


if __name__ == "__main__":
    gitlab_auth()