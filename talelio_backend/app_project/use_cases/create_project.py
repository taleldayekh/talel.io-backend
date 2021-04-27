# pylint: disable=W0104
from talelio_backend.app_project.domain.project_model import Project
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import UserError
from talelio_backend.data.uow import UnitOfWork


def create_project(uow: UnitOfWork, user_id: int, title: str, body: str) -> Project:
    with uow:
        user_record = uow.user.get(User, id=user_id)

        if user_record is None:
            raise UserError('User does not exist')

        new_project = Project(title, body)
        new_project.convert_body_to_html

        user_record.projects.append(new_project)
        uow.commit()

        project_record = uow.projects.get(Project)

        return project_record
