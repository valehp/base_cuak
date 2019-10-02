from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

fila = Blueprint('fila', __name__)

@fila.route('/crear', methods=["POST",])
def create():
	if request.method == "POST":
		content = request.get_json()
		return get_model().create_fila()

@fila.route('/mean_value/<fecha_hora>', methods=["GET",])
def like(fecha_hora):
	return get_model().get_mean_value(fecha_hora)

@fila.route('/obtener/<id>', methods=["GET",])
def get(id):
	return get_model().get_fila(id)