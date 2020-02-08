#!/bin/python3

from lib import *
import sys
import logging
import os

logging.basicConfig(filename='logs/address-spider.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
cache_file_url = "cache/address.temp"

sites = [
    ('https://etherscan.io/contractsVerified/1?ps=100', 'etherscan'),
    ('https://ropsten.etherscan.io/contractsVerified/1?ps=100', 'ropsten_etherscan'),
    ('https://kovan.etherscan.io/contractsVerified/1?ps=100', 'kovan_etherscan'),
    ('https://rinkeby.etherscan.io/contractsVerified/1?ps=100',
     'rinkeby_etherscan'), ('https://tobalaba.etherscan.com/contractsVerified/1?ps=100', 'tobalaba_etherscan')
]


def record_status(url, title, current, totals, success, error):
    with open(cache_file_url, "w") as f:
        f.write("{url},{title},{current},{totals},{success},{error}".format(
            url=url, title=title, current=current, totals=totals, success=success, error=error))


def remore_status():
    with open(cache_file_url, "w") as f:
        f.write("")

def read_index(status):
    index, isnew = 0, True
    if status:
        for url, path in sites:
            if path == status['title'] and status['url'] != "":
                isnew = False
                break
            elif path == status['title'] and status['url'] == "":
                index += 1
                break
            else:
                index += 1
        if index == len(sites):
            index = 0
    return index, isnew


class SPIDER:

    def __init__(self, start_url='https://etherscan.io/contractsVerified/1?ps=100', path=None, status=None):
        self.urlmanage = URLMAN()
        self.urlload = URLLOAD()
        self.urlparse = RESPARSE()
        self.output = OUTPUT(path=path, file="address.txt", mode="a+", status=status)
        self.spider_name = path
        self.run(url=start_url, title=path, status=status)

    def run(self, url, title, status=None):
        cache_next_url = ""
        if status:
            url = status['url']
        self.urlmanage.seturl(url)
        totals, total, success, error = 0, 0, 0, 0
        if status:
            totals = status['totals']
            total = status['total']
            success = status['success']
            error = status['error']
        else:
            totals = self.urlparse.parse_list_page_count(
                self.urlload.dorequest(url))
        while self.urlmanage.has_new_url():
            url = self.urlmanage.get_newurl()
            if url == None:
                break
            if status:
                title = status['title']
            content = self.urlload.dorequest(url)
            if content:
                data, next_url = self.urlparse.parselist(content, url)
                cache_next_url = "" if next_url == url else next_url
                self.output.write_datas(data)
                self.urlmanage.seturl(next_url)
                success += 1
            else:
                error += 1
                logging.info(url + " - spider wrong : " + str(content))
            total += 1
            sys.stdout.write(process_bar_text(
                self.spider_name, total, totals, success, error))
            record_status(url=cache_next_url, title=title, current=total,
                          totals=totals, success=success, error=error)
        sys.stdout.flush()


def main(status=None):
    index, isnew = read_index(status)
    # change
    _sites = sites[index:1]
    for url, path in _sites:
        if isnew:
            spider = SPIDER(start_url=url, path=path, status=None)
            if path == _sites[-1][1]:
                remore_status()
        else:
            spider = SPIDER(start_url=status["url"], path=path, status=status)
            isnew=True
            status = None


def init():
    try:
        status = {}
        with open(cache_file_url, "r") as f:
            data = f.readlines()
            data_list = data[0].strip().split(',')
            status['url'] = data_list[0]
            status['title'] = data_list[1]
            status['total'] = int(data_list[2])
            status['totals'] = int(data_list[3])
            status['success'] = int(data_list[4])
            status['error'] = int(data_list[5])
        return status
    except Exception as e:
        return None


if __name__ == '__main__':
    main(init())
