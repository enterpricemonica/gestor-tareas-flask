from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

tareas = []
siguiente_id = 1

def guardar_datos():
    with open('tareas.json', 'w') as f:
        json.dump({'siguiente_id': siguiente_id, 'tareas': tareas}, f)

def cargar_datos():
    global siguiente_id, tareas
    try:
        with open('tareas.json', 'r') as f:
            data = json.load(f)
            tareas = data['tareas']
            siguiente_id = data['siguiente_id']
    except FileNotFoundError:
        pass

cargar_datos()

def agregar_tarea(texto):
    global siguiente_id
    tareas.append({'id': siguiente_id, 'texto': texto, 'hecho': False})
    siguiente_id += 1
    guardar_datos()

def completar_tarea(id):
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['hecho'] = True
            break
    guardar_datos()

def eliminar_tarea(id):
    global tareas
    tareas = [t for t in tareas if t['id'] != id]
    guardar_datos()

@app.route('/completar/<int:id>')
def completar(id):
    completar_tarea(id)
    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    eliminar_tarea(id)
    return redirect('/')

@app.route('/')
def index():
    # Ordenar tareas: incompletas primero, luego completadas
    tareas_ordenadas = sorted(tareas, key=lambda t: t['hecho'])
    return render_template('index.html', tasks=tareas_ordenadas)

@app.route('/agregar', methods=['POST'])
def agregar():
    texto_tarea = request.form.get('texto_tarea')
    if texto_tarea:
        agregar_tarea(texto_tarea)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)