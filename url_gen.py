# GNU/GPL3 David Crespo, 2017
class Peticiones:
	def __init__(self):
		self.opciones=[['id', False], ['book_title', False], ['book_author', False], 
					['publisher', False], ['publisher_date', False], ['lang', False], 
					['keyword', False], ['book_title_index', False], ['category', False], 
					['category_id', False], ['subcategory', False], ['subcategory_id', False], 
					['any_tags', False], ['results_range', '0,10'], ['criteria', False], 
					['order', False], ['since', False], ['num_items', False], 
					['count_items', False], ['decode', 'true']]
		self.metodos=[['get_categories', False], ['get_subcategories_by_category_ID', False]]
		self.servidor = 'www.etnassoft.com'
		self.ruta = '/api/v1/get/'
	def list_categories(self):
		orden = 'http://'+self.servidor+self.ruta+'?get_categories=all'
		return orden
	def most_viewed(self):
		orden = 'http://'+self.servidor+self.ruta+'?criteria=most_viewed'
		return orden
	def reset(self):
		origen = [['id', False], ['book_title', False], ['book_author', False], 
					['publisher', False], ['publisher_date', False], ['lang', False], 
					['keyword', False], ['book_title_index', False], ['category', False], 
					['category_id', False], ['subcategory', False], ['subcategory_id', False], 
					['any_tags', False], ['results_range', '0,10'], ['criteria', False], 
					['order', False], ['since', False], ['num_items', False], 
					['count_items', False], ['decode', 'true']]
		self.opciones=origen
	def list_subcategories(self, id_cat):
		orden = 'http://'+self.servidor+self.ruta+'?'+self.metodos[1][0]+'='+id_cat
		return orden
	def get_book_by_id(self, id):
		orden = 'http://'+self.servidor+self.ruta+'?id='+ id + "&callback=?"
		return orden
	def get_full_path(self):
		orden = ''
		for i in self.opciones:
			if i[1] :
				if orden == '':
					orden = orden + '?'+ i[0] + '=' + i[1]
				else:
					orden = orden + '&'+ i[0] + '=' + i[1]
		return self.ruta+orden
	def get_servidor(self):
		return self.servidor
	def set_servidor(self, nombre):
		self.servidor = nombre
	def get_path(self):
		return self.ruta
	def set_path(self, ruta):
		self.ruta = ruta
	def get_opciones(self):
		return self.opciones
	def id(self, id):
		self.opciones[0][1]=id
	def id_off(self):
		self.opciones[0][1]=False
	def book_title(self, title):
		self.opciones[1][1]=title
	def title_off(self):
		self.opciones[1][1]=False
	def book_author(self, nombre):
		self.opciones[2][1]=nombre
	def book_author_off(self):
		self.opciones[2][1]=False
	def publisher(self, nombre):
		self.opciones[3][1]=nombre
	def publisher_off(self):
		self.opciones[3][1]=False
	def publisher_date(self, date):
		self.opciones[4][1]=date
	def publisher_date_off(self):
		self.opciones[4][1]=False
	def lang(self, language):
		self.opciones[5][1]=language
	def lang_off(self):
		self.opciones[5][1]=False
	def keyword(self, key):
		self.opciones[6][1]=key
	def keyword_off(self):
		self.opciones[6][1]=False
	def book_title_index(self, datos):
		self.opciones[7][1]=datos
	def book_title_index_off(self):
		self.opciones[7][1]=False
	def category(self, cat):
		self.opciones[8][1]=cat
	def category_off(self):
		self.opciones[8][1]=False
	def category_id(self, id):
		self.opciones[9][1]=id
	def category_id_off(self):
		self.opciones[9][1]=False
	def subcategory(self, cat):
		self.opciones[10][1]=cat
	def subcategory_off(self):
		self.opciones[10][1]=False
	def subcategory_id(self, id):
		self.opciones[11][1]=id
	def subcategory_id_off(self):
		self.opciones[11][1]=False
	def any_tags(self, tags):
		self.opciones[12][1]=tags
	def any_tags_off(self):
		self.opciones[12][1]=False
	def results_range(self, range):
		self.opciones[13][1]=range
	def results_range_off(self):
		self.opciones[13][1]=False
	def criteria(self, criteria):
		self.opciones[14][1]=criteria
	def criteria_off(self):
		self.opciones[14][1]=False
	def order(self, order):
		self.opciones[15][1]=order
	def order_off(self):
		self.opciones[15][1]=False
	def since(self, since):
		self.opciones[16][1]=since
	def since_off(self):
		self.opciones[16][1]=False
	def num_items(self, num):
		self.opciones[17][1]=num
	def num_items_off(self):
		self.opciones[17][1]=False
	def count_items(self):
		self.opciones[18][1]='true'
	def count_items_off(self):
		self.opciones[18][1]=False
	def decode(self):
		self.opciones[19][1]='true'
	def decode_off(self):
		self.opciones[19][1]=False
	def get_socketline(self):
		line = 'GET %s HTTP/1.0\r\nHost: %s\r\n\r\n' % (self.get_servidor()+self.get_full_path(), self.get_servidor())
		return line
	def get_webline(self):
		line = 'http://%s'%(self.get_servidor()+self.get_full_path())
		return line
