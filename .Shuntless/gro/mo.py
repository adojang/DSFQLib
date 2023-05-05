momname = 'three'
names_list = ['rhino']
nn = 0
print(names_list)
names_list = names_list[:nn] + [item + "_" + momname for item in names_list[nn:]]
print(names_list)
