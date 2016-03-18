from dressingManage.models import Color

f=open("color.txt",mode='r')
lignes = f.readlines()

flag=1
n=''
c=''

for x in lignes:
    x=x.rstrip('\n')
    
    if flag==1:
        n=x
        flag=flag+1
    else:
        c=x
        flag=1
        newColor = Color(name = n, code = c)
        newColor.save()
        n=''
        c=''
    
    print(x)
