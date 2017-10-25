# GNU/GPL3 David Crespo, 2017
from urllib3 import PoolManager
class WebOp:
	def __init__(self):
		self.web = PoolManager()
		self.charset = None
	def get_web(self, web):
		datos = self.web.request('GET', web)
		if datos.status == 200:
			if datos.headers['content-type'].startswith('text'):
				tipocontenido = datos.headers['content-type'].split('=')
				self.charset=tipocontenido[1]
			return datos.data
		else:
			return False
	def get_web_to_file(self, web, file):
		try:
			datos = self.get_web(web)
			if datos:
				fichero = open(file, 'wb')
				fichero.write(datos)
				fichero.close()
				return True
			else:
				return False
		except:
			return False
		
