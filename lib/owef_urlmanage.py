#! /bin/python3


class URLMAN:

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        return self.get_new_url_count() > 0

    def get_newurl(self):
        if self.has_new_url():
            url = self.geturl()
            if url:
                self.old_urls.add(url)
                return url

    def geturl(self):
        if self.has_new_url():
            return self.new_urls.pop()

    def seturl(self, url):
        if self.has_url(url):
            return
        else:
            self.new_urls.add(url)

    def seturls(self, urls):
        for url in urls:
            self.seturls(url)

    def get_new_url_count(self):
        return len(self.new_urls)

    def get_old_url_count(self):
        return len(self.old_urls)

    def has_url(self, url):
        return url in self.new_urls or url in self.old_urls
