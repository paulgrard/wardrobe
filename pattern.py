from dressingManage.models import Color, Pattern

f=open("patterns_coul.txt",mode='r')
lignes = f.readlines()

flag=1
n=''
c=''
temp=[]


for x in lignes:
    x=x.rstrip('\n')
    
    if flag==1:
        n=x
        flag=flag+1
    elif flag==2:
        flag=flag+1
        print(x)
    else:
        temp = []
        c=x.split("-")
        flag=1
        for i in c:
            temp.append(Color.objects.get(id=i))
        newPat = Pattern(name = n)
        newPat.save()
        for y in temp:
            newPat.colors.add(y)
        n=''
        c=''
    print(temp)
