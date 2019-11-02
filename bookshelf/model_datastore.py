# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import current_app
#from google.cloud import datastore
from google.appengine.ext import ndb
#from .models import *

import datetime
import json


builtin_list = list

def init_app(app):
    pass

class Comida(ndb.Model):
	nombre_comida = ndb.StringProperty()
	puntaje_promedio = ndb.FloatProperty()
	comida_del_dia = ndb.BooleanProperty(default=False)

class Usuario(ndb.Model):
	nombre_usuario = ndb.StringProperty()
	password = ndb.StringProperty()
	correo = ndb.StringProperty()
	nombre_real = ndb.StringProperty()
	fecha_nacimiento = ndb.StringProperty()
	carrera = ndb.StringProperty()
	almuerzos_preferidos = ndb.StructuredProperty(Comida, repeated=False)
	quack_puntos = ndb.FloatProperty()

class Publicacion(ndb.Model):
	pubId = ndb.IntegerProperty()
	user = ndb.StructuredProperty(Usuario, repeated=False)
	nombre_comida = ndb.StructuredProperty(Comida)
	valoracion = ndb.FloatProperty()
	contenido = ndb.TextProperty()
	likes = ndb.IntegerProperty()
	dislikes = ndb.IntegerProperty()
	fecha_hora = ndb.DateTimeProperty(auto_now_add=True)

class Comentario(ndb.Model):
	comentId = ndb.IntegerProperty()
	user = ndb.StructuredProperty(Usuario, repeated=False)
	publicacion = ndb.StructuredProperty(Publicacion, repeated=False)
	comentario = ndb.TextProperty()
	valoracion = ndb.FloatProperty()
	fecha_hora = ndb.DateTimeProperty(auto_now_add=True)

class Fila(ndb.Model):
	filaId = ndb.IntegerProperty()
	user = ndb.StructuredProperty(Usuario)
	fecha_hora = ndb.DateTimeProperty(auto_now_add=True)
	puntaje = ndb.FloatProperty()
	es_junaeb = ndb.BooleanProperty()
	es_normal = ndb.BooleanProperty()

def returnJson_usuario(user):
	r = dict()
	r['nombre_usuario'] = user.nombre_usuario
	r['correo'] = user.correo
	r["nombre_real"] = user.nombre_real
	r["fecha_nacimiento"] = user.fecha_nacimiento
	r["carrera"] = user.carrera
	r["almuerzos_preferidos"] = []
	r["quack_puntos"] = user.quack_puntos
	r["password"] = user.password
	aux = []
	if user.almuerzos_preferidos:
		for almuerzo in user.almuerzos_preferidos:
			r["almuerzos_preferidos"] = returnJson_comida(almuerzo)
	return r

def returnJson_comida(comida):
	r = dict()
	r["id"] = comida.key.id()
	r["nombre_comida"] = comida.nombre_comida
	r["puntaje_promedio"] = comida.puntaje_promedio
	r["comida_del_dia"] = comida.comida_del_dia
	return r

def returnJson_publicacion(pub):
	r = dict()
	r["pubId"] = pub.pubId
	r["id"] = pub.key.id()
	r["user"] = returnJson_usuario(pub.user)
	r["nombre_comida"] = pub.nombre_comida
	r["valoracion"] = pub.valoracion
	r["contenido"] = pub.contenido
	r["likes"] = pub.likes
	r["dislikes"] = pub.dislikes
	r["fecha_hora"] = pub.fecha_hora.strftime("%m/%d/%Y,%H:%M:%S")
	return r

def returnJson_comentario(com):
	r = dict()
	r["comentId"] = com.comentId
	r["id"] = com.key.id()
	r["user"] = returnJson_usuario(com.user)
	r["publicacion"] = returnJson_publicacion(com.publicacion)
	r["comentario"] = com.comentario
	r["valoracion"] = com.valoracion
	r["fecha_hora"] = com.fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
	return r

