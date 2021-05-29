from __future__ import annotations

from contextlib import contextmanager
from io import SEEK_END, BytesIO
from sys import getsizeof
from tempfile import TemporaryFile
from types import TracebackType
from typing import Any, Dict, Generator, List, Optional, Tuple, Type, Union

from PIL import Image
from werkzeug.datastructures import FileStorage, ImmutableMultiDict

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
def generate_file_streams(
        filenames_and_sizes: List[Tuple[str, int]]) -> Generator[List[BytesIO], None, None]:
    image_file_extensions = ['gif', 'jpeg', 'png']
    file_streams: List[BytesIO] = []

    try:
        for filename_and_size in filenames_and_sizes:
            filename, extension = filename_and_size[0].split('.')
            file_size = filename_and_size[1]

            if extension in image_file_extensions:
                image = Image.new('RGB', (500, 500))
                image_stream = BytesIO()
                setattr(image_stream, 'name', filename_and_size[0])
                image.save(image_stream, format=extension)
                image_file_size = getsizeof(image_stream)
                image_stream.seek(0, SEEK_END)
                image_stream.write(b'0' * (file_size - image_file_size))
                image_stream.seek(0)

                file_streams.append(image_stream)
                image.close()
            else:
                with TemporaryFile(suffix=f'.{extension}', prefix=filename) as temp_file:
                    temp_file_size = getsizeof(temp_file)
                    temp_file.write(b'0' * (file_size - temp_file_size))
                    temp_file.seek(0)
                    file_stream = BytesIO(temp_file.read())
                    setattr(file_stream, 'name', filename_and_size[0])

                    file_streams.append(file_stream)
        yield file_streams
    finally:
        for streams in file_streams:
            streams.close()


@contextmanager
def generate_request_files(
        filenames_and_sizes: List[Tuple[str, int]]) -> Generator[ImmutableMultiDict, None, None]:
    try:
        request_files: List[Tuple[str, FileStorage]] = []

        with generate_file_streams(filenames_and_sizes) as file_streams:
            for file_stream in file_streams:
                filename = file_stream.name
                request_file_storage = FileStorage(file_stream, filename)
                request_files.append((filename, request_file_storage))

            yield ImmutableMultiDict(request_files)
    finally:
        for request_file in request_files:
            request_file[1].close()
