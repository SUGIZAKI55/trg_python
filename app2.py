import random
r = random.randint(1,6)
print(r)
if r==6:
    print("大当たり")
elif r==5 or r==4:
     print("中当たり")
else:
    print("ハズレ")