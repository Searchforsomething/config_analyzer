class Attribute:
    def __init__(self, name: str, attr_type: str):
        self.name = name
        self.attr_type = attr_type

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.attr_type,
        }


class Class:
    def __init__(self, name: str, is_root: bool, documentation: str, attributes: list[Attribute]):
        self.name = name
        self.is_root = is_root
        self.documentation = documentation
        self.attributes = attributes
        self.children = []
        self.parent = None
        self.min = None
        self.max = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def to_dict(self):
        parameters = []
        for attribute in self.attributes:
            parameters.append(attribute.to_dict())
        for child in self.children:
            parameters.append({'name': child.name, 'type': 'class'})
        class_dict = {
            'class': self.name,
            'isRoot': self.is_root,
            'documentation': self.documentation,
        }
        if self.max is not None:
            class_dict['max'] = self.max
        if self.min is not None:
            class_dict['min'] = self.min
        class_dict['parameters'] = parameters
        return class_dict
