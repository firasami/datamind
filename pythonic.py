from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config[
    "SECRET_KEY"
] = "518b27555b2c665ab650263a6f5f7ef46f3671072acb21c14924bd222c9b0236"


News = [{
    'title': 'news 1',
    'author': 'firas',
    'backgr' : 'pic1.jpg'  ,
},
{ 'title': 'news 2',
  'author': 'firas',
  'backgr' : 'pic4.jpg'  ,
    
},
{ 'title': 'news 3',
   'author': 'firas',
   'backgr' : 'pic3.webp'  ,
},
]

courses = [
{
        'name': 'Python',
        'icon': 'python.jpg',
        'description': 'Python is a popular, high-level programming language known for its simplicity and readability'
    },

    {
        'name': 'Data Analysis',
        'icon': 'dataan.jpg',
        'description': 'Data analyst who collects and analyzes data in order to turn it into meaningful information that companies can use to improve and grow.'
    },

    {
        'name': 'Machine Learning',
        'icon': 'machine.jpg',
        'description': 'Machine learning is the process of using mathematical models of data to help a computer learn without direct instruction. '
    },
     {
        'name': 'Deep Learning',
        'icon': 'deep.jpg',
        'description': 'Deep learning is a branch of machine learning that is made up of a neural network with three or more layers'
    },
     {
        'name': 'Data Structure',
        'icon': 'datast.jpg',
        'description': 'Data structure is a data organization, and storage format that is usually chosen for efficient access to data'
    },
        {
        'name': 'Tips & Tricks',
        'icon': 'idea.png',
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!'
    },

]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', News=News, courses=courses)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (
            form.email.data == "firasamin526@gmail.com"
            and form.password.data == "PASS!!word123"
        ):
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)



if __name__=="__main__":
    app.run(debug=True)