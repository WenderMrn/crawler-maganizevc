#!/usr/bin/python

import json


class Product(json.JSONEncoder):
    name: str
    price: float
    colors: str
    img: str
    page_url: str
    shipping: str

    def __init__(self, name="", price=0, colors="", img="", page_url="", shipping=""):
        self.name = name
        self.price = price
        self.colors = colors
        self.img = img
        self.page_url = page_url
        self.shipping = shipping

    def default(self, o):
        return o.__dict__

    def __str__(self):
        return self.toJson()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
