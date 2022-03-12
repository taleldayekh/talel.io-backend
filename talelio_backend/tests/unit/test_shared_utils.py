from talelio_backend.shared.utils import generate_slug


def test_generates_slug_with_word_characters_only() -> None:
    string = '@talel, the #slug for this string should contain 54 word characters!'
    slug = 'talel-the-slug-for-this-string-should-contain-54-word-characters'

    assert generate_slug(string) == slug


def test_generates_slug_in_lowercase() -> None:
    string = 'THE SLUG FOR THIS STRING SHOULD BE ALL LOWERCASE'
    slug = 'the-slug-for-this-string-should-be-all-lowercase'

    assert generate_slug(string) == slug


def test_generates_slug_with_normalized_text() -> None:
    string = 'Den här texten kommer att sakna både "ä" och "å"'
    slug = 'den-har-texten-kommer-att-sakna-bade-a-och-a'

    assert generate_slug(string) == slug
