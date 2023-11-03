from datetime import datetime
from src.lib.appwrapper import *
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, ID, STORED

class App(AppWrapper):
    def __init__(self):
        self.agenda = {}

        super().__init__(rootDir= os.path.dirname(os.path.abspath(__file__)),
            menu=[
                MenuTab(
                    title = 'Datos',
                    items = [
                        MenuTabItem(
                            label = 'Cargar',
                            callback = self.store
                        ),
                        MenuTabItem(
                            label = 'Listar',
                            callback = self.list
                        ),
                        MenuTabItem(
                            label = 'Salir',
                            callback = self.close
                        )
                    ]
                ),
                MenuTab(
                    title = 'Buscar',
                    items = [
                        MenuTabItem(
                            label = 'Cuerpo',
                            callback = self.searchCuerpo
                        ),
                        MenuTabItem(
                            label = 'Fecha',
                            callback = self.searchFecha
                        ),
                        MenuTabItem(
                            label = 'Spam',
                            callback = self.searchSpam
                        )
                    ]
                )
            ],
            components=[],
            schema=Schema(remitente=ID(stored=True), destinatarios=KEYWORD(stored=True), fecha=DATETIME(stored=True), asunto=TEXT(stored=True), contenido=TEXT(stored=True,phrase=False), nombrefichero=STORED)
        )

    def store(self):
        def add_doc(writer, path, docName):
            docPath = os.path.join(path, docName)

            try:
                fileobj=open(docPath, "r")
                rte=fileobj.readline().strip()
                dtos=fileobj.readline().strip()
                f=fileobj.readline().strip()
                dat=datetime.datetime.strptime(f,'%Y%m%d')
                ast=fileobj.readline().strip()
                ctdo=fileobj.read()
                fileobj.close()

                writer.add_document(remitente=rte, destinatarios=dtos, fecha=dat, asunto=ast, contenido=ctdo, nombrefichero=docName)
            
            except:
                messagebox.showerror("ERROR", "Error: No se ha podido añadir el documento "+docPath)

        def cargarAgenda():
            docPath= os.path.join(self.dirs['data'], 'Agenda', 'agenda.txt')

            try:
                fileobj=open(docPath, "r")
                email=fileobj.readline()

                while email:
                    nombre=fileobj.readline()
                    self.agenda[email.strip()]=nombre.strip()
                    email=fileobj.readline()

                fileobj.close()

            except:
                messagebox.showerror("ERROR", f'No se ha podido crear la agenda. Compruebe que existe el fichero {docPath}')

        self.createIndex(docsDir='Correos', addDoc=add_doc)
        cargarAgenda()

    def showList(self, results):
        content = []
        for row in results:
            content.append([
                'REMITENTE: ' + row['remitente'],
                'DESTINATARIOS: ' + row['destinatarios'],
                'FECHA: ' + row['fecha'].strftime('%d-%m-%Y'),
                'ASUNTO: ' + row['asunto'],
                'CUERPO: ' + row['contenido']
            ])

        self.gui.listScrollWindow('Resultados', content)

    def list(self):
        if not exists_in(self.dirs['index']):
            messagebox.showerror("ERROR", "No existe el Ã­ndice. Se procede a crearlo")
            self.store()

        self.whoosh.getAll(self.showList)
    
    def searchCuerpo(self):
        def search(param, window):
            self.whoosh.query('contenido', param, self.showList)

        if not exists_in(self.dirs['index']):
            messagebox.showerror("ERROR", "No existe el Í­ndice. Se procede a crearlo")
            self.store()

        newWindow = self.gui.formWindow(title="Buscar mensajes según cuerpo", components = [{
            'type': 'label',
            'text': 'Introduzca consulta en el cuerpo: ',
            'side': 'left'
        }, {
            'type': 'text',
            'func': search,
            'side': 'left',
            'width': 30
        }])

        newWindow.create()

    def searchFecha(self):
        def search(param, window):
            try:
                self.whoosh.query('fecha', param, self.showList)
            except:
                messagebox.showerror('Error', 'Formato de fecha incorrecto')

        if not exists_in(self.dirs['index']):
            messagebox.showerror("ERROR", "No existe el Índice. Se procede a crearlo")
            self.store()

        newWindow = self.gui.formWindow(title="Buscar mensajes según cuerpo", components = [{
            'type': 'label',
            'text': 'Introduzca consulta en el cuerpo: ',
            'side': 'left'
        }, {
            'type': 'text',
            'func': search,
            'side': 'left',
            'width': 30
        }])

        newWindow.create()

    def searchSpam(self):
        def search(param, window):
            self.whoosh.query('asunto', param, self.showList)

        if not exists_in(self.dirs['index']):
            messagebox.showerror("ERROR", "No existe el Índice. Se procede a crearlo")
            self.store()

        newWindow = self.gui.formWindow(title="Buscar mensajes según cuerpo", components = [{
            'type': 'label',
            'text': 'Introduzca el término spam: ',
            'side': 'left'
        }, {
            'type': 'text',
            'func': search,
            'side': 'left',
            'width': 30
        }])

        newWindow.create()

# Lanza App
App()