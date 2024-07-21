fish=["マグロ","イカ","タコ","ウナギ"]
seikai=["タコ","ウナギ"]
for sentaku in fish:
    # print(sentaku)
    if sentaku in seikai: 
        print(sentaku,"○")
    else:
        print(sentaku,"×")