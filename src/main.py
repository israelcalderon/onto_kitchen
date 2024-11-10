import random
import types
import owlready2

from collections import namedtuple
from models import (names, last_names, principal_food, entry_food, deserts,
                    fit_food, vegetarian_food)
from typing import Callable


Class = namedtuple('Class', ['name', 'parent'])
Property = namedtuple('Property', ['name', 'domain', 'range', 'parent'])


def random_name() -> str:
    """Creates a random name with last name separated by underscore"""
    return f'{random.choice(names)}_{random.choice(last_names)}'


def random_food(data: list[str]) -> str:
    "Picks a rando dish from the provided data"
    return random.choice(data)


def create_classes(clases: list[Class],
                   onto: owlready2.Ontology) -> dict[str, owlready2.Thing]:
    class_index = {}

    for onto_class in clases:
        with onto:
            base = class_index.get(onto_class.parent) if onto_class.parent \
                else owlready2.Thing

            new_class = types.new_class(onto_class.name, (base,))
            if onto_class.name:
                class_index[onto_class.name] = new_class
    return class_index


def create_properties(properties: list[Property],
                      onto: owlready2.Ontology) -> dict[str, owlready2.ObjectProperty]:  # noqa: E501
    property_index = {}

    for prop in properties:
        with onto:
            base = property_index.get(prop.parent) if prop.parent \
                else owlready2.ObjectProperty
            new_property = type(prop.name, (base,), {
                'domain': [prop.domain],
                'range': [prop.range]
            })

            property_index[prop.name] = new_property
    return property_index


def create_individual(class_: owlready2.Thing, generator: Callable[[], str],
                      onto: owlready2.Ontology, data: list = None) -> None:
    if data:
        class_(generator(data), onto)
    else:
        class_(generator(), onto)


def main(ontology_path: str, ontology_name: str) -> None:
    onto = owlready2.get_ontology(f'https://test.org/{ontology_name}')

    classes = create_classes([
            Class('Persona', None),
            Class('Comensal', 'Persona'),
            Class('Cocinero', 'Persona'),
            Class('Catador', 'Comensal'),
            Class('Repostero', 'Cocinero'),
            Class('Restaurante', None),
            Class('Comida', None),
            Class('Primero', 'Comida'),
            Class('Segundo', 'Comida'),
            Class('Postre', 'Comida'),
            Class('Hipocalorica', 'Comida'),
            Class('Vegetariana', 'Comida')
        ],
        onto)

    create_properties([
        Property('trabaja-en',
                 domain=classes.get('Cocinero'),
                 range=classes.get('Restaurante'),
                 parent=None),
        Property('ofrece',
                 domain=classes.get('Restaurante'),
                 range=classes.get('Comida'),
                 parent=None),
        Property('consume',
                 domain=classes.get('Comensal'),
                 range=classes.get('Comida'),
                 parent=None),
        Property('preparado-por',
                 domain=classes.get('Comida'),
                 range=classes.get('Cocinero'),
                 parent=None),
        Property('cocina',
                 domain=classes.get('Cocinero'),
                 range=classes.get('Comida'),
                 parent=None),
        Property('especialista-en',
                 domain=classes.get('Repostero'),
                 range=classes.get('Postre'),
                 parent='cocina'),
        ],
        onto)

    for _ in range(15):
        create_individual(classes['Persona'], random_name, onto)
        create_individual(classes['Comensal'], random_name, onto)
        create_individual(classes['Cocinero'], random_name, onto)
        create_individual(classes['Catador'], random_name, onto)
        create_individual(classes['Repostero'], random_name, onto)
        create_individual(classes['Cocinero'], random_name, onto)

        create_individual(classes['Primero'], random_food, onto, entry_food)
        create_individual(classes['Segundo'], random_food, onto, principal_food)  # noqa: E501
        create_individual(classes['Postre'], random_food, onto, deserts)
        create_individual(classes['Hipocalorica'], random_food, onto, fit_food)
        create_individual(classes['Vegetariana'], random_food, onto, vegetarian_food)  # noqa: E501

    onto.save(f"{ontology_path}{ontology_name}.rdf")


if __name__ == '__main__':
    path = input('Ontology path, eg: /Users/jane/ontologies/: ')
    name = input('Ontology name: ')
    main(path, name)
