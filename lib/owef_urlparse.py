#!/bin/python3
from lxml import etree
from urllib.parse import urljoin
from .owef_convert import *
import requests
import json


class RESPARSE:

    def parse(self):
        self.html = etree.HTML(self.content)

    def run(self, res, url=None):
        self.content = res
        self.url = url
        self.parse()

    def parselist(self, res, url):
        self.run(res, url)
        try:
            addresss = self.html.xpath("//table/tbody/tr")
            uri1 = self.html.xpath('//*[@id="transfers"]/div[1]/nav/ul/li[4]/a/@href')
            uri2 = self.html.xpath("//div[@class='profile container']/div[4]/div[2]/p/a[3]/@href")
            if uri1 == [] and uri2 == []:
                next_url = url
            else:
                next_url = urljoin(url, uri1[0]) if len(uri1)==1 else urljoin(url, uri2[0])
            code_urls = []
            if(len(addresss)):
                for address in addresss:
                    _xml_url = address.xpath("td/a/@href")
                    _xml_contractname = address.xpath('td[2]/text()')
                    _xml_dateVerified = address.xpath('td[8]/text()')# 7->8 changed by zyx
                    _url = urljoin(url, _xml_url[0]) if len(
                        _xml_url) > 0 else ""
                    _ContractName = _xml_contractname[0] if len(
                        _xml_contractname) > 0 else ""
                    _DateVerified = Date2path(_xml_dateVerified[0]) if len(
                        _xml_dateVerified) > 0 else ""
                    code_urls.append(_url + ',' + _ContractName +
                                     ',' + _DateVerified + '\n')
            return (code_urls, next_url)
        except Exception as e:
            print("ERROR: %s\t\tdetail:%s" % (url, e))
            # set current url to a file, when restart set url to it

    def parsecode(self, res, url):
        self.run(res, url)
        _pres = self.html.xpath("//pre")
        _CSCO = None
        _CSC = None
        _CCC = None
        if len(_pres) >= 2:
            _CSCO = _pres[0].xpath("text()")
            _CSC = _pres[1].xpath("text()")
            _CCC = _pres[2].xpath("div/text()")
        Contract_Source_Code, Contract_ABI, Contract_Creation_Code_16 = "", "", ""
        if _CSCO:
            Contract_Source_Code_origin = _CSCO[0]
            Contract_Source_Code = Code_rm_black(Contract_Source_Code_origin)
        if _CSC:
            Contract_ABI = _CSC[0]
        if _CCC:
            Contract_Creation_Code_16 = _CCC[0] if "bzzr" not in _CCC[0] else ""
            _ = self.load_opcode()
            Contract_Creation_Opcode = "" if "Unable to decode" == _ else _
        return (Contract_Source_Code, Contract_ABI, Contract_Creation_Code_16, Contract_Creation_Opcode)

    def parse_list_page_count(self, res):
        self.run(res)
        _counts_old = self.html.xpath(
            "//div[@class='profile container']/div[2]/div[2]/p/span/b[2]/text()")
        _counts_new = self.html.xpath(
            '//*[@id="transfers"]/div[1]/nav/ul/li[3]/span/strong[2]/text()')


        counts = _counts_new[0] if len(_counts_new) == 1 else _counts_old[0]
        return int(counts)

    def load_opcode(self):
        address = self.url.split('/')[2]
        api_url = "https://etherscan.io/api?module=opcode&action=getopcode&address={addr}".format(
            addr=address)
        req = requests.get(api_url)
        ans = json.loads(req.text)
        return ans['result'].replace('<br>', "\r\n")
