"""
author songjie
"""
from concurrent.futures import ThreadPoolExecutor, as_completed


class CommonFunc(object):
    def __init__(self):
        pass

    @staticmethod
    def start_thread(data, fun, max_worker=15, **kwargs):
        """
        This function can start a thread pool
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
            break
        for i in as_completed(task_list):
            result.append(i.result())
        return result
