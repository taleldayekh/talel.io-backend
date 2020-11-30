from playground.app import index


def test_index() -> None:
    assert index() == 'Hello talel.io'
