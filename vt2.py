# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, make_response

from flask_wtf_polyglot import PolyglotForm #tämä tuottaa xml-yhteensopivia lomakekenttiä
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, widgets, SelectMultipleField, ValidationError

import os
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['POST', 'GET'])
def test():
    fields = {"size": "", "name1": "", "name2": ""}
    errors = dict(fields)  # tekee kopion samoilla avaimilla
    if request.method == 'POST':  # varmistetaan, että lomake on lähetetty
        for k in errors:
            try:
                fields[k] = request.form[k]
            except KeyError:
                errors[k] = "!"

    class GameField(PolyglotForm):
        size = IntegerField('Laudan koko', validators=[validators.InputRequired(), validators.NumberRange(min=1, message="Liian pieni taulukko")])
        name1 = StringField('Pelaaja 1', validators=[validators.InputRequired(), validators.Length(min=2, message="Liian lyhyt nimi")])
        name2 = StringField('Pelaaja 2', validators=[validators.InputRequired(), validators.Length(min=2, message="Liian lyhyt nimi")])

    form = GameField()
    if request.method == 'POST':
        form.validate()

    resp = make_response(render_template('view.xhtml', form=form))
    resp.headers['Conent-type'] = 'application/xhtml+xml;charset=UTF-8'
    return resp
