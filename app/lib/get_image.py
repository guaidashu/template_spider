"""
author songjie
"""
import threading

from tool_yy import debug, curl_data
from tool_yy.lib.db import DBConfig

from app.lib.common import CommonFunc

lock = threading.RLock()

GET_CONFIG = {
    "img_aim_path": "static/static/images/",
    "file_name": "",
    "is_record_status": True,
    "is_test": False,
    "img_prefix": "",
    "img_url_column": "img_url",
    "header": False
}


class GetImages(object):
    def __init__(self, **kwargs):
        self.img_aim_path = kwargs.setdefault("img_aim_path", GET_CONFIG['img_aim_path'])
        self.file_name = kwargs.setdefault("file_name", GET_CONFIG['file_name'])
        self.is_record_status = kwargs.setdefault("is_record_status", GET_CONFIG['is_record_status'])
        self.is_test = kwargs.setdefault("is_test", GET_CONFIG['is_test'])
        self.img_prefix = kwargs.setdefault("img_prefix", GET_CONFIG['img_prefix'])
        self.img_url_column = kwargs.setdefault("img_url_column", GET_CONFIG['img_url_column'])
        self.header = kwargs.setdefault("header", GET_CONFIG['header'])
        self.common = CommonFunc()
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        self.get_images(data)

    def get_images(self, data):
        self.common.start_thread(data, self.__get_images)

    def __get_images(self, item):
        page_resource = self.get_page_resource(self.img_prefix + item[self.img_url_column])
        with open(self.img_aim_path, "wb") as f:
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
