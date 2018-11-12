from flask import Flask, render_template, request, session, redirect, url_for, flash
import pymysql
import pandas
import matplotlib.pyplot as plt
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/>?@$'
# ----------------- SECTION FOR ADDING MENU ITEMS, UPLOADING IMAGES AND DISPLAYING IMAGES ON WEBPAGE ----------------

UPLOAD_FOLDER = 'C:\\Users\\Mary\\Documents\\1.PycharmProgams\\RestaurantWebsiteFlaskProject\\static\\testDirectory\\'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# this section has code that adds menu item to homepage using backend form
# adds a menu item into the database
@app.route('/additem', methods=['POST', 'GET'])
def additem():
    if request.method == 'POST':  # check if user posted something
        item = request.form['item']
        description = request.form['description']
        cost = request.form['cost']
        image = request.form['image']

        if item == "":
            # flash('Email is empty')
            return render_template('add-item.html', msg_item="*Item is empty")
        elif description == "":
            # flash('Name is empty')
            return render_template('add-item.html', msg_description="*Description is empty")
        elif cost == "":
            # flash('Message is empty')
            return render_template('add-item.html', msg_cost="*Cost is empty")
        elif image == "":
            # flash('Message is empty')
            return render_template('add-item.html', msg_image="*Image is empty")
        else:
            # save the three items to db
            # establish db connection
            con = pymysql.connect("localhost", "root", "", "sampledb")
            cursor = con.cursor()
            if description == 'meal':
                sql = "INSERT INTO meals_tbl(`item`,`description`,`cost`,`image`) VALUES(%s,%s,%s,%s)"
                try:
                    cursor.execute(sql, (item, description, cost, image))
                    con.commit()  # commit changes to the db
                    return render_template('add-item.html', msg="Uploaded!")
                except:
                    con.rollback()
                    return render_template('add-item.html', msg="Failed!")
            elif description == 'drink':
                sql = "INSERT INTO drinks_tbl(`item`,`description`,`cost`,`image`) VALUES(%s,%s,%s,%s)"
                try:
                    cursor.execute(sql, (item, description, cost, image))
                    con.commit()  # commit changes to the db
                    return render_template('add-item.html', msg="Uploaded!")
                except:
                    con.rollback()
                    return render_template('add-item.html', msg="Failed!")
            elif description == 'dessert':
                sql = "INSERT INTO dessert_tbl(`item`,`description`,`cost`,`image`) VALUES(%s,%s,%s,%s)"
                try:
                    cursor.execute(sql, (item, description, cost, image))
                    con.commit()  # commit changes to the db
                    return render_template('add-item.html', msg="Uploaded!")
                except:
                    con.rollback()
                    return render_template('add-item.html', msg="Failed!")
    else:
        return render_template('add-item.html')


# code for uploading images to folder named static/image.
# The path is stated in UPLOADED_FOLDER at the top of the page
@app.route('/imageUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'img-file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['img-file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploads'))

    return render_template('upload-image.html')


from flask import send_from_directory, session


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# displays all the images uploaded by the admin with their respective names.
# This makes it easier for them to add the name of the picture when they are adding a menu item
@app.route('/uploaded-images')
def uploads():
    pictures = os.listdir('static/testDirectory/')
    return render_template("menu-images.html", pics=pictures)


@app.route('/homepage')
def homepage():
    con = pymysql.connect("localhost", "root", "", "sampledb")

    cursor_1 = con.cursor()
    cursor_2 = con.cursor()
    cursor_3 = con.cursor()
    sql_meals = "SELECT * FROM `meals_tbl` ORDER BY `id`"
    sql_drinks = "SELECT * FROM `drinks_tbl` ORDER BY `id`"
    sql_dessert = "SELECT * FROM `dessert_tbl` ORDER BY `id`"
    # execute sql
    cursor_1.execute(sql_meals)
    cursor_2.execute(sql_drinks)
    cursor_3.execute(sql_dessert)

    rows_meals = cursor_1.fetchall()
    rows_drinks = cursor_2.fetchall()
    rows_dessert = cursor_3.fetchall()

    return render_template("homepage.html", mealsdata=rows_meals,
                           drinksdata=rows_drinks,
                           dessertdata=rows_dessert,
                           path_to_images='../static/testDirectory/')


@app.route('/delete-image/<pic>/', methods=['GET', 'POST'])
def delete_image(pic):
    if 'userkey' in session:

        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pic))
        return redirect(url_for('uploads'))

    elif 'userkey' not in session:
        return redirect('/login')
    else:
        return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
