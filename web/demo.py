#!/bin/python
# -*- coding:utf-8 -*-

from flask import Flask

app = Flask('test')


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(port=9990)
