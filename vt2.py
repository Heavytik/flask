# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, make_response

from flask_wtf_polyglot import PolyglotForm #tämä tuottaa xml-yhteensopivia lomakekenttiä
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, widgets, SelectMultipleField, ValidationError, SubmitField

import os
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['POST', 'GET'])
def test():
    fields = {"x": "", "pelaaja1": "", "pelaaja2": ""}
    errors = dict(fields)  # tekee kopion samoilla avaimilla

    boardSize = 8

    if request.method == 'POST':  # varmistetaan, että lomake on lähetetty
        for k in errors:
            try:
                fields[k] = request.form[k]
            except KeyError:
                errors[k] = "!"
        try:
            boardSize = int(fields["size"])
        except:
            boardSize = 8

    class GameField(PolyglotForm):
        x = IntegerField('Laudan koko',
                            validators=[validators.InputRequired(),
                                        validators.NumberRange(min=8, max=16, message="Taulukon koon täytyy olla välillä 8 - 16")])
        pelaaja1 = StringField('Pelaaja 1',
                            validators=[validators.InputRequired(),
                                        validators.Length(min=2, message="Liian lyhyt nimi")])
        pelaaja2 = StringField('Pelaaja 2',
                            validators=[validators.InputRequired(),
                                        validators.Length(min=2, message="Liian lyhyt nimi")])
        submit = SubmitField('Lähetä!')

    form = GameField()
    if request.method == 'POST':
        form.validate()

    resp = make_response(render_template('view.xhtml', form=form, boardSize=boardSize))
    resp.headers['Conent-type'] = 'application/xhtml+xml;charset=UTF-8'
    return resp
