from playground.app import index


def test_index() -> None:
    assert index() == 'Welcome to talel.io'
