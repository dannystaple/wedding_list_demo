Running Tests:
    In the top level directory:
    python -m pytest
Getting products populated:
    python -m gift_list.staging.import_products
Getting staging gift data:
    python -m gift_list.staging.make_test_gifts
Running:
    FLASK_APP=run.py flask run --host=0.0.0.0 --port=80

The default DB is test - which will be messed with by unit tests.
If you are trying to stage/run, I suggest setting
DB_NAME for that command.

    DB_NAME=staging python -m gift_list.staging.import_products products.json 
    DB_NAME=staging python -m gift_list.staging.make_test_gifts
    DB_NAME=staging FLASK_APP=run.py flask run --host=0.0.0.0 --port=80