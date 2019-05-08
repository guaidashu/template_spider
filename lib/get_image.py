"""
author songjie
"""
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from tool.lib.db import DBConfig
from tool.lib.function import curl_data, debug

lock = threading.RLock()

GET_CONFIG = {
    "path": ""
}


class GetImages(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        self.get_images(data, "large", img_url="img_url_large")

    @classmethod
    def start_thread(cls, data, fun, path, img_url, prefix):
        thread_pool = ThreadPoolExecutor(max_workers=15)
        task_list = list()
        result = list()
        for item in data:
            task = thread_pool.submit(fun, item, path, img_url, prefix)
            task_list.append(task)
        for i in as_completed(task_list):
            result.append(i.result())
        return result

    def get_images(self, data, path, img_url, prefix=""):
        self.start_thread(data, self.__get_images, path, img_url, prefix)

    def __get_images(self, item, path, img_url, prefix):
        page_resource = self.get_page_resource(prefix + item[img_url])
        with open("static/images/{path}/{id}.jpg".format(path=path, id=item['id']), "wb") as f:
            try:
                page_resource = page_resource.encode("utf-8")
            except Exception as e:
                debug(e)
            f.write(page_resource)
            f.close()
            update_data = {
                "status": 1
            }
            condition = ["id={id}".format(id=item['id'])]
            self.__update_data(update_data, "list", condition)

    @classmethod
    def get_page_resource(cls, url):
        data = curl_data(url, open_virtual_ip=True)
        return data

    def __update_data(self, update_data, table, condition):
        update_arr = {
            "table": table,
            "set": update_data,
            "condition": condition
        }
        lock.acquire()
        self.db.update(update_arr, is_close_db=False)
        lock.release()

    def get_data(self):
        data = self.db.select({
            "table": "list",
            "columns": ["id", "img_url", "img_url_large"],
            "condition": ["status=0"]
        }, is_close_db=False)
        return data
