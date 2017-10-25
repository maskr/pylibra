# GNU/GPL3 David Crespo, 2017
import os
from gi.repository import GdkPixbuf

class Fichero:
	def __init__(self, main_dir):
		self.app_dir=main_dir
		self.buffer=GdkPixbuf.Pixbuf()
	def home(self):
		return os.environ['HOME']
	def app_dir(self):
		return self.app_dir
	def main_dir(self):
		return self.home()+'/'+self.app_dir+'/'
	def directorio_datos(self):
		return self.main_dir()+'data/'
	def directorio_categorias(self):
		return self.directorio_datos()+'categorias/'
	def directorio_fichas(self):
		return self.directorio_datos()+'fichas/'
	def directorio_tmp(self):
		return self.main_dir()+'tmp/'
	def directorio_imagenes(self):
		return self.directorio_datos()+'imgs/'
	def fichero_tmp(self):
		return self.directorio_tmp()+'nuevos.dat'
	def categorias(self):
		return self.directorio_categorias() +'categories.dat'
	def subcategoria(self, id):
		return self.directorio_categorias()+'SUB'+id
	def imagen(self, id):
		return self.directorio_imagenes()+'PIC'+id
	def imagen_nula(self):
		return '110x153.png'
	def imagen_nula_mini(self):
		return 'nofile.png'
	def datos(self, id):
		return self.directorio_fichas()+'ID'+id
	def gendir(self, directorio):
		os.mkdir(directorio)
	def gendirs(self):
		lista = [self.main_dir(), self.directorio_datos(), self.directorio_categorias(), 
					self.directorio_fichas(), self.directorio_imagenes(), self.directorio_tmp()]
		for i in lista:
			if not self.checkdir(i):
				os.mkdir(i)
	def checkdir(self, dir_buscado):
		ruta = dir_buscado.split('/')
		ruta_padre=[]
		for i in ruta:
			if i == '':
				pass
			else:
				ruta_padre=ruta_padre+[i]
		objetivo = len(ruta_padre)-1
		dir_padre=''
		for i in range(0, objetivo):
			dir_padre=dir_padre+'/'+ruta_padre[i]
		dir = os.listdir(dir_padre)
		for i in dir:
			if i == ruta_padre[objetivo]:
				return True
				break
		return False
	def remove(self, fichero):
		os.remove(fichero)
	def remove_tmp(self):
		try:
			os.remove(self.fichero_tmp())
		except FileNotFoundError:
			pass
	def abrir_ficha(self, id):
		return self.leer(self.datos(id))
	def cargar_imagen_nula(self):
		return self.buffer.new_from_file(self.imagen_nula())
	def cargar_imagen_nula_mini(self):
		return self.buffer.new_from_file_at_scale(self.imagen_nula_mini(), 43, 60, True)
	def cargar_imagen(self, id):
		return self.buffer.new_from_file(self.imagen(str(id)))
	def cargar_imagen_mini(self, id):
		return self.buffer.new_from_file_at_scale(self.imagen(id), 43, 60, True)
	def leer_busqueda(self):
		return self.leer(self.fichero_tmp())
	def leer_categorias(self):
		return self.leer(self.categorias())
	def leer_subcategoria(self, id):
		return self.leer(self.subcategoria(id))
	def leer(self, nombre):
		fichero=open(nombre)
		lectura = fichero.readlines()
		fichero.close()
		for i in lectura:
			i = i.lstrip('?')
			if i.startswith('(['):
				datos = i.rstrip(';')
				datos = datos.lstrip('([')
				datos = datos.rstrip('])')
				return str(datos)
