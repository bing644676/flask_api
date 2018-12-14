#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import xlsxwriter
from xlrd import open_workbook


def read_excel_file(excel_file):
    workbook = open_workbook(excel_file)
    book_sheet = workbook.sheet_by_name('Sheet1')
    items = []
    for row in range(0, book_sheet.nrows):
        res = []
        for col in range(book_sheet.ncols):
            cel = book_sheet.cell(row, col)
            val = cel.value
            ctype = cel.ctype
            # 如果是整形
            if ctype == 2 and val % 1 == 0:
                val = int(val)
            res.append(val)
        items.append(res)
    return items


def deal_row(rows):
    result = {}
    rows.pop(0)  # 剔除第一行
    for row in rows:
        key = row[0]
        value = row[1]
        result[key] = value
    return result


def deal_line(rows):
    data_list = []
    length = len(rows)
    if length <= 1:
        print("the csvfile invaild")
        sys.exit(-1)
    for i in range(1, length):
        data_dict = {}
        for j in range(len(rows[0])):
            key = rows[0][j]
            value = rows[i][j]
            if not isinstance(value, int) and len(value) > 0 and value[0] in ['[', '{']:
                value = eval(value)
            data_dict[key] = value
        data_list.append(data_dict)

    return data_list


def write_to_excel(out_file, values):
    work_book = xlsxwriter.Workbook(out_file)
    work_sheet = work_book.add_worksheet('Sheet1')
    work_sheet.set_column('A:A', 20)
    work_sheet.write(values)
    work_book.close()


if __name__ == '__main__':
    item = read_excel_file('img_material.xlsx')
    data = deal_line(item)
    print(data)
