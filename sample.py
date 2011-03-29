# -*- encoding:utf-8 -*-
import datetime
import kabu

if __name__ == '__main__':
    start_date=datetime.date(2010, 4, 1)
    end_date=datetime.date(2011, 3, 31)
    code=9501 
    try:
        # 株価の取得
        brand_name, stockpricess = kabu.getData(code=code, start_date=start_date, end_date=end_date)

        # 株価の表示
        print u'銘柄名:' + brand_name
        for sp in stockpricess:
            try:
                print u'%d年%d月%d日 始値:%d 高値:%d 安値:%d 終値:%d 出来高:%s 調整後出来高:%s'%(sp['year'],sp['month'],sp['day'],sp['open'],sp['high'],sp['low'],sp['close'],sp['volume'],sp['adj_close'])
            except KeyError, e:
                print u'%d年%d月%d日 株分割等:%s'%(sp['year'],sp['month'],sp['day'],sp['comment'])
    except kabu.CodeError, e:
        print e
