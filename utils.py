def num2class(nrs,type_=2,no_mild=[0,1,2,3]):
    nrs = int(nrs)
    label = ''
    if type_ ==2:
        if nrs in no_mild:
            label = 0
        else:
            label = 1
    else:
        raise Exception(f'there is no type {type_}.')
    return label 
