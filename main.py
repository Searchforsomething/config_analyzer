from os import makedirs, getenv

from config_diff_analyzer.delta_applier import apply_delta
from config_diff_analyzer.delta_generator import generate_delta
from xml_analyzer.analyzer import parse_xml

if __name__ == '__main__':
    output_dir = getenv('OUTPUT_DIR') if getenv('OUTPUT_DIR') else 'out'
    input_dir = getenv('INPUT_DIR') if getenv('INPUT_DIR') else 'test_files'
    xml_input_path = f'{input_dir}/test_input.xml'
    config_input_path = f'{input_dir}/config.json'
    patched_config_input_path = f'{input_dir}/patched_config.json'

    makedirs(output_dir, exist_ok=True)
    parse_xml(xml_input_path, output_dir)
    delta_path = generate_delta(config_input_path, patched_config_input_path, output_dir)
    apply_delta(config_input_path, delta_path, output_dir)
