import os, sys, csv, io



# def new_parse_csv_info():
#     with open("catalog.csv", "r") as csvfile:
#         raw_data = csvfile.readlines()
#         csvfile.close()
#     product_list = []
#     product_info = {}
#     for item in raw_data:
#         print(item)
#         list = item.split(',')
#         supplier_code = list[0]
#         field = list[1]
#         info = list[2]
#         if 'supplier_code' not in product_info:
#             product_info.update({'supplier_code'})


def get_csv_info(name):
    with open("{0}.csv".format(name)) as csvfile:
        catalog_reader = csv.DictReader(csvfile, delimiter=',')
        catalog_reader  = list(catalog_reader)
        product_code_list = []
        csvfile.close()

    #supplier_code_set = {}
    #for row in catalog_reader:
    #	supplier_code_set.add(row['supplier_code'])
    return parse_info( catalog_reader, name)

def parse_info( catalog_reader, name):
    data_list = []
    data_dict = {}
    prev_sup_code = None
    for row in catalog_reader:
	if prev_sup_code != None and prev_sup_code != row['supplier_code']:
		data_list.append(data_dict.copy())
		data_dict.clear()
        prev_sup_code = row['supplier_code']
	data_dict.update({'supplier_code': prev_sup_code})
        field = row['field']
        field_info = row['synonym']
        data_dict.update({field : field_info})

    # for product_code in supplier_code_list:
    #     data_dict = {}
    #    prev_sup_code = ""
    #    for row in catalog_info:
    #        prev 
    #	    data_dict.update({'supplier_code': product_code})
    #        field = row['field']
    #        field_info = row['synonym']
    #        data_dict.update({field : field_info})
    #    data_list.append(data_dict)
    return write_to_tsv(data_list, name)

#def write_to_tsv(data_list, name):
#     keys = ['supplier_code', 'field', '']
#     with open('formatted_{0}.tsv'.format(name), 'w') as newfile:
#	dict_writer = csv.DictWriter(output_file, keys, delimiter='\t')

def write_to_tsv(data_list, name):
    header_fields = []
    for each in data_list:
        for key in each.keys():
            if key not in sorted(header_fields):
                if key == 'supplier_code':
                    header_fields.insert(0, key)
                else:
                    header_fields.append(key)
    print(header_fields)
    with open('formatted_{0}.tsv'.format(name), 'w') as newfile:
        writer = csv.writer(newfile, delimiter='\t')
        writer.writerow(header_fields)
        for product in data_list:
            values_list = []
            for index in range(len(header_fields)):
                for key, value in product.items():
                    if key == header_fields[index]:
                       values_list.append(value)
            writer.writerow(values_list)





        # header, header_set = [], set()
        # writer.writerow('')  # place holder for header
        # for row in data_list:
        #     for key in row:
        #         if key not in header_set:
        #             header_set.add(key)
        #             header.append(key)
        #     writer.writerow(row.get(col, '') for col in header)

def main():
    input = sys.argv[1]
    csv_file = input.split('.')[0]
    get_csv_info(csv_file)

if __name__=="__main__":
    main()
