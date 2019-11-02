from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

fila = Blueprint('fila', __name__)

@fila.route('/crear', methods=["POST",])
def create():
	if request.method == "POST":
		content = request.get_json()
		return get_model().create_fila()

@fila.route('/mean_value/type', methods=["GET",])
def like(type):
	return get_model().get_mean_value(type)

@fila.route('/obtener/<id>', methods=["GET",])
def get(id):
	return get_model().get_fila(id)

@fila.route('/todos', methods=["GET",])
def all():
	return get_model().get_all_fila()
