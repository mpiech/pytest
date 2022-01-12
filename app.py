import os
from flask import Flask, render_template, request
from waitress import serve
import pymongo
import psycopg2
import pandas as pd

app = Flask(__name__, static_url_path='')

### Crunchy Bridge

cbhost = os.environ['PGHOST']
cbusr = os.environ['PGUSER']
cbpwd = os.environ['PGPASSWORD']
cbdb = os.environ['PGDB']

cbconn = psycopg2.connect (
    host=cbhost, 
    database=cbdb,
    user=cbusr,
    password=cbpwd
    )

def create_pandas_table(sql_query):
    table = pd.read_sql_query(sql_query, cbconn)
    return table

### Mongo Atlas

atlashost = os.environ['ATLAS_HOST']
atlasusr = os.environ['ATLAS_USERNAME']
atlaspwd = os.environ['ATLAS_PASSWORD']
atlasdb = os.environ['ATLAS_DB']

mngclient = pymongo.MongoClient("mongodb+srv://" +
                                atlasusr + ":" +
                                atlaspwd + "@" +
                                atlashost + "/" +
                                atlasdb +
                                "?retryWrites=true&w=majority")
db = mngclient.mystrk
coll = db.tracks
trk = coll.find_one()

### Google Maps

gmapskey = os.environ['GMAPS_KEY']

### Flask Routes

@app.route("/")
def hanndler_get_index():
    # return app.send_static_file('index.html')
    return render_template('index.html.jinja',
                           name=trk,
                           googlemapskey=gmapskey)

@app.route("/test")
def hanndler_get_test():
    return trk

@app.route("/resdates", methods=["GET"])
def handler_get_resdates():
    start = str(request.args.get('start', type=str))
    end = request.args.get('end')
#    sqlstr = "SELECT DISTINCT res_date FROM reservations WHERE \
#    CAST (res_date AS TIMESTAMP) >= \
#    CAST (" + start + " AS TIMESTAMP)"
    sqlstr = "SELECT DISTINCT res_date FROM reservations WHERE \
    CAST (res_date AS TIMESTAMP) >= \
    CAST ('2022-01-01' AS TIMESTAMP)"
    fmt = '%Y%m%d %H:%M:%S'
    resdates = pd.read_sql_query(sqlstr,
                                 cbconn,
                                 parse_dates={'res_date':fmt})
    resarr = []
    resarr.append({'title': 'Mys Rsvd', 'start': '2022-01-23'})
    resarr.append({'title': 'Mys Rsvd', 'start': '2022-01-24'})
    resstr=','.join(map(str,resarr))
    return resstr


# Waitress HTTP server

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
