from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/etnan', methods=['GET', 'POST'])
def etnan():
    val = request.form['searchval']
    return render_template('new.html',val=val)
if __name__ == '__main__':
    app.run(debug=True)
