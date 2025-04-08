from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os  # Importar os para obtener el puerto

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de MySQL
app.config['MYSQL_HOST'] = '52.41.36.82'
app.config['MYSQL_PORT'] = 3306  # Asegúrate de que este sea el puerto correcto
app.config['MYSQL_USER'] = 'root'  # Asegúrate de que este sea el usuario correcto
app.config['MYSQL_PASSWORD'] = ''  # Deja este campo vacío si no hay contraseña
app.config['MYSQL_DB'] = 'agenda_citas'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                if account['role'] == 'doctor':
                    return redirect(url_for('doctor_menu'))
                else:
                    return redirect(url_for('user_menu'))
            else:
                msg = 'Incorrect username/password!'
        except MySQLdb.Error as e:
            msg = f"Error operativo de MYSQLdb: {e}"
    return render_template('login.html', msg=msg)

# Ruta para el menú del usuario
@app.route('/user_menu')
def user_menu():
    if 'loggedin' in session:
        return render_template('user_menu.html', username=session['username'])
    return redirect(url_for('login'))

# Ruta para el menú del doctor
@app.route('/doctor_menu')
def doctor_menu():
    if 'loggedin' in session:
        return render_template('doctor_menu.html', username=session['username'])
    return redirect(url_for('login'))

# Ruta para agendar cita
@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    if 'loggedin' in session:
        if request.method == 'POST':
            order_number = request.form['order_number']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM orders WHERE order_number = %s AND user_id = %s', (order_number, session['id'],))
            order = cursor.fetchone()
            if order:
                cursor.execute('SELECT * FROM doctors WHERE specialty = %s', (order['specialty'],))
                doctors = cursor.fetchall()
                return render_template('select_doctor.html', doctors=doctors, order=order)
            else:
                flash('Su orden no es válida, por favor agende una cita con un médico general')
                cursor.execute('SELECT * FROM doctors WHERE specialty = "medicina general"')
                doctors = cursor.fetchall()
                return render_template('select_general_doctor.html', doctors=doctors)
        return render_template('agendar_cita.html')
    return redirect(url_for('login'))

@app.route('/select_doctor', methods=['POST'])
def select_doctor():
    if 'loggedin' in session:
        doctor_id = request.form['doctor_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM appointments WHERE doctor_id = %s AND user_id IS NULL', (doctor_id,))
        appointments = cursor.fetchall()
        return render_template('select_appointment.html', appointments=appointments, doctor_id=doctor_id)
    return redirect(url_for('login'))

# Ruta para seleccionar doctor general
@app.route('/select_general_doctor', methods=['GET', 'POST'])
def select_general_doctor():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id, name FROM doctors WHERE specialty = "medicina general"')
        doctors = cursor.fetchall()
        return render_template('select_general_doctor.html', doctors=doctors)
    return redirect(url_for('login'))

@app.route('/confirm_appointment', methods=['POST'])
def confirm_appointment():
    if 'loggedin' in session:
        appointment_id = request.form['appointment_id']
        order_number = request.form['order_number']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE appointments SET user_id = %s WHERE id = %s', (session['id'], appointment_id,))
        cursor.execute('DELETE FROM orders WHERE order_number = %s', (order_number,))
        mysql.connection.commit()
        flash('Cita agendada exitosamente')
        return redirect(url_for('user_menu'))
    return redirect(url_for('login'))

@app.route('/confirm_general_appointment', methods=['POST'])
def confirm_general_appointment():
    if 'loggedin' in session:
        appointment_id = request.form['appointment_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE appointments SET user_id = %s WHERE id = %s', (session['id'], appointment_id,))
        mysql.connection.commit()
        flash('Cita agendada exitosamente')
        return redirect(url_for('user_menu'))
    return redirect(url_for('login'))

# Ruta para ver citas
@app.route('/ver_citas')
def ver_citas():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT a.date, a.time, a.cubicle, d.name as doctor FROM appointments a JOIN doctors d ON a.doctor_id = d.id WHERE a.user_id = %s', (session['id'],))
        citas = cursor.fetchall()
        if not citas:
            flash('Aún no hay citas agendadas')
        return render_template('ver_citas.html', citas=citas)
    return redirect(url_for('login'))

# Ruta para cancelar citas
@app.route('/cancelar_citas', methods=['GET', 'POST'])
def cancelar_citas():
    if 'loggedin' in session:
        if request.method == 'POST':
            appointment_id = request.form['appointment_id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE appointments SET user_id = NULL WHERE id = %s', (appointment_id,))
            mysql.connection.commit()
            flash('Cita cancelada exitosamente')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT a.id, a.date, a.time, a.cubicle, d.name as doctor FROM appointments a JOIN doctors d ON a.doctor_id = d.id WHERE a.user_id = %s', (session['id'],))
        citas = cursor.fetchall()
        return render_template('cancelar_citas.html', citas=citas)
    return redirect(url_for('login'))

# Ruta para ver órdenes
@app.route('/mis_ordenes')
def mis_ordenes():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM orders WHERE user_id = %s', (session['id'],))
        ordenes = cursor.fetchall()
        return render_template('mis_ordenes.html', ordenes=ordenes)
    return redirect(url_for('login'))

# Ruta para ver perfil
@app.route('/mi_perfil')
def mi_perfil():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        perfil = cursor.fetchone()
        return render_template('mi_perfil.html', perfil=perfil)
    return redirect(url_for('login'))

# Ruta para ver la agenda del doctor
@app.route('/ver_agenda')
def ver_agenda():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT a.date, a.time, a.cubicle, u.username as patient FROM appointments a LEFT JOIN users u ON a.user_id = u.id WHERE a.doctor_id = %s', (session['id'],))
        agenda = cursor.fetchall()
        return render_template('ver_agenda.html', agenda=agenda)
    return redirect(url_for('login'))

# Ruta para asignar órdenes
@app.route('/asignar_ordenes', methods=['GET', 'POST'])
def asignar_ordenes():
    if 'loggedin' in session:
        if request.method == 'POST':
            user_id = request.form['user_id']
            specialty = request.form['specialty']
            order_number = specialty[:2] + str(user_id).zfill(4)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO orders (user_id, doctor_id, specialty, order_number) VALUES (%s, %s, %s, %s)', (user_id, session['id'], specialty, order_number,))
            mysql.connection.commit()
            flash('Orden asignada exitosamente')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE role = "user"')
        users = cursor.fetchall()
        return render_template('asignar_ordenes.html', users=users)
    return redirect(url_for('login'))

# Ruta para salir
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Obtén el puerto del entorno (Render asignará este puerto)
    port = int(os.environ.get("PORT", 5000))

    # Ejecuta Flask en el puerto adecuado
    app.run(debug=True, host='0.0.0.0', port=port)

