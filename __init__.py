from flask import Flask, render_template, request, redirect
app = Flask(__name__)
import MySQLdb
import MySQLdb.cursors
import gc
gc.collect()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/my-link/')
def my_link():
    db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                        cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    diet = "3"
    cursor.execute("""SELECT * FROM Diets WHERE dietID='{0}'""".format(diet))
    rv = cursor.fetchall()
    db.close()
    return rv[0]['name']

@app.route('/home')
def home():
    return '<h1>Hello, Home!!!</h1>'

@app.route('/search', methods=['GET', 'POST'])
def search():
    #return '<h1>Hello, Search!!!</h1>'
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
def searchResults():
    return render_template('searchResults.html')

@app.route('/view/<int:rec_id>', methods=['GET', 'POST'])
def view(rec_id):
    rec_id = str(rec_id)
    db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                        cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Recipes WHERE recipeID='{0}'""".format(rec_id))
    rv = cursor.fetchone()
    db.close()
    if rv :
        return render_template('view_recipes.html', rec=rec_id, rv=rv)
    else:
        return "error"

@app.route('/edit/<int:rec_id>', methods=['GET', 'POST'])
def edit(rec_id):
    rec_id = str(rec_id)
    db = MySQLdb.connect(host="localhost", user="root", db="cuisineRecipes",
                        cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Recipes WHERE recipeID='{0}'""".format(rec_id))
    rv = cursor.fetchone()
    db.close()
    if rv :
        return render_template('edit_recipes.html', rec=rec_id, rv=rv)
    else:
        return "error"

@app.route('/add', methods=['GET', 'POST'])
def add():
    #
    return render_template('add_recipes.html')

if __name__ == '__main__':
    app.run(debug=True)

