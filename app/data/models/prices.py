from app import db
from datetime import datetime
from sqlalchemy.orm import Session
import json
from flask import jsonify
from app.constants import PURCHASABLE


class CatalogPricing(db.Model):
    __tablename__ = 'catalog_prices'
    item_id = db.Column(db.Integer, primary_key=True)
    cat_id_fk = db.Column(db.Integer, unique=True, nullable=False)
    supplier_code = db.Column(db.String(64), unique=True, nullable=False)
    currency = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.String(64), nullable=True)
    quantity = db.Column(db.String(64), nullable=True)
    unit = db.Column(db.String(64), nullable=True)
    shipping = db.Column(db.String(64), nullable=True)
    region = db.Column(db.String(64))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Catalog ID {} - {} : Price {}, Quantity {}>".format(self.cat_id_fk, self.supplier_code, self.price,
                                                                     self.quantity)

    def to_dict(self):
        molecule_info = {}
        molecule_info = {'supplier_code': self.supplier_code,
                         'cat_id_fk': self.cat_id_fk,

                         }
        return molecule_info
    def get_pack_info(self):
        pack = {}
        if self.price in ['0.0', '0', 'NA', 'POA'] or self.price == 0:
            if (self.price != '0' or self.quantity != '0'):
                self.price = 0
                self.currency = None
                self.quantity = 0
                self.unit = None
                self.shipping = str(20)
        else:
            pack = {"price": float(self.price),
                    "currency": self.currency,
                    "quantity": float(self.quantity),
                    "unit": self.unit,
                    "shipping": PURCHASABLE[int(self.shipping)],
                    "region": self.region
                    }
        return pack


    @classmethod
    def get_molecule_info(cls, supplier_codes_list, molecule_id, vendors_list):

        result = []
        found_supplier_codes = set()
        found = cls.query.filter(cls.supplier_code.in_(supplier_codes_list)).all()
        prev_code = ""
        pack_list = []
        molecule_info = {}

        if found:
            print("Length : " + str(len(found)))
            for i in range(len(found)):
                print(i)
                item = found[i]
                if i < len(found) - 1:
                    found_supplier_codes.add(item.supplier_code)
                    print(item)
                    if prev_code != item.supplier_code and prev_code != "":
                        molecule_info.update({"packs": pack_list.copy()})
                        result.append(molecule_info.copy())
                        pack_list.clear()
                        molecule_info.clear()

                    prev_code = item.supplier_code
                    molecule_info.update({"supplier_code": item.supplier_code})
                    molecule_info.update({'query_molecule': molecule_id})
                    molecule_info.update({'cat_id_fk': item.cat_id_fk})
                    molecule_info.update({'cat_name': vendors_list[molecule_info['cat_id_fk']]})
                    pack = item.get_pack_info()
                    if pack:
                        if pack['price'] != 0 or len(pack_list) == 0:
                            pack_list.append(pack)
                    print(pack_list)


                else:
                    molecule_info = item.to_dict()
                    molecule_info.update({'query_molecule': molecule_id})
                    molecule_info.update({'cat_name': vendors_list[molecule_info['cat_id_fk']]})
                    pack = item.get_pack_info()
                    if pack:
                        if pack['price'] != 0 or len(pack_list) == 0:
                            pack_list.append(pack)
                    molecule_info.update({"packs": pack_list.copy()})
                    result.append(molecule_info.copy())

                i += 1
                print(molecule_info)
                print('---------------------------')

        print(json.dumps(result, indent=4))

        return result, found_supplier_codes


    @classmethod
    def get_catalog_content(cls, cat_id_fk):
        content = cls.query.filter_by(cat_id=cat_id_fk).all()
        catalog_content_list = []
        for item in content:
            catalog_content_list.append(item.to_dict())
        return catalog_content_list



# Maybe add a Catalog table to know how many vendors are actually on ZINC