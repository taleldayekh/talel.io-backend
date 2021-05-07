from __future__ import annotations

from contextlib import contextmanager
from io import BytesIO
from types import TracebackType
from typing import Any, Dict, Generator, List, Optional, Tuple, Type, Union

from PIL import Image
from werkzeug.datastructures import FileStorage, ImmutableMultiDict, MultiDict

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_project.domain.project_model import Project
from talelio_backend.app_user.domain.user_model import User


class FakeRepository:
    def __init__(self, fake_db: Dict[str, List[Any]]) -> None:
        self.fake_db = fake_db


class FakeAccountRepository(FakeRepository):
    def add(self, model: Account) -> Account:
        new_id: int
        available_account_ids = []

        if len(self.fake_db['account']):
            for account in self.fake_db['account']:
                available_account_ids.append(account.id)

            new_id = max(available_account_ids) + 1
        else:
            new_id = 1

        setattr(model, 'id', new_id)
        setattr(model.user, 'id', new_id)

        self.fake_db['account'].append(model)
        # Account has relation with user
        self.fake_db['user'].append(model.user)

        return model

    def get(self, _model: Any, **kwargs: Any) -> Union[Account, None]:
        for account in self.fake_db['account']:
            if account.email == kwargs.get('email'):
                return account
        return None


class FakeUserRepository(FakeRepository):
    def get(self, _model: User, **kwargs: Any) -> Union[User, None]:
        for user in self.fake_db['user']:
            if user.id == kwargs.get('id'):
                return user
            if user.username == kwargs.get('username'):
                return user
        return None


class FakeProjectRepository(FakeRepository):
    def get(self, _model: Project) -> List[Project]:
        return self.fake_db['user'][-1].projects


class FakeUnitOfWork:
    fake_db: Dict[str, List[Any]]
    account: FakeAccountRepository
    user: FakeUserRepository
    projects: FakeProjectRepository

    def __init__(self) -> None:
        self.fake_db = {'account': [], 'user': []}
        self.committed = False
        self.account = FakeAccountRepository(self.fake_db)
        self.user = FakeUserRepository(self.fake_db)
        self.projects = FakeProjectRepository(self.fake_db)

    def __enter__(self) -> FakeUnitOfWork:
        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        pass

    def commit(self) -> None:
        self.committed = True


@contextmanager
def generate_request_image_files(
        filenames_with_extensions: List[str]) -> Generator[MultiDict, None, None]:
    request_image_files: List[Tuple[str, FileStorage]] = []

    try:
        for file in filenames_with_extensions:
            filename, extension = file.split('.')
            image = Image.new('RGB', (500, 500))
            image_bytes = BytesIO()
            image.save(image_bytes, format=extension)
            image_bytes.seek(0)

            image.close()

            request_image_file_storage = FileStorage(image_bytes,
                                                     filename,
                                                     content_type=f'image/{extension}')
            request_image_files.append((file, request_image_file_storage))

        yield ImmutableMultiDict(request_image_files)
    finally:
        for request_image_file in request_image_files:
            request_image_file[1].close()
