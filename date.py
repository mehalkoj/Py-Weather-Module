from datetime import *

x = date.today()
print(x)
a = date(2020, 5, 17)

print(a)

if x > a:
    print("date past", a)
elif x == a:
    print("atch")
else:
    print("cool")
