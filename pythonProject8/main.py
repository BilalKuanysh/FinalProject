from flask import Flask, request, render_template
import requests
import psycopg2
hostname = 'localhost'
database = '1gate'
username = 'postgres'
pwd = 'mama1967'
port_id = 5432

conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id
)
cur = conn.cursor()

create_script = ''' CREATE TABLE IF NOT EXISTS register (
temp varchar(40)  NOT NULL,
feels_like varchar(50),
weather varchar(50),
location varchar(50)
) '''
cur.execute(create_script)
conn.commit()

def weather1(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()
print(weather1('95129', 'c83120d4614a77ca16f268781f559467'))
app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def weather_dashboard2():
    if request.method == "POST":
        zip  = request.form['zipCode']

        api_key = 'c83120d4614a77ca16f268781f559467'
        data = weather1(zip, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
        weather = data["weather"][0]['main']
        location = data['name']
        insert_into = 'INSERT INTO register VALUES (%s, %s, %s, %s)'
        insert_values = (temp, feels_like, weather, location)
        cur.execute(insert_into, insert_values)
        conn.commit()
        return render_template('result.html', temp=temp, feels_like=feels_like, weather=weather,location=location)

if __name__ == "__main__":
    app.run(debug=True)