import uuid
import pandas as pd
import glob, os

from flask import *
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/", methods=['GET'])
def get_tables():

    paths = []

    for f in glob.glob("./tmp/*.html"):
        file = f.replace(".html", "").replace("./tmp/", "")

        paths.append(f"/tables/{file}")

    return render_template(
        'list.html',
        paths=paths
    )

@app.route("/tables/<id>", methods=['GET'])
def get_tables_by_id(id):
    try:
        f = open(f"tmp/{id}.html", "r")
        content = f.read()
        f.close()

        return content
    except:
        template = render_template('404.html')
        return template

@app.route("/tables", methods=['POST'])
def create_tables():
    titles = []
    tables = []
    content = request.json

    for table in content['tables']:
        columns = table['data'][0].keys()
        values = []

        titles.append(table['title'])

        for elm in table['data']:
            values.append(list(elm.values()))

        classes = ""

        if len(tables) % 2 == 0:
            classes += "even"
        else:
            classes += "odd"

        tables.append(
            pd.DataFrame(values, columns=columns).to_html(classes=classes)
        )

    template = render_template(
        'view.html',
        tables=tables,
        titles=titles
    )

    uuidOne = uuid.uuid1()

    f = open(f"tmp/{uuidOne}.html", "w")
    f.write(template)
    f.close()

    return template

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)