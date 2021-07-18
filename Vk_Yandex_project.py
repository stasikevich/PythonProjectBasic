import os
from os import path
import requests
import time
from tqdm import tqdm
import json
import glob

from pprint import pprint


VK_USER_ID = ""
VK_USER_TOKEN = ''

photo_json = []
photo_list = []


#By Stas Mitin 

class VK:

    def __init__(self, VK_USER_ID, VK_USER_TOKEN, album_id="wall"):

        self.VK_USER_ID = VK_USER_ID
        self.VK_USER_TOKEN = VK_USER_TOKEN
        self.album_id = album_id
        photo_json.append(self)
        photo_list.append(self)

    def get_photo_data(self, offset="0", count="100"):
        self.count = count
        self.offset = offset
        api = requests.get('https://api.vk.com/method/photos.get',
                           params={'owner_id': self.VK_USER_ID, 'access_token': self.VK_USER_TOKEN,
                                   'album_id': self.album_id, 'extended': "1", "count": self.count,
                                   "offset": self.offset, "photo_sizes": '0', 'v': '5.131'})
        return json.loads(api.text)

    def get_photo(self, photos_folder):
        self.photos_folder = photos_folder
        data = self.get_photo_data()
        count_photo = data["response"]["count"]
        index = 0
        count = 5
        photos = []

        while index <= count_photo:
            if index != 0:
                data = self.get_photo_data(offset=index, count=count)
            for files in tqdm(data["response"]["items"]):
                photo_data = {}
                upload_time = time.ctime(files['date'])
                ch_time_1 = upload_time.replace(' ', '_')
                h_upload_time = ch_time_1.replace(":", "_")
                photo_data['size'] = data["response"]["items"][-1]["sizes"][-1]["type"]
                file_url = files['sizes'][-1]['url']
                filename0 = file_url.split("/")[-1]
                filename = filename0.split("?")[0]
                new_filename = filename.replace(filename, (format(files['likes']['count']) + ".jpg"))
                if new_filename in photo_list:
                    photos.append(new_filename)
                    time.sleep(0.1)
                    api = requests.get(file_url)
                    file_name_orig = new_filename.replace(".jpg", "_" + h_upload_time)
                    photo_data['filename'] = file_name_orig
                    photo_list.append(file_name_orig)
                    with open("{}Likes_number_{}.jpg".format(self.photos_folder, file_name_orig), "wb") as file:
                        print(file_name_orig)
                        file.write(api.content)
                else:
                    photos.append(filename)
                    time.sleep(0.1)
                    api = requests.get(file_url)
                    photo_data['filename'] = new_filename
                    photo_list.append(new_filename)
                    with open("{}Likes_number_{}".format(self.photos_folder, new_filename), "wb") as file:
                        print(new_filename)
                        file.write(api.content)
                        print()
                photo_json.append(photo_data)

            index += count
        pprint(len(photos))
        pprint(photo_json)


class YandexDisk:
    def __init__(self, token):
        self.token = token
        # self.file_path = file_path
        # self.file = file

    def get_headers(self):
        return {'Content-type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}

    def upload(self):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        # params = {"path": "vk_image", "overwrite": "true", "templated": "false"}
        # response_upload = requests.get(upload_url, headers=headers, params=params)
        # res = response_upload.json().get("href", "")
        index = 0
        arr = os.listdir(photos_folder)
        for file in tqdm(arr):
            params = {"path": "vk_image/{}".format(arr[index]), "overwrite": "true", "templated": "false"}
            response_upload = requests.get(upload_url, headers=headers, params=params)
            res = response_upload.json().get("href", "")
            try:
                response_url = requests.put(res, data=open("{}\\{}".format(photos_folder, arr[index]), 'rb'))
                print(arr[index])
                response_url.raise_for_status()
                if response_url.status_code == 201:
                    print("Success")

            except FileNotFoundError:
                print("Файл не найден")

            index += 1


if __name__ == "__main__":
    yandex_token = ''
    photos_folder = 'C:\\images\\'
    user1 = VK(VK_USER_ID, VK_USER_TOKEN)
    user1.get_photo(photos_folder)
    user1 = YandexDisk(yandex_token)
    user1.upload()
