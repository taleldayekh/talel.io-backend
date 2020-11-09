## Codebase

### Development

#### Setup

1. Clone repository  

   ```bash
   git clone git@github.com:taleldayekh/talel.io-backend.git
   ```

2. Set Git Hooks path  

   This is necessary for using the hooks located in the `.githooks` directory.

   ```bash
   make set-githooks-path
   ```

#### Code Style

To maintain consistency across the codebase, coding standards that conforms to the _*PEP 8*_ style guide are enforced with the help of:

- [**YAPF**](https://github.com/google/yapf) for reformatting the code.

- [**isort**](https://github.com/PyCQA/isort) for sorting and separating imports.

To help detect errors and reduce bugs the following static code analysis tools are used:

- [**mypy**](https://github.com/python/mypy) for checking type errors.

- [**Pylint**](https://github.com/PyCQA/pylint) for checking programming errors.

