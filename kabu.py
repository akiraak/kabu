#!/usr/bin/python
# -*- encoding:utf-8 -*-
import os
import datetime
import traceback
import lxml.html
import re
from urllib import urlencode, urlopen

baseUrl = 'http://table.yahoo.co.jp/t?'

class Error(Exception):
    pass

class CodeError(Error):
    def __init__(self, message):
        self.message = message

def getBrand(html):
    html_root = lxml.html.fromstring(html)
    xpath_text = u'//*[@class="yjXL"]'
    brand = html_root.xpath(xpath_text)
    if len(brand) > 0:
        return brand[0].text_content()
    return None

def getDataMonth(code, year, month, start_day, end_day, get_brand):
    if start_day == None:
        start_day = 1
    if end_day == None:
        work_year = year
        work_month = month+1
        if work_month > 12:
            work_year += 1
            work_month = 1
        end_day = (datetime.date(work_year, work_month, 1)-datetime.timedelta(days=1)).day
    
    query = {
        'c': year,
        'a': month,
        'b': start_day,
        'f': year,
        'd': month,
        'e': end_day,
        'g': 'd',
        's': code,
        'y': '0',
        'z': code,
        'x': 'sb',
    }
    url = baseUrl + urlencode(query)
    print url
    html = urlopen(url).read()
    #print html
    html=unicode(html, 'euc-jp', 'ignore')

    # 銘柄名の取得
    brand = None
    if get_brand:
        brand = getBrand(html)

    html_root = lxml.html.fromstring(html)
    th_tags = [u'日付',u'始値',u'高値',u'安値',u'終値',u'出来高']
    xpath_text = u'//table['
    for i in range(len(th_tags)):
        if i != 0:
            xpath_text += u' and '
        xpath_text += u'./tr/th[position()=%s]/small/text()="%s"'%(i+1, th_tags[i])
    xpath_text += u']/tr[position()!=1]'
    #print xpath_text
    kabu_trs = html_root.xpath(xpath_text)
    items = []
    return_tags=['year','month','day','open','high','low','close','volume','adj_close']
    for tr in reversed(kabu_trs):
        text = tr.text_content()
        r=re.search(u'(\d{4})年(\d{1,2})月(\d{1,2})日\s+(.+)\s+(.+)\s+(.+)\s+(.+)\s+(.+)\s+(.+)', text)
        try:
            items_val = {}
            for i in range(len(r.groups())):
                if i < len(return_tags):
                    items_val[return_tags[i]] = int(r.group(i+1).replace(',', ''))
            items.append(items_val)
        except Exception, e:
            try:
                r=re.search(u'(\d{4})年(\d{1,2})月(\d{1,2})日\s+(.*)', text)
                for i in range(3):
                    if i < len(return_tags):
                        items_val[return_tags[i]] = int(r.group(i+1).replace(',', ''))
                items_val['comment'] = r.group(4)
                items.append(items_val)
            except Exception, e:
                print traceback.format_exc()
                print e
            print traceback.format_exc()
            print e
    return brand, items

def getData(code, start_date, end_date):
    if start_date > end_date:
        raise
    
    brand = ''
    items = []
    
    loop = True
    is_brand = True
    get_start_year = start_date.year
    get_start_month = start_date.month
    get_start_day = start_date.day
    get_end_date = None
    if get_start_year == end_date.year and get_start_month == end_date.month:
        d_date = end_date.day
    while(loop):
        # 株情報の取得
        get_brand, get_items = getDataMonth(code, get_start_year, get_start_month, get_start_day, get_end_date, is_brand)
        # 銘柄は初回のみ取得
        if is_brand:
            # 銘柄名がない場合は銘柄コードが間違っている
            if not get_brand:
                raise CodeError(u'None kabu code')
            is_brand = False
            brand = get_brand
        # 株価をリストに追加
        items.extend(get_items)
        # 同一年月なら終了
        if get_start_year == end_date.year and get_start_month == end_date.month:
            loop = False
        else:
            # 次の年月日へ
            get_start_day = 1
            get_start_month += 1
            if get_start_month > 12:
                get_start_year += 1
                get_start_month = 1
            if get_start_year == end_date.year and get_start_month == end_date.month:
                get_end_date = end_date.day
            else:
                get_end_date = None
    
    return brand, items 
