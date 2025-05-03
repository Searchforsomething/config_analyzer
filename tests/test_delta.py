import pytest

from config_diff_analyzer.delta_applier import apply_delta
from config_diff_analyzer.delta_generator import generate_delta

TEST_CONFIG_PATH = '../test_files/config.json'
TEST_PATCHED_PATH = '../test_files/patched_config.json'
TEST_DELTA_PATH = '../test_files/delta.json'


@pytest.fixture
def malformed_json(tmp_path):
    file_path = tmp_path / "malformed.json"
    file_path.write_text('{"param1": "value",')
    return str(file_path)


@pytest.fixture
def not_a_dict_json(tmp_path):
    file_path = tmp_path / "list.json"
    file_path.write_text('["value1", "value2"]')
    return str(file_path)


@pytest.fixture
def missing_file_path(tmp_path):
    return str(tmp_path / "nonexistent.json")


@pytest.fixture
def invalid_delta_format(tmp_path):
    file_path = tmp_path / "bad_delta.json"
    file_path.write_text('["not", "a", "dict"]')
    return str(file_path)


def test_generate_delta_with_malformed_json(malformed_json, tmp_path, capfd):
    patched_path = tmp_path / "patched.json"
    patched_path.write_text('{"param": "value"}')
    out_path = tmp_path / "delta.json"

    with pytest.raises(SystemExit):
        generate_delta(malformed_json, str(patched_path), str(out_path))

    out, err = capfd.readouterr()
    assert 'Error reading JSON from' in err


def test_generate_delta_with_non_dict_json(not_a_dict_json, tmp_path, capfd):
    patched_path = tmp_path / "patched.json"
    patched_path.write_text('{"param": "value"}')
    out_path = tmp_path / "delta.json"

    with pytest.raises(SystemExit):
        generate_delta(not_a_dict_json, str(patched_path), str(out_path))

    out, err = capfd.readouterr()
    assert 'list.json must be dict, not list' in err


def test_generate_delta_missing_file(missing_file_path, tmp_path, capfd):
    patched_path = tmp_path / "patched.json"
    patched_path.write_text('{"param": "value"}')
    out_path = tmp_path / "delta.json"

    with pytest.raises(SystemExit):
        generate_delta(missing_file_path, str(patched_path), str(out_path))

    out, err = capfd.readouterr()
    assert 'File not found' in err


def test_apply_delta_with_invalid_format(invalid_delta_format, tmp_path, capfd):
    config_path = tmp_path / "config.json"
    config_path.write_text('{"param": "123"}')
    out_path = tmp_path / "res.json"

    with pytest.raises(SystemExit):
        apply_delta(str(config_path), invalid_delta_format, str(out_path))

    out, err = capfd.readouterr()
    assert 'bad_delta.json must be dict, not list' in err


def test_generate_delta(tmp_path):
    generate_delta(TEST_CONFIG_PATH, TEST_PATCHED_PATH, tmp_path)
    delta_files = list(tmp_path.glob('delta*.json'))
    assert len(delta_files) == 1

    delta_path = delta_files[0]
    delta = open(delta_path, 'r').read()
    delta_correct = open(TEST_DELTA_PATH, 'r').read()
    assert delta == delta_correct


def test_apply_delta(tmp_path):
    apply_delta(TEST_CONFIG_PATH, TEST_DELTA_PATH, tmp_path)

    patched_files = list(tmp_path.glob('res_patched_config*.json'))
    assert len(patched_files) == 1

    res_patched_path = patched_files[0]
    res_patched = open(res_patched_path, 'r').read()
    correct_patched = open(TEST_PATCHED_PATH, 'r').read()
    assert res_patched == correct_patched