def returnJson_fila(fila):
	r = dict()
	r["filaId"] = fila.filaId
	r["id"] = fila.key.id()
	r["fecha_hora"] = fila.fecha_hora.strftime("%m/%d/%Y, %H:%M:%S")
	r["puntaje"] = fila.puntaje
	r["user"] = returnJson_usuario(fila.user)
	r["es_junaeb"] = fila.es_junaeb
	r["es_normal"] = fila.es_normal
	return r

### METODOS DE USUARIO
def update_usuario(data, id=None):
	usuario = Usuario()
	usuario.nombre_usuario = str(data["nombre_usuario"])
	usuario.password = str(data["password"])
	usuario.correo = str(data["correo"])
	usuario.nombre_real = str(data["nombre_real"])
	usuario.carrera = str(data["carrera"])
	usuario.fecha_nacimiento = str(data["fecha_nacimiento"])
	usuario.quack_puntos = int(data["quack_puntos"])
	comidas = []
	if data["almuerzos_preferidos"]:
		for comida in data["almuerzos_preferidos"]:
			aux = Comida.query(Comida.nombre_comida == str(comida)).fetch()
			for c in aux:
				c.append(aux)
	if comidas: usuario.almuerzos_preferidos = comida
	usuario.put()
	return json.dumps(returnJson_usuario(usuario))

create_usuario = update_usuario

def get_best_launch(username):
	user = Usuario.query(Usuario.nombre_usuario == str(username)).fetch()[0]
	print user
	res = []
	if user.almuerzos_preferidos:
		for comida in user.almuerzos_preferidos:
			res.append(returnJson_comida(comida))
	return json.dumps(res)

def delete_usuario(username):
	user = Usuario.query(Usuario.nombre_usuario == username).fetch()[0]
	user.key.delete()
	return "Correct"
	
def get_usuario(username):
	return json.dumps(returnJson_usuario(Usuario.query(Usuario.nombre_usuario == username).fetch()[0]))
### LISTOS METODOS DE USUARIO

""" METODOS DE PUBLICACION """
def update_publicacion(data, id=None):
	pub = Publicacion()
	pub.pubId = int(data["pubId"])
	pub.user = returnJson_usuario(Usuario.query(Usuario.nombre_usuario == username).fetch()[0])
	pub.nombre_comida = returnJson_comida(Comida.query(Comida.nombre_comida == pub.nombre_comida).fetch()[0])
	pub.valoracion = float(data["valoracion"])
	pub.contenido = str(data["contenido"])
	pub.likes = str(data["likes"])
	pub.dislikes = str(data["dislikes"])
	pub.put()
	return json.dumps(pub)

create_publicacion = update_publicacion

def Like(pubId, like):
	pub = Publicacion.get_by_id(int(pubId))
	if like: pub.like += 1
	else: pub.dislikes += 1
	return json.dumps(returnJson_publicacion(pub))

def delete_publicacion(pubId):
	pub = Publicacion.get_by_id(int(pubId))
	pub.key.delete()
	return "Correct"

def get_publicacion(pubId):
	pub = Publicacion.get_by_id(int(pubId))
	return json.dumps(returnJson_publicacion(pub))

def get_all_publicacion():
	publicaciones = Publicacion.query().fetch()
	p = []
	if publicaciones:
		for publicacion in publicaciones:
			p.append(returnJson_publicacion(publicacion))
	return json.dumps(p)
""" FIN METODOS DE PUBLICACCION """

""" METODOS DE COMENTARIO """
def update_comentario(data, id=None):
	c = Comentario()
	c.comentId = int(data["comentId"])
	c.user = returnJson_usuario(Usuario.query(Usuario.nombre_usuario == str(data["nombre_usuario"])).fetch()[0])
	c.publicacion = returnJson_publicacion(Publicacion.query(Publicacion.get_by_id(int(data["publicacion"]))))
	c.comentario = str(data["comentario"])
	c.valoracion = float(data["valoracion"])
	return json.dumps(returnJson_comentario(c))

create_comentario = update_comentario

def delete_comentario(comentId):
	c = Comentario.get_by_id(int(comentId))
	c.key.delete()
	return "Correct"

