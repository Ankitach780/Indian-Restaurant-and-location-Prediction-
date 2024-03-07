from flask import Flask, render_template, request
from sklearn import preprocessing
import joblib
model = joblib.load('restaurant.pkl')
df1=joblib.load('values.pkl')   
label_encoder=preprocessing.LabelEncoder()
label_encoder.fit(df1['about'])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

def decode_predicted_value(predicted_value):
    decoded_about = label_encoder.inverse_transform([predicted_value])[0]
    return decoded_about

@app.route("/search", methods=['GET','POST'])
def search():
    res=None
    if request.method == 'POST':
        rating = float(request.form['rating'])
        average_price = int(request.form['avg_price'])
        average_delivery_time = int(request.form['avg_delivery_time'])
        south_indian = int(request.form['south_indian_or_not'])
        north_indian = int(request.form['north_indian_or_not'])
        fast_food = int(request.form['fast_food_or_not'])
        street_food = int(request.form['street_food'])
        biryani = int(request.form['biryani_or_not'])
        bakery = int(request.form['bakery_or_not'])

        prediction = model.predict([[rating, average_price, average_delivery_time, south_indian, north_indian, fast_food, street_food, biryani, bakery]])
        predicted_about = decode_predicted_value(prediction)
        res = {
            'prediction': predicted_about
        }
    return render_template('search.html',Restaurants=res)

@app.route('/contact',methods=['GET'])   
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
