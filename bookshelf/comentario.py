from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

comentario = Blueprint('comentario', __name__)

@comentario.route('/crear', methods=["POST",])
def create():
	if request.method == "POST":
		content = request.get_json()
		return get_model().create_comentario()

@comentario.route('/obtener/<id>', methods=["GET",])
def get(id):
	return get_model().get_comentario(id)