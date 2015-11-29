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
    return render_template('search.html', methods=['GET', 'POST'])

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
    return render_template('add_recipes.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == "GET":
        if request.args['sub'] == "submit":
            nam = request.args['name']
            die = request.args["diet"]
            des = request.args["desc"]
            ing = request.args["ingr"]
            ins = request.args["inst"]
            db = MySQLdb.Connection(host="localhost", user="root", db="cuisineRecipes",
                cursorclass=MySQLdb.cursors.DictCursor)
            cursor = db.cursor()
            # check if diet exists
            cursor.execute("""SELECT * FROM Diets WHERE name='{0}'""".format(die))
            rv = cursor.fetchone()
            if rv is None:
                cursor.execute("""INSERT INTO Diets(name) VALUES('{0}')""".format(die))
                db.commit()
            # insertion
            cursor.execute("""INSERT INTO 
                Recipes(name, diet, description, ingredients, instructions) 
                VALUES('{0}', '{1}', '{2}', '{3}', '{4}')"""
                .format(nam, die, des, ing, ins))
            db.commit()
            # go to view of new entry
            cursor.execute("""SELECT * FROM Recipes WHERE instructions='{0}'""".format(ins))
            rv = cursor.fetchone()
            rec_id = rv["recipeID"]
            db.close()
            return render_template('view_recipes.html', rec=rec_id, rv=rv)
        else:
            return render_template('index.html')
    else:
        return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)

