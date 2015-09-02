from flask import Flask, render_template, request, redirect

app_stock = Flask(__name__)

app_stock.vars = {}

@app_stock.route('/')
def main():
    return redirect('/index')

@app_stock.route('/index', method=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app_stock.vars['ticker'] = request.form['ticker']
        print request.form['features']
        app_stock.vars['features'] = request.form['features']

    return "POST method!"

if __name__ == '__main__':
  app_stock.run(port=33507)
