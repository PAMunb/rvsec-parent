import csv
from rvandroid.constants import *


class Method:
    def __init__(self, class_name: str, name: str, params: str, signature: str, reachable: bool, reaches_mop: bool, directly_reaches_mop: bool, directly_reachable_mop: str):
        self.class_name = class_name
        self.name = name
        self.params = params
        self.signature = signature
        self.reachable = reachable
        self.reaches_mop = reaches_mop
        self.directly_reaches_mop = directly_reaches_mop
        self.directly_reachable_mop = directly_reachable_mop
        self.reached = False

    def __eq__(self, other):
        if isinstance(other, Method):
            return self.signature == other.signature
        return False

    def __hash__(self):
        return hash(self.signature)

    def __str__(self):
        return f"Method=[name={self.name},signature={self.signature},reachable={self.reachable},reaches_mop={self.reaches_mop}, directly_reaches_mop={self.directly_reaches_mop}]"

    def __repr__(self):
        return f"{self.signature}"


class Clazz:
    def __init__(self, name: str, is_activity: bool, is_main_activity: bool):
        self.name = name
        self.is_activity = is_activity
        self.is_main_activity = is_main_activity
        self.methods = set()
        self.fields = set()

    def add_method(self, method: Method):
        if method in self.methods:
            return False
        self.methods.add(method)
        return True

    def add_field(self, field: str):
        self.fields.add(field)

    def __str__(self):
        return f"Clazz=[name={self.name},is_activity={self.is_activity},is_main={self.is_main_activity},method={self.methods}, fields={self.fields}]"

    def __repr__(self):
        return f"[{self.name},{self.is_activity},{self.is_main_activity}]"


class Classes:
    def __init__(self):
        self.classes: dict[str, Clazz] = {}
        self.methods: dict[str, Method] = {}

    def get_classes(self):
        return [self.classes[name] for name in self.classes.keys()]

    def add_clazz(self, name: str, is_activity: bool, is_main_activity: bool) -> Clazz:
        if name not in self.classes:
            self.classes[name] = Clazz(name, is_activity, is_main_activity)
        return self.classes[name]

    def get_clazz(self, name: str):
        if name in self.classes:
            return self.classes[name]
        return None

    def add_method(self, method: Method):
        if method.signature not in self.methods:
            clazz = self.get_clazz(method.class_name)
            if clazz and clazz.add_method(method):
                self.methods[method.signature] = method
                return True
        return False

    def __str__(self):
        text = []
        for name in self.classes:
            text.append(str(self.classes[name]))
        return f"Classes=[classes={text}]"


#class,is_activity,is_main_activity,method,params,reachable,reaches_mop,directly_reaches_mop,signature,mop_methods_reached
def __to_method(line, class_name: str):
    name = line[3]
    params = line[4]
    signature = line[8]
    reachable = eval(line[5].capitalize())
    reaches_mop = eval(line[6].capitalize())
    directly_reaches_mop = eval(line[7].capitalize())
    directly_reachable_mop = line[9]
    return Method(class_name, name, params,signature,reachable,reaches_mop,directly_reaches_mop,directly_reachable_mop)


def read_reachable_methods(in_file: str):
    classes = Classes()
    reachable = {}
    with open(in_file, 'r') as data:
        csv_reader = csv.reader(data, delimiter=',')
        next(csv_reader)
        for line in csv_reader:
            print(line)
            clazz = __to_clazz(line, classes)

            method = __to_method(line, clazz.name)
            classes.add_method(method)

            # if clazz not in reachable:
            #     reachable[clazz] = {IS_ACTIVITY: eval(line[1].capitalize()), METHODS: {}}
            # reachable[clazz][METHODS][method] = {REACHABLE: eval(line[3].capitalize()), USE_JCA: eval(line[4].capitalize())}
    return classes



def __to_clazz(line, classes: Classes):
    name = line[0]
    is_activity = eval(line[1].capitalize())
    is_main_activity = eval(line[2].capitalize())
    return classes.add_clazz(name, is_activity, is_main_activity)