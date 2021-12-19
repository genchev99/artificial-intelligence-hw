import csv
import json
from typing import Generator

DATA_PATH = "./data/voting_records.csv"
K_FOLD = 10


class Classes:
    democrat = "democrat"
    republican = "republican"


class Attributes:
    handicapped_infants = "handicapped_infants"
    water_project_cost_sharing = "water_project_cost_sharing"
    adoption_of_the_budget_resolution = "adoption_of_the_budget_resolution"
    physician_fee_freeze = "physician_fee_freeze"
    el_salvador_aid = "el_salvador_aid"
    religious_groups_in_schools = "religious_groups_in_schools"
    anti_satellite_test_ban = "anti_satellite_test_ban"
    aid_to_nicaraguan_contras = "aid_to_nicaraguan_contras"
    mx_missile = "mx_missile"
    immigration = "immigration"
    synfuels_corporation_cutback = "synfuels_corporation_cutback"
    education_spending = "education_spending"
    superfund_right_to_sue = "superfund_right_to_sue"
    crime = "crime"
    duty_free_exports = "duty_free_exports"
    export_administration_act_south_africa = "export_administration_act_south_africa"

    @classmethod
    def iter_attributes(cls):
        yield cls.handicapped_infants
        yield cls.water_project_cost_sharing
        yield cls.adoption_of_the_budget_resolution
        yield cls.physician_fee_freeze
        yield cls.el_salvador_aid
        yield cls.religious_groups_in_schools
        yield cls.anti_satellite_test_ban
        yield cls.aid_to_nicaraguan_contras
        yield cls.mx_missile
        yield cls.immigration
        yield cls.synfuels_corporation_cutback
        yield cls.education_spending
        yield cls.superfund_right_to_sue
        yield cls.crime
        yield cls.duty_free_exports
        yield cls.export_administration_act_south_africa


class AttributeOptions:
    yes = "yes"
    no = "no"
    na = "na"

    @classmethod
    def from_data(cls, raw: str):
        if raw == "y":
            return cls.yes
        elif raw == "n":
            return cls.no
        elif raw == "?":
            return cls.na
        else:
            raise ValueError(f"Unsupported raw value: {raw}")


def read_data() -> list:
    with open(DATA_PATH, newline='') as csv_fd:
        header = [h.strip() for h in csv_fd.readline().split(',')]
        items = list(csv.DictReader(csv_fd, fieldnames=header))

        for row in items:
            for key in row:
                if key != "class":
                    row[key] = AttributeOptions.from_data(row[key])

        return items


def iter_k_fold(data: list, k: int = K_FOLD) -> Generator:
    length = len(data)
    offset = round(length / k)

    for i in range(k):
        test_from = offset * i
        test_to = offset * (i + 1)

        yield data[0:test_from] + data[test_to:], data[test_from:test_to]


def likeliness(data: list, attribute: str, option: str):
    for d in data:
        if d.get(attribute) is None:
            print(d)
    return sum(1 for d in data if d[attribute] == option) / len(data)


def likeliness_for_attr(data: list, attribute: str):
    return {
        AttributeOptions.yes: likeliness(data, attribute, AttributeOptions.yes),
        AttributeOptions.no: likeliness(data, attribute, AttributeOptions.no),
        AttributeOptions.na: likeliness(data, attribute, AttributeOptions.na),
    }


def calc_attr(data: list, attr: str):
    return {attr: likeliness_for_attr(data, attr)}


def calc_attributes(data):
    res = {}

    for attr in Attributes.iter_attributes():
        res.update(calc_attr(data, attr))

    return res


def train(train_data: list) -> dict:
    democrats = list(filter(lambda x: (x["class"] == Classes.democrat), train_data))
    republicans = list(filter(lambda x: (x["class"] == Classes.republican), train_data))

    total_democrats = len(democrats)
    total_republicans = len(republicans)
    total_all = total_democrats + total_republicans

    results = {
        "total": total_all,
        Classes.democrat: {
            "total": total_democrats,
            "prob": total_democrats / total_all,
            "attributes": calc_attributes(democrats),
        },
        Classes.republican: {
            "total": total_republicans,
            "prob": total_republicans / total_all,
            "attributes": calc_attributes(republicans),
        }
    }

    return results


def classify_helper(train_info: dict, record: dict, cls: str) -> float:
    res = train_info[cls]["prob"]

    for attr in Attributes.iter_attributes():
        res *= train_info[cls]["attributes"][attr][record[attr]]

    return res


def classify(train_info: dict, record: dict) -> str:
    democrats_score = classify_helper(train_info, record, Classes.democrat)
    republicans_score = classify_helper(train_info, record, Classes.republican)

    if democrats_score >= republicans_score:
        return Classes.democrat

    return Classes.republican


def classify_test(train_info: dict, record: dict) -> bool:
    return record["class"] == classify(train_info, record)


def solution():
    data = read_data()

    # for fold in iter_k_fold(list(range(12)), 3):
    #     print("fold: ", fold)

    accuracies = []
    for train_data, test_data in iter_k_fold(data):
        train_info = train(train_data)
        length_of_test_data = len(test_data)
        positive_guesses = sum(1 for record in test_data if classify_test(train_info, record))

        accuracy = positive_guesses / length_of_test_data
        accuracies.append(accuracy)
        print("Accuracy: {:.5f}".format(accuracy))

    print("Average Accuracy: {:.5f}".format(sum(accuracies) / len(accuracies)))


def main():
    solution()


if __name__ == '__main__':
    main()
