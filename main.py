import sqlite3
import os
import shutil
from datetime import datetime
import requests
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window

# ========== CONFIGURACIÓN ==========
DB_PATH = "datos_ilmvc.db"
MODELOS_PATH = "MODELOS_DE_IA"

# ========== FUNCIONES BACKEND ==========
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS informacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            titulo TEXT,
            contenido TEXT,
            fecha TEXT
        )
    ''')
    conn.commit()
    conn.close()

def agregar_info(tipo, titulo, contenido):
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO informacion (tipo, titulo, contenido, fecha) VALUES (?,?,?,?)",
                       (tipo, titulo, contenido, fecha))
        conn.commit()
        conn.close()
        return json.dumps({"exito": True, "mensaje": f"Guardado: {titulo}"})
    except Exception as e:
        return json.dumps({"exito": False, "mensaje": f"Error: {str(e)}"})

def ver_buscar_info(busqueda=""):
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if busqueda:
            cursor.execute("SELECT * FROM informacion WHERE titulo LIKE? OR contenido LIKE?",
                           (f"%{busqueda}%", f"%{busqueda}%"))
        else:
            cursor.execute("SELECT * FROM informacion ORDER BY id DESC LIMIT 20")
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                "id": row[0], "tipo": row[1], "titulo": row[2],
                "contenido": row[3], "fecha": row[4]
            })
        conn.close()
        return resultados
    except Exception as e:
        return []

def crear_respaldo():
    try:
        if not os.path.exists("RESPALDOS"):
            os.makedirs("RESPALDOS")
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = f"RESPALDOS/respaldo_{fecha}.db"
        shutil.copy2(DB_PATH, destino)
        return {"exito": True, "archivo": destino, "mensaje": f"Respaldo: {destino}"}
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}

def generar_informe_basico():
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM informacion ORDER BY fecha DESC")
        datos = cursor.fetchall()
        conn.close()

        if not os.path.exists("ARCHIVOS_GENERADOS"):
            os.makedirs("ARCHIVOS_GENERADOS")

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = f"ARCHIVOS_GENERADOS/informe_{fecha}.txt"

        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(f"=== INFORME BASICO ===\n")
            f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total registros: {len(datos)}\n\n")
            for row in datos:
                f.write(f"[{row[4]}] {row[1]} - {row[2]}\n{row[3]}\n\n")

        return {"exito": True, "archivo": archivo, "mensaje": f"Informe: {archivo}"}
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}

def verificar_modelos_ia():
    try:
        if not os.path.exists(MODELOS_PATH):
            return json.dumps({"tiene_ia": False, "modelos": "", "mensaje": "No hay modelos IA"})
        modelos = os.listdir(MODELOS_PATH)
        modelos_str = ", ".join(modelos) if modelos else "Sin modelos"
        return json.dumps({"tiene_ia": len(modelos) > 0, "modelos": modelos_str})
    except Exception as e:
        return json.dumps({"tiene_ia": False, "modelos": "", "mensaje": f"Error: {str(e)}"})

def descargar_modelo_url(url, nombre_archivo):
    try:
        if not os.path.exists(MODELOS_PATH):
            os.makedirs(MODELOS_PATH)
        ruta = f"{MODELOS_PATH}/{nombre_archivo}"
        r = requests.get(url, stream=True, timeout=30)
        with open(ruta, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return json.dumps({"exito": True, "mensaje": f"Modelo descargado: {nombre_archivo}"})
    except Exception as e:
        return json.dumps({"exito": False, "mensaje": f"Error: {str(e)}"})

# ========== INTERFAZ KIVY ==========
class GestorMasterSRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Titulo
        self.add_widget(Label(
            text='[b]GestorMasterS.ILMVC[/b]',
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0.3, 0.7, 1, 1)
        ))
        
        # Subtitulo
        self.add_widget(Label(
            text='Gestor de Informacion y Modelos IA',
            font_size='14sp',
            size_hint_y=None,
            height=25,
            color=(0.7, 0.7, 0.7, 1)
        ))
        
        # === SECCION: AGREGAR ===
        self.add_widget(Label(
            text='[b]Nuevo Registro:[/b]',
            markup=True,
            size_hint_y=None,
            height=30,
            color=(1, 0.8, 0.3, 1)
        ))
        
        self.tipo_input = TextInput(
            hint_text='Tipo (ej: Nota, Tarea, Link)',
            size_hint_y=None,
            height=45,
            multiline=False
        )
        self.add_widget(self.tipo_input)
        
        self.titulo_input = TextInput(
            hint_text='Titulo *',
            size_hint_y=None,
            height=45,
            multiline=False
        )
        self.add_widget(self.titulo_input)
        
        self.contenido_input = TextInput(
            hint_text='Contenido / Descripcion',
            multiline=True,
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.contenido_input)
        
        btn_guardar = Button(
            text='GUARDAR REGISTRO',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.3, 1)
        )
        btn_guardar.bind(on_press=self.guardar_registro)
        self.add_widget(btn_guardar)
        
        # === SECCION: BUSCAR ===
        self.add_widget(Label(
            text='[b]Buscar:[/b]',
            markup=True,
            size_hint_y=None,
            height=30,
            color=(1, 0.8, 0.3, 1)
        ))
        
        box_buscar = BoxLayout(size_hint_y=None, height=50, spacing=5)
        self.buscar_input = TextInput(
            hint_text='Buscar por titulo o contenido...',
            multiline=False
        )
        box_buscar.add_widget(self.buscar_input)
        
        btn_buscar = Button(
            text='BUSCAR',
            size_hint_x=None,
            width=100,
            background_color=(0.2, 0.4, 0.7, 1)
        )
        btn_buscar.bind(on_press=self.buscar_registros)
        box_buscar.add_widget(btn_buscar)
        self.add_widget(box_buscar)
        
        # === SECCION: ACCIONES ===
        self.add_widget(Label(
            text='[b]Herramientas:[/b]',
            markup=True,
            size_hint_y=None,
            height=30,
            color=(1, 0.8, 0.3, 1)
        ))
        
        box_acciones = BoxLayout(size_hint_y=None, height=50, spacing=5)
        
        btn_respaldo = Button(
            text='RESPALDO DB',
            background_color=(0.5, 0.3, 0.7, 1)
        )
        btn_respaldo.bind(on_press=self.hacer_respaldo)
        box_acciones.add_widget(btn_respaldo)
        
        btn_informe = Button(
            text='GENERAR INFORME',
            background_color=(0.7, 0.5, 0.2, 1)
        )
        btn_informe.bind(on_press=self.hacer_informe)
        box_acciones.add_widget(btn_informe)
        
        btn_modelos = Button(
            text='VER MODELOS IA',
            background_color=(0.2, 0.5, 0.6, 1)
        )
        btn_modelos.bind(on_press=self.ver_modelos)
        box_acciones.add_widget(btn_modelos)
        
        self.add_widget(box_acciones)
        
        # === SECCION: RESULTADOS ===
        self.add_widget(Label(
            text='[b]Registros:[/b]',
            markup=True,
            size_hint_y=None,
            height=30,
            color=(1, 0.8, 0.3, 1)
        ))
        
        self.scroll = ScrollView()
        self.resultados_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.resultados_layout.bind(minimum_height=self.resultados_layout.setter('height'))
        self.scroll.add_widget(self.resultados_layout)
        self.add_widget(self.scroll)
        
        # Cargar todo al inicio
        Clock.schedule_once(lambda dt: self.buscar_registros(None), 0.5)
    
    def guardar_registro(self, instance):
        tipo = self.tipo_input.text.strip()
        titulo = self.titulo_input.text.strip()
        contenido = self.contenido_input.text.strip()
        
        if not titulo:
            self.mostrar_popup("Error", "El titulo es obligatorio")
            return
        
        resultado = agregar_info(tipo or "General", titulo, contenido)
        data = json.loads(resultado)
        self.mostrar_popup("Resultado", data["mensaje"])
        
        if data["exito"]:
            self.tipo_input.text = ""
            self.titulo_input.text = ""
            self.contenido_input.text = ""
            self.buscar_registros(None)
    
    def buscar_registros(self, instance):
        busqueda = self.buscar_input.text.strip()
        resultados = ver_buscar_info(busqueda)
        
        self.resultados_layout.clear_widgets()
        
        if not resultados:
            lbl = Label(
                text='No hay registros',
                size_hint_y=None,
                height=60,
                color=(0.5, 0.5, 0.5, 1)
            )
            self.resultados_layout.add_widget(lbl)
            return
        
        for r in resultados:
            texto = f"[b][{r['fecha']}][/b]  [color=ffcc00]{r['tipo']}[/color] - {r['titulo']}\n[color=aaaaaa]{r['contenido'][:150]}...[/color]"
            lbl = Label(
                text=texto,
                markup=True,
                size_hint_y=None,
                height=90,
                text_size=(Window.width - 50, None),
                halign='left',
                valign='top'
            )
            self.resultados_layout.add_widget(lbl)
    
    def hacer_respaldo(self, instance):
        resultado = crear_respaldo()
        self.mostrar_popup("Respaldo", resultado["mensaje"])
    
    def hacer_informe(self, instance):
        resultado = generar_informe_basico()
        self.mostrar_popup("Informe", resultado["mensaje"])
    
    def ver_modelos(self, instance):
        resultado = verificar_modelos_ia()
        data = json.loads(resultado)
        if data.get("tiene_ia"):
            msg = f"Modelos encontrados:\n{data['modelos']}"
        else:
            msg = data.get("mensaje", "No hay modelos")
        self.mostrar_popup("Modelos IA", msg)
    
    def mostrar_popup(self, titulo, mensaje):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=mensaje))
        btn_cerrar = Button(text='Cerrar', size_hint_y=None, height=50)
        popup = Popup(title=titulo, content=content, size_hint=(0.85, 0.5))
        btn_cerrar.bind(on_press=popup.dismiss)
        content.add_widget(btn_cerrar)
        popup.open()


class GestorMasterSApp(App):
    def build(self):
        Window.clearcolor = (0.08, 0.08, 0.12, 1)
        return GestorMasterSRoot()


if __name__ == '__main__':
    GestorMasterSApp().run()
