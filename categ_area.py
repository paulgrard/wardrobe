# -*- coding: utf-8 -*-
from dressingManage.models import Category

h=open("1Hauts.txt",mode='r', encoding = "ISO-8859-1")
lignes_h = h.readlines()

flag=1
n=''
c=''
l=''

for x in lignes_h:
    x=x.rstrip('\n')
    
    if flag==1:
        n=x
        flag=flag+1
    elif flag==2:
        c=x
        flag=flag+1
    else:
        l=x
        flag=1
        newCat = Category(name = n, warmth = c, area = 1, layer=l)
        newCat.save()
        n=''
        l=''
        c=''
    
    print(x)


######################


b=open("2Bas.txt",mode='r', encoding = "ISO-8859-1")
lignes_b = b.readlines()

flag=1
n=''
c=''

for x in lignes_b:
    x=x.rstrip('\n')
    
    if flag==1:
        n=x
        flag=flag+1
    else:
        c=x
        flag=1
        newCat = Category(name = n, warmth = c, area = 2)
        newCat.save()
        n=''
        c=''
    
    print(x)

######################


c=open("3Chaussures.txt",mode='r', encoding = "ISO-8859-1")
lignes_c = c.readlines()

flag=1
n=''
c=''

for x in lignes_c:
    x=x.rstrip('\n')
    
    if flag==1:
        n=x
        flag=flag+1
    else:
        c=x
        flag=1
        newCat = Category(name = n, warmth = c, area = 3)
        newCat.save()
        n=''
        c=''
    
    print(x)


######################


s=open("4Sous-vêtements.txt",mode='r', encoding = "ISO-8859-1")
lignes_s = s.readlines()


for x in lignes_s:
    x=x.rstrip('\n')
    
    newCat = Category(name = x, area = 4)
    newCat.save()    
    print(x)

######################



ch=open("5Chaussettes.txt",mode='r', encoding = "ISO-8859-1")
lignes_ch = ch.readlines()


for x in lignes_ch:
    x=x.rstrip('\n')
    
    newCat = Category(name = x, area = 5)
    newCat.save()    
    print(x)


######################
    

a=open("6Accessoires.txt",mode='r', encoding = "ISO-8859-1")
lignes_a = a.readlines()

flag=1
n=''
c=''

for x in lignes_a:
    x=x.rstrip('\n')
    
    if flag==1:
        n=x
        flag=flag+1
    else:
        c=x
        flag=1
        newCat = Category(name = n, warmth = c, area = 6)
        newCat.save()
        n=''
        c=''
    
    print(x)

################

ab=open("6Accessoires2.txt",mode='r', encoding = "ISO-8859-1")
lignes_ab = ab.readlines()


for x in lignes_ab:
    x=x.rstrip('\n')
    
    newCat = Category(name = x, area = 6)
    newCat.save()
    
    print(x)

