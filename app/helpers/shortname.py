import os, sys, json




def get_shortname(json_file):
    company_basename = ''
    catalog_type = ''
    availability =''
    try:
        with open(json_file, 'r') as file:
            job_info = json.load(file)
            company_basename = job_info.get("short_name")
            catalog_type = job_info.get("catalog_type")
            availability = job_info.get("availability")
            file.close()
    except Exception as e:
        print("Error occured: " + e)

    upload_catalog_name =""
    if not company_basename:
        print("Short_name is not detected.")
    else:
        if catalog_type == 'mixed':
            upload_catalog_name = company_basename
        upload_catalog_name = company_basename + catalog_type
        if availability == 'demand':
            upload_catalog_name = upload_catalog_name + "-v"
    return upload_catalog_name

def price_filter(price, short_name):
    pass

def prepare_folders(job_dir):
    pass


def main():
    short_name = get_shortname(sys.argv[1])
    print(short_name)
    return short_name


if __name__=="__main__":
    main()


