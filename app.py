from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

    def __rep__(self):
        return '<Task %r>' % self.id

# db.create_all()
# exit()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'
    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)

    # render_template requires files to be placed in a folder called templates.
    # return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
