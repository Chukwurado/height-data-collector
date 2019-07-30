import psycopg2
from flask import Flask, render_template, request

from send_email import send_email
from dbconfig import DBURI

app=Flask(__name__)

class Data():
    def __init__(self):
        self.con=psycopg2.connect(DBURI)
        self.cur=self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS data (id SERIAL PRIMARY KEY, email TEXT, height INTEGER)")
        self.con.commit()

    def insert(self, email, height):
        self.cur.execute("INSERT INTO data (email, height) VALUES (%s,%s)", (email, height))
        self.con.commit()

    def checkEmail(self, email):
        self.cur.execute(f"SELECT * FROM data where email=lower('{email}')")
        rows=self.cur.fetchall()
        return len(rows) > 0

    def heights(self):
        self.cur.execute("SELECT height from data")
        rows=self.cur.fetchall()
        return rows

    def __del__(self):
        self.con.close()

data=Data()
@app.route("/")
def index():
    Data()
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form['email_name']
        height=request.form['height_name']
    
    if data.checkEmail(email):
        return render_template("index.html", text="Email has been used") 

    data.insert(email, height)
    all_hieghts=[x[0] for x in data.heights()]
    avg_height=sum(all_hieghts) / len(all_hieghts)
    send_email(email, height, avg_height, len(all_hieghts))
    return render_template("success.html")

if __name__ == '__main__':
    app.debug=True
    app.run()
