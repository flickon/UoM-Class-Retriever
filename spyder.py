import requests
import bs4
from bs4 import BeautifulSoup

"""
Using OOP trying to achieve multiprocessing work
"""
class Spyder():

    def __init__(self, code, year, semester, series, start, end):
        self.code = code.upper()
        self.year = year
        self.semester = semester
        self.series = series
        self.start = str(start)
        self.end = str(end)
        self.url = 'https://sws.unimelb.edu.au/' + year + '/Reports/List.aspx'
        self.r = None
    
    def setup_target(self):
        payload = dict()
        payload['objects'] = self.code
        payload['weeks'] = "1-52"
        payload['days'] = self.start + "-" + self.end
        payload['periods'] = "1-56"
        payload['template'] = 'module_by_group_list'

        self.r = requests.get(self.url, params=payload, timeout=30)
        self.r.raise_for_status
        self.r.encoding = self.r.apparent_encoding
    
    def whole_class_list(self):
        res = []
        soup = BeautifulSoup(self.r.text, 'html.parser')
        trs = soup('table')[self.semester-1]
        trs = trs('tr')

        for i in range(1,len(trs)-1):
            tds = trs[i].find_all('td')
            res.append([tds[1].string, tds[2].string, tds[3].string, 
                        tds[4].string, tds[5].string, tds[7].string])

        return res

    def printer(self, classes):
        output = "{:3}\t{:3}\t{:3}\t{:3}\t{:3}\t{:3}\t\n\n".format("code", self.code, "year",self.year, "semester", self.semester)
        tplt = "{:^10}\t{:10}\t{:10}\t{:^10}\t{:10}\t{:10}\n"
        title = tplt.format('Class type', 'Date', 'Start', 'End', 'Duration', 'Place')
        output += title + "-"*150 + '\n'

        for i in range(len(classes)):
            s = classes[i]
            temp = tplt.format(s[0], s[1], s[2], s[3], s[4], s[5])
            output += temp + "-"*145 + '\n'
        
        return output
    
    def get(self):
        self.setup_target()
        print(self.printer(self.whole_class_list()))

    
        