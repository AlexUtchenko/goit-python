class Meta(type):

    def __init__(cls, name, bases, attrs):
        cls.class_number = Meta.children_number
        Meta.children_number += 1
        super(Meta, cls).__init__(name, bases, attrs)

    children_number = 0


class Cls1(metaclass=Meta):

    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):

    def __init__(self, data):
        self.data = data