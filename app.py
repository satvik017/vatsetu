from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///vatsetu.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class vatsetu(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(800), nullable=True)
    place = db.Column(db.String(200), nullable=False)
    item = db.Column(db.String(500), nullable=False)
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def fun1():
    return render_template("index.html") 

@app.route('/txtfind', methods=['GET','POST'])
def search():
    if request.method=='POST':
        search=request.form['search']
        allTodo=vatsetu.query.all()
        return render_template('page3.html',allTodo=allTodo, search=search)
    else:
        return render_template("index.html")


@app.route('/fun')
def fun():
    return render_template("page1.html")

@app.route('/donor', methods=['GET','POST'])
def donate():
    allTodo = vatsetu.query.all()
    if request.method=='POST':
        items = request.form['donoitem']
        desc = request.form['donodesc']
        phone = int(request.form['donomobile'])
        city = request.form['donocity']
        todo = vatsetu(phone=phone, place=city, item=items, description=desc)
        db.session.add(todo)
        db.session.commit()
        allTodo = vatsetu.query.all() 
    return render_template('page3.html', allTodo=allTodo, item=0, place=0,search=0)

@app.route('/donorinfo')
def donar():
    return render_template('page2.html')

@app.route('/search', methods=['GET','POST'])
def find():
    if request.method=='POST':
        item=request.form['item']
        place=request.form['place']
        allTodo = vatsetu.query.all()
        return render_template("page3.html", item=item, place=place, allTodo=allTodo)
    else:
        return render_template('index.html')

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = vatsetu.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/donor")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        item = request.form['title']
        desc = request.form['desc']
        phone = request.form['phone']
        place = request.form['city']
        todo = vatsetu.query.filter_by(sno=sno).first()
        todo.item = item
        todo.phone = phone
        todo.place = place
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/donor")
        
    todo = vatsetu.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    app.run(debug=False, post='0.0.0.0')