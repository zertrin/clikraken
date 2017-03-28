from subprocess import check_output


def test_cli_version():
    ck_ver_output = check_output(['clikraken', '-V'], universal_newlines=True)
    assert 'clikraken version:' in ck_ver_output
