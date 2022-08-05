def num2class(nrs,type_=2):
    nrs = int(nrs)
    label = ''
    if type_ ==2:
        if nrs in [0,1,2,3]:
            label = 0
        else:
            label = 1
    else:
        raise Exception(f'there is no type {type_}.')
    return label 