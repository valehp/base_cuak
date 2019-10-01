from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

usuario = Blueprint('usuario', __name__)

@usuario.route('/crear', methods=['POST',])
def create():
	if request.method == "POST":
		content = request.get_json()
		return get_model().crear_usuario(content)

@usuario.route('/obtener/<id>', methods=['GET',])
def get(id):
	return get_model().get_usuario(id)

@usuario.route('/best_launch/<username>', methods=["GET",])
def best_launch(username):
	return get_model().get_best_launch(username)

