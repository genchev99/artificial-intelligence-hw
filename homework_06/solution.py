import csv
import math
from operator import itemgetter
from typing import Generator

DATA_PATH = "data/breast_cancer.csv"
K_FOLD = 10
K_DATA_PRUNING = 6


class Classes:
    no_recurrence_events = "no-recurrence-events"
    recurrence_events = "recurrence-events"

    @classmethod
    def iter(cls):
        yield cls.no_recurrence_events
        yield cls.recurrence_events


class Attributes:
    age = "age"
    menopause = "menopause"
    tumor_size = "tumor_size"
    inv_nodes = "inv_nodes"
    node_caps = "node_caps"
    deg_malig = "deg_malig"
    breast = "breast"
    breast_quad = "breast_quad"
    irradiat = "irradiat"

    @classmethod
    def iter(cls):
        yield cls.age
        yield cls.menopause
        yield cls.tumor_size
        yield cls.inv_nodes
        yield cls.node_caps
        yield cls.deg_malig
        yield cls.breast
        yield cls.breast_quad
        yield cls.irradiat


class AttributeOptions:
    age = ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99"]
    menopause = ["lt40", "ge40", "premeno"]
    tumor_size = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"]
    inv_nodes = ["0-2", "3-5", "6-8", "9-11", "12-14", "15-17", "18-20", "21-23", "24-26", "27-29", "30-32", "33-35", "36-39"]
    node_caps = ["yes", "no"]
    deg_malig = ["1", "2", "3"]
    breast = ["left", "right"]
    breast_quad = ["left_up", "left_low", "right_up", "right_low", "central"]
    irradiat = ["yes", "no"]

    @classmethod
    def iter(cls, attr: str):
        if attr not in Attributes.iter():
            raise ValueError(f"Not supported attribute: {attr}")

        return iter(cls.__dict__[attr])


def read_data() -> list:
    with open(DATA_PATH, newline="") as csv_fd:
        header = [h.strip() for h in csv_fd.readline().split(',')]
        # Remove lines with missing data
        items = [d for d in csv.DictReader(csv_fd, fieldnames=header) if "?" not in d.values()]

        return items


def iter_k_fold(data: list, k: int = K_FOLD) -> Generator:
    length = len(data)
    offset = round(length / k)

    for i in range(k):
        test_from = offset * i
        test_to = offset * (i + 1)

        yield data[0:test_from] + data[test_to:], data[test_from:test_to]


def entropy_with_attr(data: list, attr: str) -> float:
    if attr not in Attributes.iter():
        raise ValueError(f"Not supported attribute: {attr}")

    res = 0

    for attr_val in AttributeOptions.iter(attr):
        records = [r for r in data if r[attr] == attr_val]

        res += len(records) / len(data) * entropy(records)

    return res


def entropy(data: list) -> float:
    result = 0
    total = len(data)

    total_of_classes = {}

    for cls in Classes.iter():
        total_of_class = sum([1 for record in data if record["class"] == cls])
        if total_of_class == total:
            return .0

        total_of_classes.update({
            cls: total_of_class
        })

    for cls in Classes.iter():
        total_of_class = total_of_classes[cls]

        if total_of_class == total:
            return .0

        probability = total_of_class / total
        result -= probability * math.log(probability, 2)

    return result


def gain(data: list, attr: str):
    if attr not in Attributes.iter():
        raise ValueError(f"Not supported attribute: {attr}")

    return entropy(data) - entropy_with_attr(data, attr)


def best_gain(data: list, attributes: list) -> tuple:
    gains = [gain(data, attr) for attr in Attributes.iter()]
    _, best_attr = max(zip(gains, attributes), key=itemgetter(0))
    index_of_best_attr = attributes.index(best_attr)

    return best_attr, attributes[:index_of_best_attr] + attributes[index_of_best_attr + 1:]


class NodeTypes:
    pruned = "pruned"
    attr = "attr"
    option = "option"
    leaf = "leaf"


class Node:
    def __init__(self):
        self.value = None
        self.type = None
        self.children = []


def display(curr, level=0):
    curr = curr
    print(f"| {'-' * level * 4} {curr.value} [{curr.type}]")

    for child in curr.children:
        display(child, level + 1)


def id3(data: list):
    root = Node()
    id3_rec(data, available_attributes=list(Attributes.iter()), node=root)

    return root


def majority_class(data: list) -> str:
    counts = []
    for cls in Classes.iter():
        counts.append((cls, sum([1 for d in data if d['class'] == cls])))

    major, _ = max(counts, key=itemgetter(1))
    return major


def id3_rec(data: list, available_attributes: list, node: Node):
    if len(data) <= K_DATA_PRUNING:
        # Missing data pruning
        node.type = NodeTypes.leaf
        node.value = majority_class(data)
        return node

    if entropy(data) == 0 or not available_attributes:
        # TODO: change
        node.value = data[0]["class"]
        node.type = NodeTypes.leaf
        return node

    best_attr, rest_attr = best_gain(data, available_attributes)
    node.value = best_attr
    node.type = NodeTypes.attr

    for option in AttributeOptions.iter(best_attr):
        child = Node()
        child.value = option
        child.type = NodeTypes.option

        node.children.append(child)
        sub_data = [d for d in data if d[best_attr] == option]
        child.children = [id3_rec(sub_data, rest_attr, Node())]

    return node


def _get_child_option_node(root: Node, option: str) -> Node:
    if root.type != NodeTypes.attr:
        raise ValueError("This function can only be executed for attribute Nodes")

    for child in root.children:
        if child.type == NodeTypes.option and child.value == option:
            return child

    raise Exception(f"Couldn't find such option child: {option}")


def _is_option_child_final(option_node: Node):
    """
    An option child is final if it has a child that the predicted class - it's of type leaf
    """
    if option_node.type != NodeTypes.option:
        raise Exception("This function only works with nodes of type option")

    for child in option_node.children:
        if child.type == NodeTypes.leaf:
            return True

    return False


def get_prediction(root: Node, record: dict) -> str:
    # print("rootval:", root.value)
    option = record[root.value]
    # print("option: ", option)

    option_child = _get_child_option_node(root, option)
    if _is_option_child_final(option_child):
        for child in option_child.children:
            if child.type == NodeTypes.leaf:
                return child.value

    return get_prediction(option_child.children[0], record)


def eval_record_decision_tree(root: Node, record: dict):
    return get_prediction(root, record) == record["class"]


def solution():
    data = read_data()

    total_accuracy = []
    for train_data, test_data in iter_k_fold(data):
        root = id3(train_data)
        # display(root)
        positive_hits = 0
        for d in test_data:
            # print(d)
            if eval_record_decision_tree(root, d):
                positive_hits += 1
        # positive_hits = sum([1 for d in test_data if eval_record_decision_tree(root, d)])
        accuracy = positive_hits / len(test_data)
        total_accuracy.append(accuracy)
        print(f"Accuracy: {accuracy}")

    print(f"Average Accuracy: {sum(total_accuracy) / len(total_accuracy)}")


def main():
    solution()


if __name__ == '__main__':
    main()
