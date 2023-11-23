import re
import requests
from bs4 import BeautifulSoup


class Indicator(object):
    def __init__(self, close, rate):
        self.close = close
        self.rate = rate


class IndexScraper(object):
    def __init__(self):
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

    def _jpx_futures(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        columns = [tr.find_all("td") for tr in soup.find(
            "table").find_all("tr") if tr.find_all("td")][0]
        close_list = re.search(
            r"([0-9,.]+)\((.+)\)\((.+)\)", columns[5].text.strip())
        rate_list = re.search(r"([0-9,.]+)\((.+)\)", columns[6].text.strip())
        return Indicator(close_list.groups()[0], rate_list.groups()[1])

    def nikkei225(self):
        return self._jpx_futures("https://port.jpx.co.jp/jpx/template/quote.cgi?F=tmp/popchart&QCODE=101.555/O")

    def topix(self):
        return self._jpx_futures("https://port.jpx.co.jp/jpx/template/quote.cgi?F=tmp/popchart&QCODE=151.555/O")

    def growth250(self):
        return self._jpx_futures("https://port.jpx.co.jp/jpx/template/quote.cgi?F=tmp/popchart&QCODE=154.555/O")


class IpokabuScraper(object):
    def __init__(self):
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
        self.baseurl = "https://ipokabu.net"

    def find_urls_by_ipoday(self, date):
        res = requests.get(f"{self.baseurl}/yotei/")
        soup = BeautifulSoup(res.content, "html.parser")
        codes = []
        # 最初のテーブル内の行を反復処理する
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                # 行内で上場日を含むセルを探す
                date_cell = row.find('td')
                if date_cell:
                    # 指定された日付と一致するか確認
                    if date in date_cell.text:
                        # 同じ行内で証券コードを含むセルを見つける
                        code_cell = row.find('td', class_='td_code2')
                        if code_cell:
                            codes.append(code_cell.text.strip())
        return {code: f"{self.baseurl}/ipo/{code}" for code in codes}
