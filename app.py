from flask import Flask, render_template, url_for, request, redirect
# Here render_template is used for rendering the templates or html files on the web page.
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)   # here __name__ references this file.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test1.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        if task_content != "":
            new_task = Todo(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')

            except:
                return 'There is an error when inserting the data into the data base.'
        
        else:
            return redirect('/')

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'Error 404'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return 'Error while Updating data' 

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    # because of this debug == true we can see the errors on the web page.
    app.run(debug=True)   
