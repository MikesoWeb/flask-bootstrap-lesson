import os
import random
import shutil


def random_avatar(user):
    full_path = os.path.join(os.getcwd(), 'company/static', 'profile_pics', 'employees_pic', user)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    full_path_avatar = os.path.join(os.getcwd(), 'company/static/Avatars/')
    list_avatars = os.listdir(full_path_avatar)
    lst = random.choice(list_avatars)
    random_image_file = os.path.join(full_path_avatar, lst)
    shutil.copy(random_image_file, full_path)

    return lst
