from flask import Flask, render_template, url_for, redirect, request, session, Response
from flask_mysqldb import MySQL


app=Flask(__name__)

app.config['SECRET_KEY']= '3d6f45a5fc12445dbac2f59c3b6c7cb1'
app.config['MYSQL_HOST'] = 'your hostname'
app.config['MYSQL_USER']= 'your username'
app.config['MYSQL_PASSWORD']= 'your password'
app.config['MYSQL_DB']= 'the database you wish to access'
mysql= MySQL(app)

def createCSV(data):
    csv=""
    for row in data:
        string = str(row)
        csv=csv+(string[1:-1] + '\n')
    return csv



@app.route('/', methods=['GET','POST'])
def SQLquery():
    if request.method== "POST":
            form=request.form
            stateRequest=form['state']
            session['state']=stateRequest
    return render_template("SQLquery.html")

@app.route('/export')
def export():
    cur=mysql.connection.cursor()
    state=session.get('state')
    result_selection=cur.execute("SELECT * FROM Sbux WHERE State = '{}'".format(state))
    if result_selection>0:
        sbuxLocations=cur.fetchall()
        csv=createCSV(sbuxLocations)
    return Response(
    csv,
    mimetype="text/csv",
    headers={"Content-disposition":
    "attachment; filename={}Sbux.csv".format(state)})


app.run(debug=True, host='0.0.0.0', port= '8006')