from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import TMDB
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
    #templist = ['Film1', 'Film2']
    #temp2list = TMDB.movie_search("Hulk")
    #temp2list = TMDB.trending_media("movie", "day")
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
        return render_template("index.html", tasks=tasks) #temp2list=temp2list

    # render_template requires files to be placed in a folder called templates.
    # return render_template("index.html")

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error deleting the task.'

if __name__ == "__main__":
    app.run(debug=True)
