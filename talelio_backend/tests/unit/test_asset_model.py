from talelio_backend.app_assets.domain.asset_model import Asset


def test_can_generate_secure_filename() -> None:
    insecure_filename_one = '../../../.bashrc'
    insecure_filename_two = '1 filena@me with spe€cial characters$.jpeg'
    insecure_filename_three = '2 FILENAME WITH CAPITALIZED CHARACTERS.pdf'

    secure_filename_one = Asset().generate_secure_filename(insecure_filename_one)
    secure_filename_two = Asset().generate_secure_filename(insecure_filename_two)
    secure_filename_three = Asset().generate_secure_filename(insecure_filename_three)

    assert secure_filename_one == 'bashrc'
    assert secure_filename_two == '1_filename_with_special_characters.jpeg'
    assert secure_filename_three == '2_filename_with_capitalized_characters.pdf'