def get_all_comentario():
	comentarios = Comentario.query().fetch()
	c = []
	if comentarios:
		for comentario in comentarios:
			c.append(returnJson_comentario(comentario))
	return json.dumps(c)

def get_comentario(comentId):
	return json.dumps(returnJson_comentario(Comentario.get_by_id(int(comentId))))
""" FIN METODOS COMENTARIO """

""" METODOS FILA """
def update_fila(data, id=None):
	fila = Fila()
	fila.filaId = int(data["filaId"])
	fila.user = returnJson_usuario(Usuario.query(Usuario.nombre_usuario == str(data["user"])).fetch()[0])
	fila.puntaje = float(data["puntaje"])
	fila.es_junaeb = bool(data["es_junaeb"])
	fila.es_normal = bool(data["es_normal"])
	fila.put()
	return json.dumps(returnJson_fila(fila))

create_fila = update_fila

def get_mean_value(tipo):
	# hacer busqueda por 1 hora antes
	h = datetime.timedelta(hours = 1)
	hoy = datetime.datetime.now()
	filas = Fila.query(ndb.AND(Fila.fecha_hora >= (hoy-h), Fila.fecha_hora <= hoy, Fila.es_normal == True)).fetch()
	
	if tipo == 1:
		filas = Fila.query(ndb.AND(Fila.fecha_hora >= (hoy-h), Fila.fecha_hora <= hoy, Fila.es_juaneb == True)).fetch()
	
	promedio = 0.0
	if filas:
		for fila in filas:
			promedio += fila.puntaje
		promedio /= len(filas)
		
	aux = dict()
	aux["value"] = promedio
	return json.dumps(aux)

def delete_fila(filaId):
	fila = Fila.get_by_id(int(filaId))
	fila.key.delete()
	return "Correct"

def get_all_fila():
	f = []
	filas = Fila.query().fetch()
	if filas:
		for fila in filas:
			f.append(returnJson_fila(fila))
	return json.dumps(f)

def get_fila(filaId):
	return json.dumps(returnJson_fila(Fila.query(Fila.filaId == int(filaId))).fetch())
""" FIN METODOS FILA """

""" METODOS COMIDA """
def update_comida(data, id=None):
	c = Comida()
	c.nombre_comida = str(data["nombre_comida"])
	c.puntaje_promedio = float(data["puntaje_promedio"])
	c.comida_del_dia = bool(data["comida_del_dia"])
	c.put()
	return json.dumps(returnJson_comida(c))

create_comida = update_comida

def get_comida_dia():
	comidas = []
	for comida in Comida.query(Comida.comida_del_dia == True).fetch():
		comidas.append(returnJson_comida(comida))
	return json.dumps(comidas)

def set_comida(comida1, comida2, comida3, comida4):
	comidas = []
	for comida in Comida.query().fetch():
		if comida.nombre_comida == comida1: 
			comida.comida_del_dia = True
			comidas.append(returnJson_comida(comida))
		elif comida.nombre_comida == comida2: 
			comida.comida_del_dia = True
			comidas.append(returnJson_comida(comida))
		elif comida.nombre_comida == comida3: 
			comida.comida_del_dia = True
			comidas.append(returnJson_comida(comida))
		elif comida.nombre_comida == comida4: 
			comida.comida_del_dia = True
			comidas.append(returnJson_comida(comida))
		else: comida.comida_del_dia = False
	return json.dumps(comidas)

def get_best_comida(n):
	comidas = Comida.query().order(-Comida.puntaje_promedio).fetch()
	if len(comidas) > n: comidas = comidas[:n]
	aux = []
	for comida in comidas:
		aux.append(returnJson_comida(comida))
	return json.dumps(aux)

def delete_comida(id):
	comida = Comida.get_by_id(int(id))
	comida.key.delete()
	return "Correct"

def get_all_comida():
	comidas = Comida.query().fetch()
	c = []
	if comidas:
		for comida in comidas:
			c.append(returnJson_comida(comida))
	return json.dumps(c)

def get_comida(id):
	return json.dumps(returnJson_comida(Comida.get_by_id(int(id))))
""" FIN METODOS COMIDA """
