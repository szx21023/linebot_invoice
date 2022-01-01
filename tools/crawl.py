import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self):
        self.url_this = 'https://invoice.etax.nat.gov.tw/'
        self.url_last = 'https://invoice.etax.nat.gov.tw/lastNumber.html'
        self.prize_d = dict()
        self.prize_d['this'] = self.get_prize_number(self.url_this)
        self.prize_d['last'] = self.get_prize_number(self.url_last)
        
    def get_prize_number(self, url):
        info = requests.get(url)
        info.encoding='utf-8' 
        soup = BeautifulSoup(info.text, "html.parser")
        date = ''.join([ch for ch in soup.find_all("a", class_="etw-on")[0].text if ch in '0123456789'])
        prize_number = soup.find("table", class_="etw-table-bgbox etw-tbig").find_all("p", class_="etw-tbiggest")
        return {'date': date, 'prize_nums': [p.text.replace('\n', '') for p in prize_number]}

    def matched_prize(self, date, predict_num):
        def matched_number(prize_num, predict_num):
            count = 0
            for i in range(len(prize_num)):
                if prize_num[::-1][i] != predict_num[::-1][i]:
                    break
                count += 1
            return count

        if date == self.prize_d['this']['date']:
            prize_nums = self.prize_d['this']['prize_nums']
        else:
            prize_nums = self.prize_d['last']['prize_nums']

        if prize_nums[0] == predict_num:
            return '特別獎'
        
        if prize_nums[1] == predict_num:
            return '特獎'

        max_count = 0
        for num in prize_nums[2:]:
            count = matched_number(num, predict_num)
            if max_count < count:
                max_count = count
                
        if max_count == 8:
            return '頭獎'
        
        elif max_count == 7:
            return '二獎'
        
        elif max_count == 6:
            return '三獎'
        
        elif max_count == 5:
            return '四獎'
        
        elif max_count == 4:
            return '五獎'

        elif max_count == 3:
            return '六獎'
        return '沒中獎'

def reward(date, predict_number):
    crawler = Crawler()
    if date == crawler.prize_d['this']['date']:
        return crawler.matched_prize(date, predict_number)

    elif date == crawler.prize_d['last']['date']:
        return crawler.matched_prize(date, predict_number)

    else:
        return '你的發票日期不在對獎範圍內！'