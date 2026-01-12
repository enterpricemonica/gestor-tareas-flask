from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

tareas = []
siguiente_id = 1

def agregar_tarea(texto):
    global siguiente_id
    tareas.append({'id': siguiente_id, 'texto': texto, 'hecho': False})
    siguiente_id += 1

def completar_tarea(id):
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['hecho'] = True
            break

@app.route('/completar/<int:id>')
def completar(id):
    completar_tarea(id)
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', tasks=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    task = request.form['task']
    agregar_tarea(task)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)