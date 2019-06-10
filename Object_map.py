import configobj
import json
import os

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


def into_json(result):

    if (os.path.isfile('map.json')):
        os.remove('map.json')

    json_file = open('map.json','a+')
    json_file.write( json.dumps (result))
    json_file.close()

    return json_file.name

def into_python (map):
    json_map = open(map,'r')
    python_map = json.load(json_map)
    return python_map

def main():
    options = ('Address','Name','ID','Group')
    result = map_parse(options,'smartintel.1.map')
    name_json_file = into_json(result)
    python_object_map = into_python(name_json_file)
    print (type(python_object_map))

if __name__ == "__main__":
    main()
