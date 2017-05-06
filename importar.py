#!/usr/bin/python2
# coding=UTF-8

#-------------------------------------------------------------------------------
#
# GoogleFormUpdater v2.0
#
# Autor: El Informático de Guardia [https://goo.gl/DlxXR]
# Ayuda: Para más información consulta el artículo https://goo.gl/eziklA
#
# VERSIONES
# -------------------------------
#
#   2.0 Obtiene, a partir de la URL del formulario web, los campos a utilizar
#       evitando tener que inyectar jQuery sobre el html.
#
#       Edita el fichero CSV para incluir los nombres de los campos obtenidos
#       en el paso anterior.
#
#   1.0 Versión inicial
#
# MEJORAS
# -------------------------------
#
# IDEA 	Pedir únicamente el ID del formulario 
#      	(p.e. 1x3x3xxhDnzKmnYAtrBJYHV2AidJm5t6I) pudiendo nosotros
#		rellenar el resto de la URL y evitar tener que mirar si utiliza
#		formResponse o viewform
# IDEA  Uso de la API de Google para acceder al formulario y obtener el CSV
#       sin intervención del usuario.
#
#-------------------------------------------------------------------------------

import csv
import requests
import urllib2
from lxml import html as lxmlhtml

FICHERO_DATOS='./respuestas5.csv'
URL_FORMULARIO="https://docs.google.com/a/iesalandalus.com/forms/d/e/1FAIpQLSfWeYRsTr68aP208B_L7Cfel1qZ8SH8f4JD3uPDH9iF_j5IUw/formResponse"
#URL_FORMULARIO="https://docs.google.com/forms/d/e/1FAIpQLSfWeYRsTr68aP208B_L7Cfel1qZ8SH8f4JD3uPDH9iF_j5IUw/formResponse"

#-------------------------------------------------------------------------------
# Obtiene los campos utilizados por el formulario web de Google Drive
#-------------------------------------------------------------------------------

def getCampos():

	html = urllib2.urlopen(URL_FORMULARIO).read()

	tree = lxmlhtml.fromstring(html)
	r= tree.xpath("//input[contains(@name,'entry.')]/@name")

	# Eliminamos nombres de campo duplicados (respetando orden de aparición)
	c=[ii for n,ii in enumerate(r) if ii not in r[:n]]
	m=getCamposMultiples(c,r)

	return 'Marca temporal,'+','.join(c), m

#-------------------------------------------------------------------------------
# Simula el envío de datos al formulario web de Google Drive
#-------------------------------------------------------------------------------

def getCamposMultiples(indices, campos):
	multiples=[]
	for i in indices:
		if campos.count(i)>1:
			multiples.append(i)
	return multiples
	
#-------------------------------------------------------------------------------
# Simula el envío de datos al formulario web de Google Drive
#-------------------------------------------------------------------------------

def setRespuestas():

	ifile  = open(FICHERO_DATOS, "rb")
	reader = csv.reader(ifile)

	rownum = 0
	for row in reader:
		# Anotamos los nombres de los campos (como cabeceras) para futuros usos
		if rownum == 0:
			header, camposMultiples = getCampos()
			header=header.split(",")
		else:
			colnum = 0
			payload={}
			for col in row:
				if colnum>0:
					# Gestionamos campos de valores múltiples (checkboxes)
					if header[colnum] in camposMultiples:
						col=col.split(";")
					payload[header[colnum]]=col
				colnum += 1

			f = requests.post(url=URL_FORMULARIO, data=payload)
			if "Este contenido no ha sido creado ni aprobado por Google" in f.text:
					print "--"
					print "Error enviando los datos; revisa los nombres de los campos"
					print payload
					print "--"
			else:
					print ".",
		rownum += 1

	ifile.close()
setRespuestas()
