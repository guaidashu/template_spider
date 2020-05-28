"""
author songjie
"""
from concurrent.futures import ThreadPoolExecutor, as_completed

from googletrans import Translator
from tool_yy import debug


class CommonFunc(object):
    def __init__(self):
        self.translator = Translator(service_urls=['translate.google.cn'])

    def translate(self, content, dest="zh", src="en"):
        """
        This function can translate src source to dest source
        :param content:
        :param dest:
        :param src:
        :return:
        """
        try:
            data = self.translator.translate(content, dest, src).text
        except Exception as e:
            data = ""
            debug("翻译出错，错误信息：{error}".format(error=e))
        return data
