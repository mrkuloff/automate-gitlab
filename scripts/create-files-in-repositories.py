from typing import AnyStr, Optional

import gitlab

from dotenv import load_dotenv
from gitlab.v4.objects import Group, Project

from config.config import URL, PRIVATE_TOKEN, GROUP_ID, REPOSITORIES_NAME, BRANCH_NAME, AUTHOR_EMAIL, AUTHOR_NAME, REF_BRANCH_NAME, FILE_PATH, COMMIT_MESSAGE, MR_NAME, MR_DESCRIPTION, GROUP_NAME

load_dotenv()

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

def get_file_content(fname: str) -> Optional[AnyStr]:
    try:
        with open(fname, 'r') as my_file:
            return my_file.read()
    except:
        print(f'Error occurred when opening {fname} to read')
        return None

def create_branch(project: Project) -> bool:
    try:
        if not BRANCH_NAME in [branches.name for branches in project.branches.list()]:
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
                                           'description': MR_DESCRIPTION})
        print(f'{URL}{GROUP_NAME}/{str(project.path)}/-/merge_requests/{mr.get_id()}')
        return True
    except:
        return False

def create_file_in_repository(project: Project, file_content: AnyStr) -> bool:
    create_branch(project)
    add_file_in_repository(project, file_content)
    create_merge_request(project)
    return True

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

if __name__ == "__main__":
    gitlab_auth()