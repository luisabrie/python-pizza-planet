import pytest
from datetime import datetime


def report_clients_mock() -> dict:
    return [
        {
            'client_name': 'client 1',
            'client_dni': '12345',
            'client_phone': '12345',
            'client_address': 'address 1'
        },
        {
            'client_name': 'client 2',
            'client_dni': '23456',
            'client_phone': '12345',
            'client_address': 'address 2'
        },
        {
            'client_name': 'client 3',
            'client_dni': '34567',
            'client_phone': '12345',
            'client_address': 'address 3'
        },
        {
            'client_name': 'client 4',
            'client_dni': '45678',
            'client_phone': '12345',
            'client_address': 'address 4'
        },
        {
            'client_name': 'client 5',
            'client_dni': '56789',
            'client_phone': '12345',
            'client_address': 'address 5'
        }
    
    ]

def report_ingredients_mock() -> dict:
    return [
        {
            'name': 'ingredient 1',
            'price': 1
        },
        {
            'name': 'ingredient 2',
            'price': 2
        },
        {
            'name': 'ingredient 3',
            'price': 3
        }
    ]
def report_beverages_mock() -> dict:
    return [
        {
            'name': 'beverage 1',
            'price': 1
        },
        {
            'name': 'beverage 3',
            'price': 2
        },
        {
            'name': 'beverage 2',
            'price': 3
        }
    ]

def report_sizes_mock() -> dict:
    return [
        {
            'name': 'size 1',
            'price': 1
        },
        {
            'name': 'size 2',
            'price': 2
        },
        {
            'name': 'size 3',
            'price': 3
        }
    ]


@pytest.fixture
def report_uri():
    return '/report/'


@pytest.fixture
def create_report(client, report_uri) -> dict:
    response = client.get(report_uri)
    return response

@pytest.fixture
def create_report_ingredients_mock(client, ingredient_uri) -> list:
    ingredients = report_ingredients_mock()
    db_ingredients = []
    for ingredient in ingredients:
        new_ingredient = client.post(ingredient_uri, json=ingredient)
        db_ingredients.append(new_ingredient.json)
    return db_ingredients

@pytest.fixture
def create_report_beverages_mock(client, beverage_uri) -> list:
    beverages = report_beverages_mock()
    db_beverages = []
    for beverage in beverages:
        new_beverage = client.post(beverage_uri, json=beverage)
        db_beverages.append(new_beverage.json)
    return db_beverages

@pytest.fixture
def create_report_sizes_mock(client, size_uri) -> list:
    sizes = report_sizes_mock()
    db_sizes = []
    for size in sizes:
        new_size = client.post(size_uri, json=size)
        db_sizes.append(new_size.json)
    return db_sizes

@pytest.fixture
def create_report_order_mock(
    order_uri, 
    client,
    create_report_ingredients_mock, 
    create_report_beverages_mock, 
    create_report_sizes_mock) -> list:
    custom_orders = []
    for i in range(3):
        custom_orders.append({
            **report_clients_mock()[1],
            'date': datetime(2023, 6, 1, 0, 0, 0).isoformat(),
            'ingredients': [ingredient["_id"] for ingredient in create_report_ingredients_mock[0:2]],
            'size_id': create_report_sizes_mock[0]['_id'],
            'beverages': [beverage["_id"] for beverage in create_report_beverages_mock[0:1]]
        })

    for i in range(2):
        custom_orders.append({
            **report_clients_mock()[2],
            'date': datetime(2023, 5, 1, 0, 0, 0).isoformat(),
            'ingredients': [ingredient["_id"] for ingredient in create_report_ingredients_mock[1:3]],
            'size_id': create_report_sizes_mock[1]['_id'],
            'beverages': [beverage["_id"] for beverage in create_report_beverages_mock[1:2]]
        })
    
    custom_orders.append({
        **report_clients_mock()[3], 
        'date': datetime(2023, 5, 1, 0, 0, 0).isoformat(),
        'ingredients': [ingredient["_id"] for ingredient in create_report_ingredients_mock[2:3]],
        'size_id': create_report_sizes_mock[2]['_id'],
        'beverages': [beverage["_id"] for beverage in create_report_beverages_mock[2:3]]
    })
    db_custom_orders = []

    for custom_order in custom_orders:
        new_custom_order = client.post(order_uri, json=custom_order)
        db_custom_orders.append(new_custom_order.json)

    return db_custom_orders