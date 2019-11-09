from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

comida = Blueprint('comida', __name__)

@comida.route('/crear', methods=["POST",])
def create():
	if request.method == "POST":
		content = request.get_json()
		return get_model().create_comida(content)

@comida.route('/obtener/<id>', methods=["GET",])
def get(id):
	return get_model().get_comida(id)

@comida.route('/obtener/comida_del_dia', methods=["GET",])
def comidas():
	return get_model().get_comida_dia()

@comida.route('/obtener/junaeb', methods=["GET",])
def comidas2():
	return get_model().get_comida_junaeb()

@comida.route('/set_comida_dia/junaeb/<comida1>/<comida2>/<comida3>/<comida4>', methods=["PATCH",])
def set_comidas(comida1, comida2, comida3, comida4):
	return get_model().set_comida_junaeb(comida1, comida2, comida3, comida4)

@comida.route('/set_comida_dia/<comida1>/<comida2>/<comida3>/<comida4>', methods=["PATCH",])
def set_comidas2(comida1, comida2, comida3, comida4):
	return get_model().set_comida(comida1, comida2, comida3, comida4)

@comida.route('/mejor_comida/<n>', methods=["GET",])
def mejor(n):
	return get_model().get_best_comida(n)

@comida.route('/todos', methods=["GET", ])
def all():
	return get_model().get_all_comida()
