from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

usuario = Blueprint('usuario', __name__)

@usuario.route('/crear', methods=['POST',])
def create():
	if request.method == "POST":
		content = request.get_json()
		return get_model().create_usuario(content)

@usuario.route('/obtener/<username>', methods=['GET',])
def get(username):
	return get_model().get_usuario(username)

@usuario.route('/best_launch/<username>', methods=["GET",])
def best_launch(username):
	return get_model().get_best_launch(username)

@usuario.route('/todoss', methods=["GET", ])
def all_usuario():
	return get_model().get_all_usuario()
