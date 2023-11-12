from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'], nama=session['nama'], nim=session['nim'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # Implementasi fungsi login_user()
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            cur.close()

            if user:
                if isinstance(user, tuple) and len(user) >= 4:
                    session['username'] = user[0]
                    session['nama'] = user[2]
                    session['nim'] = user[3]
                    return redirect(url_for('home'))
                else:
                    return render_template('login.html', error='Invalid user data structure')

            else:
                return render_template('login.html', error='Invalid username or password')


        except Exception as e:
            error_message = f"An error occurred during login: {str(e)}"
            print(error_message)
            return render_template('login.html', error=error_message)

    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    # Implementasi fungsi logout_user()
    session.pop('username', None)
    session.pop('nama', None)
    session.pop('nim', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
