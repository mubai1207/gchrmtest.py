#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'RaoPQ'

import jsonpath


def getJson(json_data, json_key):
    if isinstance(json_data, dict):
        return jsonpath.jsonpath(json_data, "$..%s" % json_key)
    else:
        print("json_data is not dict")
