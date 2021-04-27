from typing import Dict, List, Union
from unittest.mock import patch

from talelio_backend.app_account.use_cases.register_account import register_account, verify_account
from talelio_backend.app_project.domain.project_model import Project
from talelio_backend.app_project.use_cases.create_project import create_project
from talelio_backend.app_project.use_cases.get_projects import get_user_projects
from talelio_backend.app_user.use_cases.authenticate_user import get_access_token
from talelio_backend.tests.constants import EMAIL_TALEL, INITIAL_USER_ID, PASSWORD, USERNAME_TALEL
from talelio_backend.tests.mocks.data import FakeUnitOfWork
from talelio_backend.tests.mocks.projects import talelio_server_project
from talelio_backend.tests.utils import generate_verification_token


def register_account_helper(uow: Union[FakeUnitOfWork, None] = None,
                            email: str = EMAIL_TALEL,
                            username: str = USERNAME_TALEL) -> FakeUnitOfWork:
    with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
        if not uow:
            uow = FakeUnitOfWork()

        register_account(uow, email, PASSWORD, username)  # type: ignore

        return uow


def verify_account_helper(uow: FakeUnitOfWork, email: str = EMAIL_TALEL) -> None:
    verification_token = generate_verification_token({'email': email})
    verify_account(uow, verification_token)  # type: ignore


def create_project_helper(uow: FakeUnitOfWork,
                          user_id: int = INITIAL_USER_ID,
                          project: Union[Dict[str, str], None] = None) -> List[Project]:
    if not project:
        project = talelio_server_project

    title = project['title']
    body = project['body']

    return create_project(uow, user_id, title, body)  # type: ignore


def get_user_projects_helper(uow: FakeUnitOfWork, username: str = USERNAME_TALEL) -> List[Project]:
    return get_user_projects(uow, username)  # type: ignore


def get_access_token_helper(uow: FakeUnitOfWork,
                            email: str = EMAIL_TALEL,
                            password: str = PASSWORD) -> Dict[str, str]:
    return get_access_token(uow, email, password)  # type: ignore
