from flask import Flask, render_template, request, redirect
#from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8

import requests
import pandas as pd

app_stock = Flask(__name__)

app_stock.vars = {}

app_stock.vars['color'] = {
    'Close': 'navy',
    'Adj. Close': 'orange',
    'Volume': 'green'
}

@app_stock.route('/')
def main():
    return redirect('/index')

@app_stock.route('/error-quandle')
def error_quandle():
    return render_template('error.html')

@app_stock.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app_stock.vars['ticker'] = request.form['ticker']
        #checked = request.form['features']
        #checked = request.form.getlist('features')  # list of checked
        app_stock.vars['features'] = request.form.getlist('features')

        # Pull stock data
        url = 'https://www.quandl.com/api/v3/datasets/WIKI/' + app_stock.vars['ticker'] + '/data.json'
        r = requests.get(url)
        if r.status_code == 404:
            return redirect('/error-quandle')
        else:
            data = r.json()['dataset_data']['data']
            cols = r.json()['dataset_data']['column_names']
            app_stock.vars['data'] = pd.DataFrame(data, columns=cols)
            #app_stock.vars['data'] = df[['Date'] + app_stock.vars['features']].head(5)
            return redirect('/graph')


@app_stock.route('/graph', methods=['GET'])
def graph():
    df = app_stock.vars['data']

    # Create a line plot from our data.
    p = figure(width=700, height=500, x_axis_type="datetime",
                title="Data from Quandle WIKI set")
    for category in app_stock.vars['features']:
        p.line(pd.to_datetime(df['Date']), df[category],
                color=app_stock.vars['color'][category], line_width=1,
                legend=app_stock.vars['ticker'] + ": " + category)

    p.legend.orientation = "top_right"

    # Configure resources to include BokehJS inline in the document.
    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw,
        css_raw=INLINE.css_raw,
        js_files=INLINE.js_files,
        css_files=INLINE.css_files,
    )

    script, div = components(p, INLINE)
    html = render_template(
        'graph.html',
        ticker=app_stock.vars['ticker'],
        plot_script=script, plot_div=div, plot_resources=plot_resources
    )
    return encode_utf8(html)



if __name__ == '__main__':
    app_stock.run(port=33507)
