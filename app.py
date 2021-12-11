from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'swertekapagnahulaanmo'

#index
@app.route('/')
def index():
    return render_template('index.html')

#about
@app.route('/about')
def about():
    return render_template('about.html')

#login
@app.route("/login", methods=["POST","GET"])
def login():
    return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h>"

#prediction
@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

if __name__ == '__main__':
    app.run(debug=True)
