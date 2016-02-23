import requests
import shutil

path = "../data/images/street2shop/"
f_in = open("../data/street2shop/photos.txt")

for line in f_in:
    x = line.strip().split(",")
    print(x)
    r = requests.get(x[1], stream=True)
    if r.status_code == 200:
        with open(path + x[0], 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)