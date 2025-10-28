from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swayam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    def _repr_(self) ->str:
        return f"{self.sno} - {self.title}"
    
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=(request.form['Title'])
        description=(request.form['desc'])    
        todo=Todo(title=title,description=description)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/show')
def products():
    return 'Welcome to products page'

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=(request.form['Title'])
        description=(request.form['description'])    
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.description=description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)