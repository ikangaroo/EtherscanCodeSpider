#!/bin/python3

from lib import *
import os
import sys
import logging

logging.basicConfig(filename='logs/code-spider.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
cache_file_url = "cache/code.temp"
code_sites = [
    'etherscan'
]


def record_status(current, totals, success, error):
    with open(cache_file_url, "w") as f:
        f.write("{current},{totals},{success},{error}".format(
            current=current, totals=totals, success=success, error=error))


def remore_status():
    with open(cache_file_url, "w") as f:
        f.write("")


def read_index(status):
    index, url = 0, ""
    if status:
        for path in code_sites:
            if path == status['title'] and status['url'] != "":
                url = status['url']
                break
            elif path == status['title'] and status['url'] == "":
                index += 1
                break
            else:
                index += 1
        if index == len(code_sites) and url == "":
            index = 0
    return index, url


def read_url_index(lines, url):
    for index in range(0, len(lines)):
        if url == lines[index]:
            return index
    return 0


class SPIDER(SPIDER_BASE):

    def run(self, address, Label, DateVerified):
        try:
            content = self.urlload.dorequest(address)
            if content:
                Contract_Source_Code, Contract_ABI, Contract_Creation_Code_16, Contract_Creation_Opcode = self.urlparse.parsecode(
                    content, address)
                self.output.write_file(str(DateVerified) + '.json')
                self.output.write_code(Contract_Source_Code, Contract_ABI, Contract_Creation_Code_16,
                                       Contract_Creation_Opcode, Label, address.split('/')[-1])
                return True
            else:
                logging.info(address + " - spider wrong : " + content)
        except Exception as e:
            logging.info(address + " - spider wrong : " + str(e))


def run(path=None, file='Ponzi_label.csv'):
    full_path = file if path == None else (
        os.getcwd() + '/data/' + path + "/" + file)
    try:
        lines = []
        file_handler = open(full_path, mode="r")
        lines = file_handler.readlines()
        file_handler.close()    

        if lines == [] or lines == None:
            logging.info("read_file full_path: {full_path} spider_wrong: {msg}".format(
                full_path=full_path, msg="file is empty!"))
            return

        spider = SPIDER(path=path, mode="a+")
        totals, total, succeed, error = 0, 0, 0, 0
        totals = len(lines)

        name = 1
        for line in lines:
            line = line.split(',')
            if total % 1000 == 0:
                name = name + 1
            ans = spider.run("https://etherscan.io/address" + os.sep + line[0], line[1].split(), name)
            if ans:
                succeed += 1
            else:
                error += 1
            total += 1

        record_status(current=total, totals=totals, success=succeed, error=error)
        sys.stdout.flush()
        pass
    except Exception as e:
        raise e
        logging.info("open_file_status:error full_path: {full_path} spider_wrong: {msg}".format(
            full_path=full_path, msg=str(e)))
        pass
    else:
        logging.info("open_file_status:succeed full_path: {full_path}".format(
            full_path=full_path))
        pass


def main():
    run(path='etherscan')
    # _code_sites = code_sites[:]
    # for site in _code_sites:
    #     run(path=site)


if __name__ == '__main__':
    main()
