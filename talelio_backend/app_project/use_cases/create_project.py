from talelio_backend.app_project.domain.project_model import Project
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork


def create_user_project(uow: UnitOfWork, username: str, title: str, body: str) -> Project:
    with uow:
        user_record = uow.user.get(User, username=username)

        if user_record is None:
            raise UserError(f"User '{username}' does not exist")

        new_project = Project(title, body).convert_body_to_html

        user_record.project.append(new_project)
        uow.commit()

        project_record = uow.project.get(Project)

        return project_record
