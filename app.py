from  flask import Flask, render_template, request
import requests
from datetime import datetime
import mysql.connector

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="weather_app"
)
cursor=conn.cursor()
print("my sql connect successfully")

# weather_data = cursor.fetchall()
# for data in weather_data:
#     print(data)
# cursor=conn.commit()

app = Flask(__name__)
API_KEY = '5a88aa2a8d0c5ead72d1bbea617b83ce'
@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    background="sunny.jpg"
     
    error = None
    if request.method == 'POST':
        citys = request.form['city']
        url = f'http://api.openweathermap.org/data/2.5/weather?q={citys}&appid={API_KEY}&units=metric'
        print(url)
        response = requests.get(url)
        data = response.json()
        if data.get("cod")==200:
           
            weather={
                "city":data["name"],
                "temp":data["main"]["temp"],
                "humidity":data["main"]["humidity"],
                "condition":data["weather"][0]["main"],
                "icon":data["weather"][0]["icon"],
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            cursor.execute(
            "insert into weather_history(city,temperature,searched_at) values (%s,%s,now())",(weather["city"],weather["temp"])
)
            conn.commit()
            if weather["condition"]=="Rain":
                background="rain.jpg"
            elif weather["condition"]=="Clouds":
                background="cloud.jpg"
            elif weather["condition"]=="Clear":
                background="sunny.jpg"
        else:
            error="City not found. Please try again."
    return render_template('index.html', weather=weather, error=error,background=background, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
if __name__ == '__main__':
    app.run(debug=True)
