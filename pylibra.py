# GNU/GPL3 David Crespo, 2017
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import libra
import webbrowser

class Principal:
	def __init__(self):
		constructor = Gtk.Builder()
		self.busqueda = libra.Busqueda()
		self.num_categorias=0
		self.num_subcategorias=0
		self.rango='0,10'
		constructor.add_from_file("libra.glade")
		constructor.connect_signals(self)
		self.principal = constructor.get_object('principal')
		self.categoria_combo=constructor.get_object('categoria')
		self.subcategoria_combo=constructor.get_object('subcategoria')
		self.anterior=constructor.get_object('anterior')
		self.siguiente=constructor.get_object('siguiente')
		self.descargar=constructor.get_object('descargar')
		self.entrada_titulo = constructor.get_object('titulo')
		self.miniatura = constructor.get_object('miniatura')
		self.posicion = constructor.get_object('posicion')
		self.emergente = constructor.get_object('emergente')
		self.mensaje = constructor.get_object('mensaje')
		self.miniatura.set_from_pixbuf(self.busqueda.cover_not_found())
		self.anterior.set_sensitive(False)
		self.siguiente.set_sensitive(False)
		self.descargar.set_sensitive(False)
		self.principal.maximize()
		self.campo_formulario=[]
		a = 0
		self.entrada=[]
		self.imagen=[]
		for i in range(0, 10):
			entrada = 'entrada%s'%(a)
			campo_formulario='campo%s'%a
			n_imagen = 'image%s'%a
			self.campo_formulario=self.campo_formulario+[constructor.get_object(campo_formulario)]
			self.entrada=self.entrada+[constructor.get_object(entrada)]
			self.imagen=self.imagen+[constructor.get_object(n_imagen)]
			self.ajustar_entrada_inicio(a)
			self.entrada[a].connect('clicked', self.seleccion, a)
			a=a+1
		self.lista_categorias = constructor.get_object('categorias')
		self.lista_subcategorias = constructor.get_object('subcategorias')
		self.lista_busqueda = constructor.get_object('lista_busqueda')
		self.actualizar_lista_categorias()
		self.libro_actual=''
		self.principal.show()
		Gtk.main()
	def seleccion(self, *args):
		self.libro_actual=self.obtener_id_titulo_busqueda(args[1])
		self.rellenar_formulario()
	def acerca_de(self, *args):
		self.mensaje.set_text('GNU/GPL 2017\nDavid Crespo')
		self.emergente.show()
	def on_si_clicked(self, *args):
		self.emergente.hide()
	def on_combo_categoria_changed(self, *args):
		self.busqueda.reset()
		self.recargar_subcategoria()
		self.subcategoria_combo.set_text('Todas')
	def on_combo_subcategoria_changed(self, *args):
		self.busqueda.reset()
	def on_delete_event(self, *args):
		Gtk.main_quit(*args)
	def on_novedades_clicked(self, *args):
		self.busqueda.novedades()
		self.rango='0,10'
		self.categoria_combo.set_text('Todas')
		self.subcategoria_combo.set_text('Todas')
		self.obtener_busqueda()
		self.siguiente.set_sensitive(False)
	def on_buscar_clicked(self, *args):
		self.rango='0,10'
		self.busqueda.nueva(self.parametros())
		self.obtener_busqueda()
	def on_anterior_clicked(self, *args):
		rango = self.rango.split(',')
		rango[0]=int(rango[0])-10
		self.rango='%s,%s'%(rango[0], rango[1])
		self.busqueda.mas_resultados(self.parametros())
		self.obtener_busqueda()
	def on_siguiente_clicked(self, *args):
		rango = self.rango.split(',')
		rango[0]=int(rango[0])+10
		self.rango='%s,%s'%(rango[0], rango[1])
		self.busqueda.mas_resultados(self.parametros())
		self.obtener_busqueda()
	def parametros(self):
		params = [self.entrada_titulo.get_text(), self.obtener_id_categoria(), 
						self.obtener_id_subcategoria(), self.rango]
		return params
	def on_descargar_clicked(self, *args):
		webbrowser.open_new_tab(self.campo_formulario[7].get_text())
	def rellenar_formulario(self):
		libro = libra.Libro(self.libro_actual)
		datos = libro.formulario()
		a=0
		for i in self.campo_formulario:
			i.set_text(datos[a])
			a = a +1
		self.miniatura.set_from_pixbuf(libro.cover())
		self.descargar.set_sensitive(True)
	def actualizar_lista_categorias(self):
		categorias = libra.Categorias()
		self.lista_categorias.clear()
		self.lista_categorias.append(['Todas', 'Todas'])
		a=0
		for i in categorias.get_full():
			self.lista_categorias.append([i[1], str(i[0])])
			print(i[0])
			a = a + 1
		self.num_categorias=a
	def obtener_id_subcategoria(self):
		valor='Todas'
		for i in range(0, self.num_subcategorias):
			if self.lista_subcategorias.get_value(self.lista_subcategorias.get_iter(i), 0)==self.subcategoria_combo.get_text():
				valor=(self.lista_subcategorias.get_value(self.lista_subcategorias.get_iter(i), 1))
				break
		return valor
	def obtener_id_categoria(self):
		valor='Todas'
		for i in range(0, self.num_categorias):
			if self.lista_categorias.get_value(self.lista_categorias.get_iter(i), 0)==self.categoria_combo.get_text():
				valor=(self.lista_categorias.get_value(self.lista_categorias.get_iter(i), 1))
				break
		return valor
	def obtener_id_titulo_busqueda(self, valor):
		return str(self.lista_busqueda.get_value(self.lista_busqueda.get_iter(valor), 1))
	def recargar_subcategoria(self):
		if self.obtener_id_categoria()!='Todas':
			subcategorias = libra.Subcategorias(self.obtener_id_categoria())
			self.lista_subcategorias.clear()
			self.lista_subcategorias.append(['Todas', 'Todas'])
			a=0
			for i in subcategorias.get_full():
				self.lista_subcategorias.append([i[1], str(i[0])])
				a=a+1
			self.num_subcategorias=a
	def obtener_busqueda(self):
		rango=self.rango.split(',')
		if int(rango[0])<=0:
			self.anterior.set_sensitive(False)
		else:
			self.anterior.set_sensitive(True)
		a=0
		self.lista_busqueda.clear()
		for i in self.busqueda.entradas():
			titulo, id, imagen = self.busqueda.datos_libro(a)
			self.ajustar_entrada(a, True, titulo, imagen)
			self.lista_busqueda.append([titulo, id])
			a=a+1
		self.posicion.set_text('%s/%s'%(rango[0], int(rango[0])+a))
		if a+1 <= len(self.entrada):
			for i in range(a, len(self.entrada)):
				self.ajustar_entrada(a, False, ' ', self.busqueda.miniatura_not_found())
				a=a+1
			self.siguiente.set_sensitive(False)
		else:
			self.siguiente.set_sensitive(True)
	def ajustar_entrada_inicio(self, num):
		self.entrada[num].set_sensitive(False)
		self.entrada[num].set_label(' ')
		self.imagen[num].set_from_pixbuf(self.busqueda.miniatura_not_found())
	def ajustar_entrada(self, num, sens, texto, imagen):
		self.entrada[num].set_sensitive(sens)
		self.entrada[num].set_label(texto)
		self.imagen[num].set_from_pixbuf(imagen)
'''
if os.name == 'posix':
	principal = Principal()
else:
	respuesta = input(''Su sistema operativo es %s.
	No es seguro que este programa funcione en su sistema.
	Está seguro de querer continuar? s/n''%(os.name))
	if respuesta == 's':
		principal = Principal()
	else:
		print('Saliendo del programa')
'''
principal=Principal()
