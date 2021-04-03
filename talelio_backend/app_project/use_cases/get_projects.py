from typing import List

from talelio_backend.app_project.domain.project_model import Project
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork


def get_user_projects(uow: UnitOfWork, username: str) -> List[Project]:
    with uow:
        user_record = uow.user.get(User, username=username)

        if user_record is None:
            raise UserError(f"User '{username}' does not exist")

        return user_record.project
