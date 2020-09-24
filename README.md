Running Tests:
    In the top level directory:
    python -m pytest
Getting products populated:
    python -m gift_list.staging.import_products
Getting staging gift data:
    python -m gift_list.staging.make_test_gifts
Running (requires products populated. Better with staging data):
    FLASK_APP=run.py flask run --host=0.0.0.0 --port=80

