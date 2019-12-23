#### Add Price api from ShopMolApp here ####

from flask import request
import requests
from app.api import api_bp as api
import json
from app.scripts.tools import parse_item_info, get_catalog_list
from app.data.models.prices import CatalogPricing

from datetime import datetime


@api.route('/_get_data', methods=['GET'])
def _get_new_data():
    start_time = datetime.now()
    molecule_id = request.args.get('molecule_id')
    if molecule_id is not None or molecule_id == '':

        files = {
            'output_fields': (None, 'supplier_code zinc_id cat_id_fk'),
        }

        response = requests.get('http://zinc15.docking.org/substances/{}/catitems.json?count=all'.format(molecule_id), files=files)
        resp = response.json()
        print("Supplier codes found: " + str(len(resp)))
        vendors_list = get_catalog_list()
        result_list = []
        # getting list of supplier code from zinc api
        supplier_codes_list = [item['supplier_code'] for item in resp]

        test, found_supplier_codes = parse_item_info(supplier_codes_list, vendors_list, molecule_id)
        for item in resp:
            if item['supplier_code'] not in found_supplier_codes:
                price_info = DefaultPriceTable.get_default_price_info(item=item, molecule_id=molecule_id, vendors_list=vendors_list)
                if price_info:
                    test.append(price_info)

        end_time = datetime.now()
        total = end_time - start_time
        print("Total time : " + str(total))
        return json.dumps(test)