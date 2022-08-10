from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import TMDB

print("S1_app.py - Imports done, start code.")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print("S2_app.py - Class Todo.")


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

    def __rep__(self):
        return '<Task %r>' % self.id


# db.create_all()
# exit()

print("S3_app.py - Run app route and def home().")


@app.route('/', methods=['POST', 'GET'])
def home():
    # templist = ['Film1', 'Film2']
    # temp2list = TMDB.movie_search("Hulk")
    temp2list = TMDB.trending_media("movie", "day")
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
        return render_template("index.html", tasks=tasks, temp2list=temp2list)

    # render_template requires files to be placed in a folder called templates.
    # return render_template("index.html")


print("S4_app.py - Run app route delete.")


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error deleting the task.'

@app.route('/search')
def media_search():
    title = request.args.get('capture_search_results')
    print(title)
    search_results = TMDB.movie_search(title)
    number_of_results = len(search_results)
    return render_template("search_results.html", search_results=search_results, number_of_results=number_of_results)


if __name__ == "__main__":
    app.run(debug=True)
