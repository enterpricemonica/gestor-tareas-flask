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

@app.route('/complete/<int:id>')
def complete(id):
    completar_tarea(id)
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']
        agregar_tarea(task)
    return render_template('index.html', tasks=tareas)

if __name__ == '__main__':
    app.run(debug=True)