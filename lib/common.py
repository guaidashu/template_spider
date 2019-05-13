"""
author songjie
"""
from concurrent.futures import ThreadPoolExecutor, as_completed

from googletrans import Translator

from tool.lib.function import debug


class CommonFunc(object):
    def __init__(self):
        self.translator = Translator(service_urls=['translate.google.cn'])

    @staticmethod
    def start_thread(data, fun, max_worker=15, is_test=False, **kwargs):
        """
        This function can start a thread pool
        :param is_test:
        :param max_worker:
        :param data:
        :param fun:
        :param kwargs:
        :return:
        """
        thread_pool = ThreadPoolExecutor(max_workers=max_worker)
        task_list = list()
        result = list()
        for item in data:
            task = thread_pool.submit(fun, item, **kwargs)
            task_list.append(task)
            if is_test:
                break
        for i in as_completed(task_list):
            result.append(i.result())
        return result

    def translate(self, content, dest="zh", src="en"):
        try:
            data = self.translator.translate(content, dest, src)
        except Exception as e:
            data = ""
            debug("翻译出错，错误信息：{error}".format(error=e))
        return data
