import configobj
import json
import os
import csv

def map_parse (options, fname):
    conf = configobj.ConfigObj(fname)
    result = {}


    for elements in conf:
        slov={}
        param = ''
        el = conf[elements]


        for values in el:
            if (values == 'Hint'):
                if isinstance(el[values],str):
                    param = el[values]
                else:
                    for init in el[values]:
                        if not init == 'Count':
                            param += str(el[values][init]) +'\n'
                slov.update({values:param})
            if (values == 'Addresses'):
                adresses = el[values].split('; ')
                slov.update({values:adresses})
            if(values in options):
                slov.update({values:el[values]})
        result.update({elements:slov})

    return result


def into_json(result,fname):

    if (os.path.isfile(fname)):
        os.remove(fname)

    json_file = open(fname,'a+')
    json_file.write( json.dumps (result))
    json_file.close()

    return json_file.name

def into_python (map):
    json_map = open(map,'r')
    python_map = json.load(json_map)
    return python_map

def Group (py_obj):

    sort = {}

    for row in py_obj:
        flag = False
        row_dev = py_obj[row]
        for init in row_dev:
            if init in 'Group':
                if row_dev[init] == '34':
                    flag = True
                else:
                    flag = False
        if flag is True:
            sort.update({row:row_dev})

    return sort

def reader_csv_file(fname):
    table = []
    csv.register_dialect('csv', delimiter=';', quoting=csv.QUOTE_NONE)
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file,'csv')

        for row in csv_reader:
            table.append(row)

    return table

def comparsion (map,table,variable_case):
    _comparsion = []
    _not_identification = {}
    _without_addresses = {}
    for row in map:
        _goal = {}
        addresses = map[row].get(variable_case)
        if addresses:
            for unit in table:
                if isinstance(addresses,str):
                    if addresses == unit[3]:
                        _goal.update({'Matched':addresses, row:map[row], 'IP-Old' : unit[3],'Name' : row})
                    elif addresses == unit[4]:
                        _goal.update({'Matched':addresses, row:map[row], 'IP' : unit[4],'Name' : row})
                else:
                    for Ip in addresses:
                        if Ip  == unit[3]:
                            _goal.update({'Matched':Ip, row:map[row],'IP-Old' : unit[3],'Name' : row})
                        elif Ip == unit[4]:
                            _goal.update({'Matched':Ip, row:map[row],'IP' : unit[4],'Name' : row})
            if _goal:
                _comparsion.append(_goal)
            else:
                _not_identification.update({row:map[row]})
        else:
            _without_addresses.update({row:map[row]})
    return  _not_identification, _comparsion, _without_addresses

def main():

    options = ('Address','Name','ID','Group')

    result_map = map_parse(options,'smartintel.1.map')

    name_json_file = into_json(result_map, 'result_map.json')

    python_object_map = into_python(name_json_file)

    table_hardware = reader_csv_file('result.csv')

    Group_map = Group(python_object_map)

    not_identification_adresses,identification_adresses, without_addresses = comparsion (Group_map,table_hardware,'Addresses')
    not_find_in_excel, find_in_excel,header = comparsion (without_addresses,table_hardware,'Address')
    into_json (identification_adresses, 'identification_adresses.json')
    into_json (without_addresses, 'without_addresses.json')
    into_json (not_identification_adresses, 'not_identification_adresses.json')
    into_json (not_find_in_excel, 'not_find_in_excel.json')
    into_json (find_in_excel, 'find_in_excel.json')
    into_json (header, 'exception.json')
    print ('done')

if __name__ == "__main__":
    main()
