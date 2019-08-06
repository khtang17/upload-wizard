import os, sys,csv, json
import re, timeit



def get_price_tag(folder):
    json_path = folder +"/" +"JOB_INFO.json"
    try:
        with open(json_path, "r") as json_file:
            job_info = json.load(json_file)
            json_file.close()
        price_tag = job_info['price_tag']
        return price_tag
    except IOException as e:
        print(e)

def parse_price_dict(price_tag, csv_file):
    price_dict = {}
    with open(csv_file) as fh:
        catalog_reader = csv.DictReader(fh, delimiter=',')
        for row in catalog_reader:
            if row['field'] == price_tag:
                price = int(re.sub('[^0-9]','', row['synonym']))
                if price == 0 or price == '' or price is None:
                    price = None
                item = {row['supplier_code'] : price}
                price_dict.update(item)
    return price_dict

def parse_smiles_file(smiles):
    smiles_dict = {}
    with open(smiles) as fh:
        list = fh.readlines()
        for line in list:
            splitted_line = line.split(' ')
            smiles = splitted_line[0]
            product_code = splitted_line[1]
            smiles_dict.update({product_code: smiles})
        fh.close()
    return smiles_dict

def do_filter(smiles_dict, prices_dict):
    economical = {}
    items = {}
    standard = {}
    premium = {}
    for product_code, smile in smiles_dict.items():
        if product_code not in prices_dict.keys():
            price = prices_dict.get(product_code)
            print(price)
        else:
            economical.update({product_code: smile})
    print(economical)



def main():
    start = timeit.timeit()
    job_folder = sys.argv[1]
    price_tag = get_price_tag(folder=job_folder)
    file_list = os.listdir(job_folder)
    for file in file_list:
        if file.endswith('.csv'):
            csv_file = file
        elif file.endswith(".smi"):
            smi_file = file
    prices_dict = parse_price_dict(price_tag, csv_file)
    smiles_dict = parse_smiles_file(smi_file)
    do_filter(smiles_dict, prices_dict)
    end = timeit.timeit()
    print("Time elapsed: " + str(end-start))
if __name__=='__main__':
    main()