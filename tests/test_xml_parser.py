import pytest

from main import parse_xml

TEST_INPUT_FILE = '../test_files/impulse_test_input.xml'
CORRECT_CONFIG_FILE = '../test_files/config.xml'
CORRECT_META_FILE = '../test_files/meta.json'


@pytest.fixture
def malformed_xml(tmp_path):
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <Classes>
        <Class name="BTS" isRoot="true" documentation="Base station">
            <Attribute name="id" type="uint32"/>
    </Classes>
    """
    file_path = tmp_path / 'malformed.xml'
    file_path.write_text(xml_content)
    return str(file_path)


@pytest.fixture
def missing_root_xml(tmp_path):
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <Classes>
        <Class name="MGMT" isRoot="false" documentation="Management"/>
    </Classes>
    """
    file_path = tmp_path / 'missing_root.xml'
    file_path.write_text(xml_content)
    return str(file_path)


@pytest.fixture
def multiple_roots_xml(tmp_path):
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <Classes>
        <Class name="BTS" isRoot="true" documentation="Base station"/>
        <Class name="MGMT" isRoot="true" documentation="Management"/>
    </Classes>
    """
    file_path = tmp_path / 'multiple_roots.xml'
    file_path.write_text(xml_content)
    return str(file_path)


@pytest.fixture
def invalid_aggregation_xml(tmp_path):
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <Classes>
        <Class name="BTS" isRoot="true" documentation="Base station"/>
        <Aggregation source="NonExistent" target="BTS" sourceMultiplicity="1"/>
    </Classes>
    """
    file_path = tmp_path / 'invalid_aggregation.xml'
    file_path.write_text(xml_content)
    return str(file_path)


def test_malformed_xml(malformed_xml, capfd):
    with pytest.raises(SystemExit):
        parse_xml(malformed_xml)

    out, err = capfd.readouterr()
    assert 'XML error: mismatched tag' in err


def test_missing_root_class(missing_root_xml, capfd):
    with pytest.raises(SystemExit):
        parse_xml(missing_root_xml)

    out, err = capfd.readouterr()
    assert 'XML error: root classes amount != 1' in err


def test_multiple_roots(multiple_roots_xml, capfd):
    with pytest.raises(SystemExit):
        parse_xml(multiple_roots_xml)

    out, err = capfd.readouterr()
    assert 'XML error: root classes amount != 1' in err


def test_invalid_aggregation(invalid_aggregation_xml, capfd):
    with pytest.raises(SystemExit):
        parse_xml(invalid_aggregation_xml)

    out, err = capfd.readouterr()
    assert 'Error: Classes for aggregation not found' in err


def test_missing_file(capfd):
    with pytest.raises(SystemExit):
        parse_xml('missing_file.xml')

    out, err = capfd.readouterr()
    assert 'File not found' in err


def test_correct_work(tmp_path):
    content = open(TEST_INPUT_FILE, 'r').read()
    file_path = tmp_path / 'correct.xml'
    file_path.write_text(content)
    parse_xml(file_path, tmp_path)
    config_files = list(tmp_path.glob('config*.xml'))
    meta_files = list(tmp_path.glob('meta*.json'))

    assert len(config_files) == 1
    assert len(meta_files) == 1

    config_path = config_files[0]
    config = open(config_path, 'r').read()
    config_correct = open(CORRECT_CONFIG_FILE, 'r').read()
    assert config == config_correct

    meta_path = meta_files[0]
    meta = open(meta_path, 'r').read()
    meta_correct = open(CORRECT_META_FILE, 'r').read()
    assert meta == meta_correct
