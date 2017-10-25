# GNU/GPL3 David Crespo, 2017
import json
import fichero
import webops
import url_gen
fichero = fichero.Fichero('pylibra')
fichero.gendirs()
web = webops.WebOp()
direccion = url_gen.Peticiones()
class Libro:
	def __init__(self, id):
		try:
			self.datos = fichero.abrir_ficha(id)
			self.datos = json.loads(self.datos)
		except FileNotFoundError:
			if web.get_web_to_file(direccion.get_book_by_id(id), fichero.datos(id)):
				self.datos = fichero.abrir_ficha(id)
				self.datos = json.loads(self.datos)
	def nuevo(self, id):
		self.actual=id
	def datos(self):
		self.datos = fichero.abrir_ficha(self.actual)
		return json.loads(self.datos)
	def cover(self):
		return fichero.cargar_imagen(self.get_id())
	def get_idx(self):
		lista = []
		for i in self.datos:
			lista = lista + [i]
		return lista
	def get_id(self):
		return self.datos['ID']
	def get_content(self):
		return self.datos['content']
	def get_url_details(self):
		return self.datos['url_details']
	def get_full_categories(self):
		return self.datos['categories']
	def get_num_comments(self):
		return self.datos['num_comments']
	def get_url_download(self):
		return self.datos['url_download']
	def get_cover(self):
		return self.datos['cover']
	def get_thumbnail(self):
		return self.datos['thumbnail']
	def get_publisher_date(self):
		return self.datos['publisher_date']
	def get_publisher(self):
		return self.datos['publisher']
	def get_language(self):
		return self.datos['language']
	def get_author(self):
		return self.datos['author']
	def get_pages(self):
		return self.datos['pages']
	def get_content_short(self):
		return self.datos['content_short']
	def get_title(self):
		return self.datos['title']
	def get_full_tags(self):
		return self.datos['tags']
	def get_categories_names(self):
		lista = []
		for i in self.get_full_categories():
			lista = lista + [i.pop('name')]
		return lista
	def get_tag_names(self):
		lista = []
		for i in self.get_full_tags():
			lista = lista + [i.pop('name')]
		return lista
	def get_license(self):
		return 'N/A'
	def formulario(self):
		lista = [self.get_id(), self.get_title(), self.get_author(), 
					self.get_publisher(), self.get_publisher_date(), 
					self.get_language(), self.get_pages(), self.get_url_download(),
					self.get_license(), self.get_content()]
		return lista
class Categorias:	
	def __init__(self):
		self.actual = None
	def datos(self):
		try:
			return fichero.leer_categorias()
		except FileNotFoundError:
			if web.get_web_to_file(direccion.list_categories(), fichero.categorias()):
				return fichero.leer_categorias()
	def entradas(self):
		valor = False
		nuevo = []
		cadena = ''
		for i in self.datos():
			if i =='{':
				valor=True
			if valor:
				cadena = cadena + i
			if i == '}':
				valor = False
				nuevo = nuevo + [cadena]
				cadena=''
		return nuevo
	def get_nombres(self):
		lista = []
		for i in self.entradas():
			categoria = json.loads(i)
			lista = lista + [categoria['name']]
		return lista
	def get_full(self):
		lista = []
		valores = []
		for i in self.entradas():
			categoria = json.loads(i)
			valores = [[categoria['category_id']]+[categoria['name']]+[categoria['nicename']]]
			lista = lista + valores
		return lista
	def get_id_by_name(self, nombre):
		for i in self.entradas():
			entrada = json.loads(i)
			if nombre == entrada['name']:
				return entrada['category_id']
	def descargar_subcategorias(self):
		for i in self.get_full():
			web.get_web_to_file(direccion.list_subcategories(str(i[0])), 
												fichero.subcategoria(str(i[0])))
class Subcategorias:
	def __init__(self, id):
		self.id = id
	def datos(self):
		try:
			return fichero.leer_subcategoria(self.id)
		except FileNotFoundError:
			tmp_cats = Categorias()
			tmp_cats.descargar_subcategorias()
			return fichero.leer_subcategoria(self.id)
	def entradas(self):
		valor = False
		nuevo = []
		cadena = ''
		for i in self.datos():
			if i =='{':
				valor=True
			if valor:
				cadena = cadena + i
			if i == '}':
				valor = False
				nuevo = nuevo + [cadena]
				cadena=''
		return nuevo
	def get_full(self):
		lista = []
		valores = []
		for i in self.entradas():
			categoria = json.loads(i)
			valores = [[categoria['subcategory_id']]+[categoria['name']]+[categoria['nicename']]]
			lista = lista + valores
		return lista
class Busqueda:
	def datos(self):
		return fichero.leer_busqueda()
	def entradas(self):
		valor = False
		corchete=False
		nuevo = []
		cadena = ''
		for i in self.datos():
			if i =='{':
				valor=True
			if i == '[':
				corchete=True
			if valor:
				cadena = cadena + i
			if i == ']':
				corchete = False
			if i == '}':
				if corchete:
					pass
				else:
					valor = False
					nuevo = nuevo + [cadena]
					cadena=''
		return nuevo
	def num_entradas(self):
		a=0
		for i in self.entradas():
			a = a +1
		return a
	def get_id_list(self):
		lista =[]
		for i in self.entradas():
			entrada = json.loads(i)
			lista = lista + [entrada['ID']]
		return lista
	def get_id(self, num):
		datos = self.entradas()[num]
		mas_datos = json.loads(datos)
		return mas_datos['ID']
	def limpiar_busqueda(self):
		fichero.remove_tmp()
	def cargar_miniatura(self, id):
		return fichero.cargar_imagen_mini(id)
	def miniatura_not_found(self):
		return fichero.cargar_imagen_nula_mini()
	def cover_not_found(self):
		return fichero.cargar_imagen_nula()
	def datos_libro(self, num):
		datos = Libro(self.get_id(num))
		try:
			imagen = self.cargar_miniatura(str(datos.get_id()))
		except:
			if web.get_web_to_file(datos.get_thumbnail(), fichero.imagen(str(datos.get_id()))):
				imagen = self.cargar_miniatura(str(datos.get_id()))
			else:
				imagen = self.miniatura_not_found()
		listadatos= datos.get_title(), str(datos.get_id()), imagen
		return listadatos
	def novedades(self):
		direccion.reset()
		self.limpiar_busqueda()
		web.get_web_to_file(direccion.most_viewed(), fichero.fichero_tmp())
	def nueva(self, datos):
		direccion.reset()
		self.limpiar_busqueda()
		self.mas_resultados(datos)
	def mas_resultados(self, datos):
		titulo, categoria, subcategoria, rango = datos
		if titulo=='':
			direccion.title_off()
		else:
			direccion.book_title(titulo)
		if categoria!='Todas':
			direccion.category_id(categoria)
		else:
			direccion.category_id_off()
		if subcategoria!='Todas':
			direccion.subcategory_id(subcategoria)
		else:
			direccion.subcategory_id_off()
		direccion.results_range(rango)
		web.get_web_to_file(direccion.get_webline(), fichero.fichero_tmp())
	def reset(self):
		direccion.reset()
		
		
	
