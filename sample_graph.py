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

        # 出来高
        volume_text = ''
        max_volume = 0
        for sp in stockpricess:
            if max_volume < sp['volume']:
                max_volume = sp['volume']
        for sp in stockpricess:
            volume_text += str(sp['volume']*100/max_volume) + ','
        volume_text = volume_text[:-1]
    
        # 株価
        close_text = ''
        max_close = 0
        for sp in stockpricess:
            if max_close < sp['adj_close']:
                max_close = sp['adj_close']
        for sp in stockpricess:
            close_text += str(sp['adj_close']*100/max_close) + ','
        close_text = close_text[:-1]
                    
        html = '<html><body>'
        html += '''<img src="http://chart.apis.google.com/chart?cht=lc
&amp;chs=700x300
&amp;chg=20,50,1,5
&amp;chxt=x,y
&amp;chxl=1:|0|%d|%d
&amp;chd=t:%s|%s
&amp;chco=FF9904,990FFf" />
'''%(max_volume/2, max_volume, volume_text, close_text)
                
        html += '</body></html>'
        print html
        
        f = open('sample_graph.html', 'w')
        f.write(html)
        f.close()
    except kabu.CodeError, e:
        print e
