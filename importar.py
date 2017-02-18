#!/usr/bin/python2
# coding=UTF-8
 
#-------------------------------------------------------------------------------
#
# GoogleFormUpdater v2.0
#
# Autor: El Informático de Guardia [https://goo.gl/DlxXR]
# Ayuda: Para más información consulta el artículo http://wp.me/pgnIv-1Pw
#
# VERSIONES
# -------------------------------
#
#   2.0 Obtiene, a partir de la URL del formulario web, los campos a utilizar
#       evitando tener que inyectar jQuery sobre el html.
#       Edita el fichero CSV para incluir los nombres de los campos obtenidos
#       en el paso anterior.
#
#   1.0 Versión inicial
#
# MEJORAS
# -------------------------------
#
# IDEA  Pedir únicamente el ID del formulario
#       (p.e. 1x3x3xxhDnzKmnYAtrBJYHV2AidJm5t6I) pudiendo nosotros
#               rellenar el resto de la URL y evitar tener que mirar si utiliza
#               formResponse o viewform
# IDEA  Uso de la API de Google para acceder al formulario y obtener el CSV
#       sin intervención del usuario.
#
#-------------------------------------------------------------------------------
 
import csv
import requests
#import urllib
import urllib2
from lxml import html as lxmlhtml
 
FICHERO_DATOS='./respuestas2.csv'
URL_FORMULARIO="https://docs.google.com/forms/d/PON-AQUI-EL-ID-DEL-FORMULARIO/formResponse"
 
#-------------------------------------------------------------------------------
# Obtiene los campos utilizados por el formulario web de Google Drive
#-------------------------------------------------------------------------------
 
def getCampos():
 
        html = urllib2.urlopen(URL_FORMULARIO).read()
 
        tree = lxmlhtml.fromstring(html)
        r= tree.xpath("//div[contains(@class,'ss-form-entry')]//*[@name]/@name")
 
        # Eliminamos nombres de campo duplicados (respetando orden de aparición)
        r=[ii for n,ii in enumerate(r) if ii not in r[:n]]
 
        return 'Marca temporal,'+','.join(r) #+'"'
 
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
                        header = getCampos().split(",")
                else:
                        colnum = 0
                        payload={}
                        for col in row:
                                if colnum>0:
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
