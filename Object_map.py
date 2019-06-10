import configobj
options = ('Address','Name','ID','Group')
itog = {}
count = -1
conf = configobj.ConfigObj('smartintel.1.map')

# print(conf)

for elements in conf:
    slov={}

    el = conf[elements]

    count += 1

    for values in el:
        if (values == 'Hint'):
            if isinstance(el[values],str):
                param = el[values]
            else:
                for init in el[values]:
                    param = '(' + init + '|' + str(el[values][init]) + ')'

            slov.update({values:param})
        if (values == 'Addresses'):
            adresses = el[values].split(';')
            slov.update({values:adresses})
        if(values in options):
            slov.update({values:el[values]})
    itog.update({elements:slov})
print (itog['Device222'])