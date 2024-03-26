#!/usr/bin/env python3
"""
a Python function that returns the list of school having a specific topi
"""


import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    a Python function that returns the list of school having a specific topi
    """
    return mongo_collection.find({"topics": topic})
