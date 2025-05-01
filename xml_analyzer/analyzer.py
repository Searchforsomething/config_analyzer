import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import deque
from xml.dom import minidom

from utils import get_unique_filename
from xml_analyzer.models import Attribute, Class


def topological_sort(classes: dict) -> list:
    graph = {name: set() for name in classes}
    in_degree = {name: 0 for name in classes}

    for cls in classes.values():
        for child in cls.children:
            graph[child.name].add(cls.name)
            in_degree[cls.name] += 1

    queue = deque([name for name in classes if in_degree[name] == 0])
    sorted_classes = []

    while queue:
        cls_name = queue.popleft()
        sorted_classes.append(cls_name)

        for dependent in graph[cls_name]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    return sorted_classes


def validate_xml(file_path) -> ET.ElementTree:
    try:
        tree = ET.parse(file_path)
        return tree
    except ET.ParseError as e:
        print(f'Ошибка в XML: {e}', file=sys.stderr)
        sys.exit(1)


def generate_tree(tree: ET.ElementTree, elements, parent_element) -> ET.ElementTree:
    for attribute in elements[parent_element.tag].attributes:
        sub_element = ET.SubElement(parent_element, attribute.name)
        sub_element.text = attribute.attr_type
    for element in elements[parent_element.tag].children:
        sub_element = ET.SubElement(parent_element, element.name)
        generate_tree(tree, elements, sub_element)
    return tree


def parse_xml(file_path, output_dir='out') -> None:
    tree = validate_xml(file_path)

    root = tree.getroot()
    class_dict = {}
    root_counter = 0

    for class_element in root.findall('Class'):
        class_name = class_element.get('name')
        is_root_str = class_element.get('isRoot')
        if is_root_str == 'true':
            is_root = True
            root_element = class_name
            root_counter += 1
        elif is_root_str == 'false':
            is_root = False
        else:
            print(f'Ошибка в XML: некорректное значение isRoot в классе {class_name}: {is_root_str}', file=sys.stderr)
            sys.exit(1)
        documentation = class_element.get('documentation')
        attributes = []

        for attr in class_element.findall('Attribute'):
            attr_name = attr.get('name')
            attr_type = attr.get('type')
            attributes.append(Attribute(name=attr_name, attr_type=attr_type))

        class_dict[class_name] = Class(
            name=class_name, is_root=is_root, documentation=documentation, attributes=attributes)

    if root_counter != 1:
        print(f'Ошибка в XML: количество корневых классов != 1', file=sys.stderr)
        sys.exit(1)

    for aggregation_element in root.findall('Aggregation'):
        target = aggregation_element.get('target')
        source = aggregation_element.get('source')
        source_multiplicity = aggregation_element.get('sourceMultiplicity')

        if source in class_dict and target in class_dict:
            class_dict[target].add_child(class_dict[source])
            multiplicity = source_multiplicity.split('..')
            class_dict[source].min = int(multiplicity[0])
            class_dict[source].max = int(multiplicity[-1])
        else:
            print(f'Ошибка: Не найдены классы для агрегации {source} -> {target}', file=sys.stderr)
            sys.exit(1)

    config_root = ET.Element(root_element)
    config_tree = ET.ElementTree(config_root)
    generate_tree(config_tree, class_dict, config_root)
    rough_string = ET.tostring(config_root, encoding='utf-8', xml_declaration=False, short_empty_elements=False)
    parsed_string = minidom.parseString(rough_string).toprettyxml(indent='  ')
    formatted_xml = "\n".join(parsed_string.split("\n")[1:])
    formatted_xml = re.sub(r'<(\w+)/>', r'<\1></\1>', formatted_xml)

    os.makedirs(output_dir, exist_ok=True)
    config_name = get_unique_filename(name='config', extension='xml', folder=output_dir)
    with open(config_name, 'a+') as file:
        file.write(formatted_xml)

    json_data = []
    sorted_classes = topological_sort(class_dict)
    for cls in sorted_classes:
        json_data.append(class_dict[cls].to_dict())
    meta_name = get_unique_filename(name='meta', extension='json', folder=output_dir)
    with open(meta_name, 'a+') as file:
        file.write(json.dumps(json_data, indent=4))
    print(f'Результат сохранен в {config_name} и {meta_name}')
