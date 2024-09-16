from enum import Enum


def get_choices(enum_class: Enum) -> list[tuple[str, str]]:
    """ Format enum choices for use in Django model fields. """
    return [(tag.value, tag.name) for tag in enum_class]
