# -*- coding: UTF-8 -*-
import requests, json


# 关键字封装
class HTTP:
    def __init__(self, writer):
        # session管理(不用每请求一次都加一次token)
        self.session = requests.session()
        # 基础的host地址
        self.url = ''
        # 解析结果
        self.result = None
        self.jsonres = None
        # 关联保存参数的字典
        self.relations = {}

        # 写入excel文件的Excel.Writer对象
        self.writer = writer
        # 记录当前写入的列
        self.row = 0

    def seturl(self, url):
        """
        设置基本url地址
        :param url:
        :return:
        """
        self.url = url
        self.__write_excel_res('PASS','设置成功:'+self.url)


    def post(self, path, params):
        """
        发送post请求
        :param path:请求的路径
        :param params:请求的参数
        :return:无
        """
        params = self.__get_relation(params)
        self.result = self.session.post(self.url + path, data=self.__get_data(params))
        try:
            self.jsonres = json.loads(self.result.text)
        except Exception as e:
            self.jsonres = None
        self.__write_excel_res('PASS', self.result.text)

    def addheader(self, key, value):
        """
        在session上面添加头
        :param key:头的键
        :param value:头的值
        :return:无
        """
        value = self.__get_relation(value)
        self.session.headers[key] = value
        self.__write_excel_res('PASS', '添加成功:'+ str(self.session.headers))

    def removeheader(self, key):
        """
        删除头里面的某一个键值对
        :param key:要删除的键
        :return:
        """
        try:
            self.session.headers.pop(key)
        except Exception as e:
            pass
        self.__write_excel_res('PASS', '删除成功:'+ str(self.session.headers))

    def __get_data(self, params):
        """
        将标准的url格式参数转换为字典
        :param params:url参数字符串
        :return:转换后的字典
        """
        if params is None or params == '':
            # 如果是空或者空字符串,都返回None
            return None
        else:
            params_dict = {}
            # 分隔url字符串的键值对
            list_params = params.split('&')
            # 遍历键值对
            for items in list_params:
                # 如果键值对里面有'=' ,那么我们就取等号左边为键,右边为值
                # 主要是支持值里面传'='
                if items.find('=') > 0:
                    params_dict[items[0: items.find('=')]] = items[items.find('=') + 1:]
                else:
                    # 如果没有'=',处理为键,值为None
                    params_dict[items] = None
        return params_dict

    # 关联的实现:1.先保存需要关联使用的数据
    #           2.使用,用一种约定来使用:在用例参数里面,如果出现{yourparam},那么我们在运行的时候,
    #           将它替换为你保存的字典里面yourparam这个键的值
    def savejson(self, key, param_name):
        """
        保存关联参数
        :param key:需要保存的json结果里面的键
        :param param_name:保存后参数的名字
        :return:无
        """
        try:
            self.relations[param_name] = self.jsonres[key]
            self.__write_excel_res('PASS', str(self.relations))
        except Exception as e:
            self.relations[param_name] = ''
            self.__write_excel_res('FAIL', str(self.relations))

    def __get_relation(self, params):
        """
        将参数里面用到的关联,替换为关联后的值
        :param params:关联前的参数
        :return:关联后的结果
        """
        if params == None or params == '':
            return ''
        else:
            # 遍历当前保存后的参数字典
            # 然后把参数里面凡是符合:{keys}这种形式的字符串都替换为relations这个字典里面这个键的值
            for key in self.relations:
                params = params.replace('{' + key + '}', self.relations[key])
        return params

    def assertequals(self, key, value):
        """
        判断json结果里面某个键的值是否和期望值value相等
        :param key:json的键
        :param value:期望值
        :return:是否相等
        """
        res = None
        try:
            res = str(self.jsonres[key])
        except Exception as e:
            pass
        # 关联
        value = self.__get_relation(value)
        if res == value:
            print('PASS')
            self.__write_excel_res('PASS',res)
            return True
        else:
            print('FAIL')
            self.__write_excel_res('FAIL', res)
            return False

    def __write_excel_res(self, status, msg):
        self.writer.write(self.row, 7, status)
        self.writer.write(self.row, 8, msg)
