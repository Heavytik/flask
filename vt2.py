# -*- coding: utf-8 -*-

from flask import Flask, request, render_template

app = Flask(__name__)

counter = 0


@app.route('/')
def test():
    global counter

    try:
        count = int(request.args.get("count", 4))
    except:
        count = 0

    counter = counter + count

    return render_template('view.html', counter=counter)
