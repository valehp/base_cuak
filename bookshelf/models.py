from flask import current_app
#from google.cloud import datastore
from google.appengine.ext import ndb

import datetime
import json


class Comida(ndb.Model):
	nombre_comida = ndb.StringProperty()
	puntaje_promedio = ndb.FloatProperty()
	comida_del_dia = ndb.BooleanProperty(default=False)

class Usuario(ndb.Model):
	nombre_usuario = ndb.StringProperty()
	password = ndb.StringProperty()
	correo = ndb.StringProperty()
	nombre_real = ndb.StringProperty()
	fecha_nacimiento = ndb.DateTimeProperty(auto_now_add=True)
	carrera = ndb.StringProperty()
	almuerzos_preferidos = ndb.StructuredProperty(Comida, repeated=True)
	quack_puntos = ndb.FloatProperty()

class Publicacion(ndb.Model):
	pubId = ndb.IntegerProperty()
	user = ndb.StructuredProperty(Usuario, repeated=True)
	nombre_comida = ndb.StructuredProperty(Comida)
	valoracion = ndb.FloatProperty()
	contenido = ndb.TextProperty()
	likes = ndb.IntegerProperty()
	dislikes = ndb.IntegerProperty()
	fecha_hora = ndb.DateTimeProperty(auto_now_add=True)

class Comentario(ndb.Model):
	comentId = ndb.IntegerProperty()
	user = ndb.StructuredProperty(Usuario, repeated=True)
	publicacion = ndb.StructuredProperty(Publicacion, repeated=False)
	comentario = ndb.TextProperty()
	valoracion = ndb.FloatProperty()
	fecha_hora = ndb.DateTimeProperty(auto_now_add=True)

class Fila(ndb.Model):
	filaId = ndb.IntegerProperty()
	user = ndb.StructuredProperty(User)
	fecha_hora = ndb.DateTimeProperty(auto_now_add=True)
	puntaje = ndb.FloatProperty()
	es_junaeb = ndb.BooleanProperty()
	es_normal = ndb.BooleanProperty()

def returnJson_usuario(user):
	r = dict()
	r['nombre_usuario'] = user.nombre_usuario
	r['correo'] = user.correo
	r["nombre_real"] = user.nombre_real
	r["fecha_nacimiento"] = user.fecha_nacimiento.strftime("%m/%d/%Y, %H:%M:%S")
	r["carrera"] = user.carrera
	r["almuerzos_preferidos"] = []
	r["quack_puntos"] = user.quack_puntos
	aux = []
	for almuerzo in user.almuerzos_preferidos:
		r["almuerzos_preferidos"] = returnJson_comida(almuerzo)
	return r

def returnJson_comida(comida):
	r = dict()
	r["nombre_comida"] = comida.nombre_comida
	r["puntaje_promedio"] = comida.puntaje_promedio
	r["comida_del_dia"] = comida.comida_del_dia
	return r

def returnJson_publicacion(pub):
	r = dict()
	r["pubId"] = pub.pubId
	r["user"] = returnJson_usuario(pub.user)
	r["nombre_comida"] = pub.nombre_comida
	r["valoracion"] = pub.valoracion
	r["contenido"] = pub.contenido
	r["likes"] = pub.likes
	r["dislikes"] = pub.dislikes
	r["fecha_hora"] = pub.fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
	return r

def returnJson_comentario(com):
	r = dict()
	r["comentId"] = com.comentId
	r["user"] = returnJson_usuario(com.user)
	r["publicacion"] = returnJson_publicacion(com.publicacion)
	r["comentario"] = com.comentario
	r["valoracion"] = com.valoracion
	r["fecha_hora"] = com.fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
	return r

def returnJson_fila(fila):
	r = dict()
	r["filaId"] = fila.filaId
	r["fecha_hora"] = fila.fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
	r["puntaje"] = fila.puntaje
	r["user"] = returnJson_usuario(fila.user)
	r["es_junaeb"] = fila.es_junaeb
	r["es_normal"] = fila.es_normal
	return r