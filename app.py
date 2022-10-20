#!/usr/bin/python
#-*- coding: utf-8 -*-
#Autor: Luis Angel Ramirez Mendoza

from flask import Flask, render_template, request, Response, redirect, send_file, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'Tu Archivo.json'
credentials = service_account.Credentials.from_service_account_file(filename=SERVICE_ACCOUNT_FILE)

service_sheets = build('sheets', 'v4', credentials=credentials)
#print(service_sheets)

GOOGLE_SHEETS_ID = 'TU ID'

worksheet_name = 'Nombre Worksheet!'

global cont
cont = 4


app = Flask(__name__)


@app.route('/')
def route():
	return render_template("index.html")


@app.route('/envia', methods=['GET', 'POST'])
def envia():
	global cont
	if request.method == 'POST':
		Fecha = request.form['fecha']
		Valor = request.form['valor']
		Descripcion = request.form['descripcion']
		Categoria = request.form['categoria']		
		cont = cont + 1
		cell_range_insert = ('B' + str(cont) + ':' + 'E' + str(cont))

		values = ((Fecha , Valor, Descripcion, Categoria),)
		value_range_body = {
			'majorDimension': 'ROWS',
			'values': values
		}

		service_sheets.spreadsheets().values().update(
			spreadsheetId=GOOGLE_SHEETS_ID,
			valueInputOption='USER_ENTERED',
			range=worksheet_name + cell_range_insert, 
			body = value_range_body).execute()

		return render_template("index.html")


if __name__ == '__main__':
	app.run(host='localhost')