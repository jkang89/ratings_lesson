from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    return render_template("user_list.html")

@app.route("/", methods=["POST"])
def process_login():
    emailAddr = request.form.get("emailaddress")
    password = request.form.get("password")

    user_id = model.authenticate(emailAddr, password)
    if user_id != None:
        flash("User authenticated!")
        session['userId'] = user_id
    else:
        flash("Login information is incorrect.")
        return redirect(url_for("index"))
    
    return redirect("/user/%s"%user_id)

@app.route("/allusers") 
#list of all the users
def see_all_users():
    user_list = model.session.query(model.User).all()
    return render_template("all_users.html", users=user_list)

@app.route("/user/<user_id>")
#click on user and see the list of movies they've rated as well as the ratings
def view_user(user_id):
    #the_user_id = model.session.query(model.User).get(user_id)
    # movie_ratings = model.session.query(model.Ratings).all()
    user = model.session.query(model.User).get(user_id)
    rating_list = model.session.query(model.Ratings).all()
    return render_template("user_profile.html", user=user, ratings=rating_list)

@app.route("/movie/<movie_id>")
#click on user and see the list of movies they've rated as well as the ratings
def movie_list(movie_id):
    movie = model.session.query(model.Ratings).get(movie_id)
    #user_id = model.session.query(model.Ratings).get(model.Ratings.users.id)
    #userId = session.get("userId")
    #username = model.session.query(model.User).get(userId)
    rating = model.session.query(model.Ratings).filter(model.Ratings.movie.name).all()
    return render_template("movie.html", movie=movie, ratings=rating) #username=username.email)


#get id out of users to apply to ratings to get ratings to apply to movies to get titles



"""
@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    user_id = model.get_user_by_name(username)
    posts = model.get_wall_posts(user_id)
    return render_template("wall.html", the_posts=posts, username=username)
"""
@app.route("/newrating") 
#should be able to when logged in, add or update personal rating for said movie  


@app.route("/register", methods = ["GET"])
def register():
    return render_template("register.html")

@app.route("/register", methods = ["POST"])
def create_user():
    email = request.form.get("emailaddress")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    user = model.User(email=email, password=password, age=age, zipcode=zipcode)
    model.session.add(user)
    model.session.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)
