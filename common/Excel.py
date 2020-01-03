# -*- coding: UTF-8 -*-

import os, xlrd
from xlutils.copy import copy


class Reader:
    def __init__(self):
        """
        用来读取excel文件内容
        """
        # 整个excel工作簿缓存
        self.workbook = None
        # 当前工作的sheet
        self.sheet = None
        # 当前sheet的行数
        self.rows = 0
        # 当前读取到的行数
        self.r = 0

    def open_excel(self, srcfile):
        """
        打开excel
        :param srcfile: 要打开的文件地址
        :return:
        """
        # 如果打开的文件不存在,就报错
        if not os.path.isfile(srcfile):
            print("错误:%s不存在" % srcfile)
            return
        # 设置读取excel使用utf8编码
        xlrd.Book.encoding = "utf8"
        # 读取excel内容到缓存workbook
        self.workbook = xlrd.open_workbook(filename=srcfile)
        # 选取第一个sheet页面
        self.sheet = self.workbook.sheet_by_index(0)
        # 设置rows为当前sheet的行数
        self.rows = self.sheet.nrows
        # 设置默认读取为第一行
        self.r = 0
        return

    def get_sheets(self):
        """
        获取sheet页面
        :return:
        """
        # 获取所有sheet的名字,并返回一个列表
        sheets = self.workbook.sheet_names()
        print(sheets)
        return sheets

    def set_sheet(self, name):
        """
        通过sheet名字,切换sheet页面
        :param name:
        :return:
        """
        self.sheet = self.workbook.sheet_by_name(name)
        self.rows = self.sheet.nrows
        self.r = 0
        return

    def readline(self):
        """
        逐行读取
        :return:
        """
        row1 = None
        # 如果当前还没有到最后一行,则往下读取一行
        if self.r < self.rows:
            # 读取第r行的内容
            row = self.sheet.row_values(self.r)
            # 设置下一次读取r的下一行
            self.r = self.r + 1
            # 辅助遍历行里面的列
            i = 0
            row1 = row
            for strs in row:
                row1[i] = str(strs)
                i = i + 1
        return row1


class Writer:
    """
    用来复制写入excel文件
    """

    def __init__(self):
        # 读取需要复制的excel
        self.workbook = None
        # 拷贝的工作空间
        self.wb = None
        # 当前工作的sheet页
        self.sheet = None
        # 记录生成的文件,用来保存
        self.df = None
        # 记录写入的行
        self.row = 0
        # 记录写入的列
        self.clo = 0

    def copy_open(self, srcfile, dstfile):
        """
        复制并打开excel
        :param srcfile: 要复制的文档
        :param dstfile: 要新建的文档
        :return:
        """
        # 判断要复制的文档是否存在,
        if not os.path.isfile(srcfile):
            print(srcfile + "不存在")
            return
        # 判断要新建的文档是否已经存在,存在则提示
        if os.path.isfile(dstfile):
            print("错误:" + dstfile + "文件已经存在!")

        # 记录要保存的文件
        self.df = dstfile
        # 读取excel到缓存
        # formatting_info带格式的复制
        self.workbook = xlrd.open_workbook(filename=srcfile, formatting_info=True)
        # 拷贝,也在内存里面
        self.wb = copy(self.workbook)
        # 默认使用第一个sheet
        # sheet = self.wb.get_sheet('Sheet1')
        return

    def get_sheet(self):
        """
        获取所有sheet的名字,并返回一个列表
        :return: 所有sheet名字的列表
        """
        sheets = self.workbook.sheet_names()
        print(sheets)
        return sheets

    def set_sheet(self, name):
        """
        通过sheet名字,切换sheet页面
        :param name:
        :return:
        """
        self.sheet = self.wb.get_sheet(name)
        return

    def write(self, r, c, value):
        """
        写入指定单元格,保留原格式
        :param r:
        :param c:
        :param value:
        :return:
        """
        # 获取要写入的单元格
        def _getCell(sheet, r, c):
            # 获取行
            row = sheet._Worksheet__rows.get(r)
            if not row:
                return None
            # 获取单元格
            cell = row._Row__cells.get(c)
            return cell

        # 获取要写入的单元格
        cell = _getCell(self.sheet, r, c)
        # 写入值
        self.sheet.write(r, c, value)
        if cell:
            # 获取要写入的单元格
            ncell = _getCell(self.sheet, r, c)
            if ncell:
                # 设置写入后格式和写入前一样
                ncell.xf_idx = cell.xf_idx
        return

    def save_close(self):
        """
        保存复制后的文件到硬盘
        :return:
        """
        self.wb.save(self.df)
        return


# 调试
if __name__ == '__main__':
    reader = Reader()
    reader.open_excel('../lib/cases/HTTP接口用例.xls')
    sheetname = reader.get_sheets()
    for sheet in sheetname:
        # 设置当前读取的sheet页面
        reader.set_sheet(sheet)
        for i in range(reader.rows):
            print(reader.readline())

    writer = Writer()
    writer.copy_open('../lib/cases/HTTP接口用例.xls', '../lib/results/result-HTTP接口用例.xls')
    sheetname = writer.get_sheet()
    writer.set_sheet(sheetname[0])
    writer.write(1, 1, 'yaocl')
    writer.save_close()


# excel中写入纯数字时,在前面加一个',变为字符串,就不会变为.0
