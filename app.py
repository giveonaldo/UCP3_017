import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = './database/perpustakaan.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

with get_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS perpustakaan(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        peminjam TEXT NOT NULL,
        buku TEXT NOT NULL,
        tanggal_peminjaman TEXT NOT NULL,
        tanggal_pengembalian TEXT NOT NULL
    )''')
    conn.commit()
   
# Home 
@app.route('/')
def index():
    conn = get_connection()
    buku = conn.execute('SELECT * FROM perpustakaan').fetchall()
    conn.close()
    return render_template('index.html', buku = buku)
   
# Add 
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        peminjam = request.form['peminjam']
        buku = request.form['buku']
        tanggal_peminjaman = request.form['tanggal_peminjaman']
        tanggal_pengembalian = request.form['tanggal_pengembalian']
        conn = get_connection()
        conn.execute('INSERT INTO perpustakaan (peminjam, buku, tanggal_peminjaman, tanggal_pengembalian) VALUES (?, ?, ?, ?)',
                     (peminjam, buku, tanggal_peminjaman, tanggal_pengembalian))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_connection()
    conn.execute('DELETE FROM perpustakaan WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Edit
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_connection()
    buku = conn.execute('SELECT * FROM perpustakaan WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        peminjam = request.form['peminjam']
        buku = request.form['buku']
        tanggal_peminjaman = request.form['tanggal_peminjaman']
        tanggal_pengembalian = request.form['tanggal_pengembalian']
        conn.execute('UPDATE perpustakaan SET peminjam = ?, buku = ?, tanggal_peminjaman = ?, tanggal_pengembalian = ?  WHERE id = ?',
                     (peminjam, buku, tanggal_peminjaman,tanggal_pengembalian , id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()    
    return render_template('edit.html', buku=buku)

if __name__ == '__main__':
    app.run(debug=True)