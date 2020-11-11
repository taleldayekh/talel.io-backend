set-githooks-path:
	git config core.hooksPath .githooks

test:
	pipenv run pytest --cov=./

