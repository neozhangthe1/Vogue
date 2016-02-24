import shutil
import grequests

path = "../data/images/street2shop/"
f_in = open("../data/street2shop/photos.txt")


def hook_factory(**factory_kwargs):
    def save_image_hook(response, **request_kwargs):
        if response.status_code == 200:
            with open(path + factory_kwargs["name"], 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
                print(factory_kwargs["name"])
    return save_image_hook

action_list = []
cnt = 0
for line in f_in:
    x = line.strip().split(",")
    action_item = grequests.get(x[1], hooks={'response': hook_factory(name=x[0])})
    action_list.append(action_item)
    cnt += 1

grequests.map(action_list)


