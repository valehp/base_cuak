from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

publicacion = Blueprint('publicacion', __name__)

@publicacion.route('/crear', methods=["POST",])
def create():
	if request.method == "POST":
		content = request.get_json()
		return get_model().create_publicacion()

@publicacion.route('/AddLike/<id>/<like>', methods=["GET",])
def like(id,like):
	return get_model().Like(id,like)

@publicacion.route('/obtener/<id>', methods=["GET",])
def get(id):
	return get_model().get_publicacion(id)