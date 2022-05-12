#!/usr/bin/python

import fire

from magazinevc.crawler import CrawlerParceiroMagalu


class Main(object):
    """A simple crawler to https://www.magazinevoce.com.br/"""

    def search(self, **kwargs):
        CrawlerParceiroMagalu(**kwargs).search()


if __name__ == '__main__':
    fire.Fire(Main)
