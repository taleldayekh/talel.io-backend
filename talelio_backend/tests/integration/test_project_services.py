import pytest

from talelio_backend.core.exceptions import UserError
from talelio_backend.tests.integration.helpers import (create_user_project_helper,
                                                       get_user_projects_helper,
                                                       register_account_helper)
from talelio_backend.tests.mocks.projects import talelio_client_project, talelio_server_project
from talelio_backend.tests.utils.constants import USERNAME_BIANCA


def test_can_create_user_project() -> None:
    uow = register_account_helper()
    project_record = create_user_project_helper(uow)

    assert project_record[0].title == talelio_server_project['title']
    assert project_record[0].body == talelio_server_project['body']


def test_cannot_create_user_project_for_non_existing_user() -> None:
    uow = register_account_helper()

    with pytest.raises(UserError, match=f"User '{USERNAME_BIANCA}' does not exist"):
        create_user_project_helper(uow, username=USERNAME_BIANCA)


def test_can_get_user_projects() -> None:
    uow = register_account_helper()

    create_user_project_helper(uow)
    project_record = get_user_projects_helper(uow)

    assert len(project_record) == 1
    assert project_record[0].title == talelio_server_project['title']
    assert project_record[0].body == talelio_server_project['body']

    create_user_project_helper(uow, project=talelio_client_project)
    project_record = get_user_projects_helper(uow)

    assert len(project_record) == 2
    assert project_record[1].title == talelio_client_project['title']
    assert project_record[1].body == talelio_client_project['body']


def test_cannot_get_projects_for_non_existing_user() -> None:
    uow = register_account_helper()

    with pytest.raises(UserError, match=f"User '{USERNAME_BIANCA}' does not exist"):
        get_user_projects_helper(uow, username=USERNAME_BIANCA)
