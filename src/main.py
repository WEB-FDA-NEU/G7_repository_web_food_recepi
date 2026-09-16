#!/bin/env python
import sqlite3

from fastapi import FastAPI, responses

conn = sqlite3.connect("cache/data")
app = FastAPI()


@app.get("/", response_class=responses.HTMLResponse)
def _():
    return open("screens/index.html", "r").read()


@app.get("/style.css", response_class=responses.HTMLResponse)
def _():
    return open("screens/style.css", "r").read()


@app.get("/admin", response_class=responses.HTMLResponse)
def _():
    conn
    return open("screens/admin.html", "r").read()


#
# @app.get("/hello/{name}")
# def _(name: str):
#     return {"message": f"{name[::-1]}Hello"}
#
#
# @app.get("/add")
# def _(a="0", b="0"):
#     if a.isdigit() and b.isdigit():
#         return {"message": f"{a + b}Hello"}
#     else:
#         return {"message": "the server have crash trying to process ur mom"}
#
#
# async def f():
#     return "Asdf"
#
#
# print(f())
