# Simple Django Catalog

This is a simple exercise to develop a product catalog in Django with the REST Framework.

It's a very basic CRUD API that allows insertion and update of products, plus selection
of stocked/unstocked ones.

## Getting Started

The quickest way to get the project up and running is to use docker-compose, which
will take care of creating and configuring all the necessary docker containers.

`docker-compose up -d`

This will build the Django image locally and spin up two containers:

- PosgreSQL 13.1
- Python 3.9 Alpine

If everything runs successfully, you should be able to access the Django
API navigator at:

`http://localhost:8000/api/products/`

## API Documentation

As per requirements, we have the following endpoints:
1. Register a product with SKU
2. Retrieve Product Details from SKU
3. List all available products (>0 Qty)
4. List all sold out products (0 Qty)
5. Register Qty Change (SKU, +/- Value)

### Insert a product

In order to insert a new product, we call the POST method on the collection

`POST http://localhost:8000/api/products/`

And the following sample payload

```json
{
    "sku": "API1",
    "name": "Api Test 1",
    "price": 15.50,
    "qty": 5
}
```
This will return a 201 upon success and store the product in the database.

### Retrieve product details

In order to retrieve product details, we execute a GET on the collection,
with the product SKU in the url, such as

`GET http://localhost:8000/api/products/API1/`

And it should return a payload similar to the following

```json
{
    "sku": "API1",
    "name": "Api Test 1",
    "price": 15.50,
    "qty": 5,
    "created_at": "2021-01-04T00:58:47.558407Z",
    "updated_at": "2021-01-05T00:39:39.655238Z"
}
```

### Retrieve in stock/out of stock products

In order to retrieve product that are or are not in stock,
we execute a GET on the collection, with the _stock_ URL
parameter.

The _stock_ URL parameter can have two values:
- available
- notavailable

`GET http://localhost:8000/api/products/?stock=available`

And it should return a payload similar to the following

```json
[
    {
        "sku": "API1",
        "name": "Api Test 1",
        "price": 15.50,
        "qty": 5,
        "created_at": "2021-01-04T00:58:47.558407Z",
        "updated_at": "2021-01-05T00:39:39.655238Z"
    }
]
```

`GET http://localhost:8000/api/products/?stock=notavailable`

And it should return a payload similar to the following

```json
[
    {
        "sku": "API0",
        "name": "Api Test 0",
        "price": 15.50,
        "qty": 0,
        "created_at": "2021-01-04T00:58:47.558407Z",
        "updated_at": "2021-01-05T00:39:39.655238Z"
    }
]
```

### Update product quantity

In order to update the product quantity, a PATCH request
must be issued to the following endpoint:

`PATCH http://localhost:8000/api/products/API1/`

And the paylad must contain only the _"qty"_  parameter:

```json
{
    "qty": 5
}
```

**NOTE**: any other parameter or invalid quantity will trigger an API error. Also the PUT method has been completely disabled and triggers an error.

## Tests

Some minor tests have been written to ensure functional consistency, they
can be found in `catalog/tests.py`.

Due to the lack of time they were not automated, but they can be run by
executing only the PostgreSQL instance in docker-compose and then locally
with pipenv:

```bash
# Run docker compose only with the postgres instance
# Then from the base directory of the project run
pip install pipenv && pipenv install --system

pipenv run python manage.py test
```

## TODO

- Fully automate test suite execution
- Add permission system to prevent unauthorized updates
- Add CORS if consumed via browser
- Separate views in their own model
