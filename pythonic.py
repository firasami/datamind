from flask import Flask, render_template, url_for

app = Flask(__name__)

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

if __name__=="__main__":
    app.run(debug=True)