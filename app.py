from flask import Flask, render_template, url_for, request
import sqlite3
from detect import Start
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('userlog.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            return render_template('userlog.html')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    if request.method == 'POST':
        image = request.form['img']
        PT = request.form['pt']
        if PT == 'bean.pt':
            path = 'static/test/bean/'+image
            ImageDisplay="http://127.0.0.1:5000/static/test/bean/"+image
        if PT == 'maize.pt':
            path = 'static/test/maize/'+image
            ImageDisplay="http://127.0.0.1:5000/static/test/maize/"+image
        if PT == 'rice.pt':
            path = 'static/test/rice/'+image
            ImageDisplay="http://127.0.0.1:5000/static/test/rice/"+image
        if PT == 'wheat.pt':
            path = 'static/test/wheat/'+image
            ImageDisplay="http://127.0.0.1:5000/static/test/wheat/"+image
        if PT == 'channa.pt':
            path = 'static/test/channa/'+image
            ImageDisplay="http://127.0.0.1:5000/static/test/channa/"+image
        Start(path, PT)
        import csv
        f = open('database.csv', 'r')
        reader = csv.reader(f)
        result = []
        for row in reader:
            result.append(row)
        f.close()
        print(result)
        return render_template('userlog.html', result=result, ImageDisplay=ImageDisplay, ImageDisplay1="http://127.0.0.1:5000/static/result/"+image)
    return render_template('userlog.html')

@app.route('/live', methods=['GET', 'POST'])
def live():
    if request.method == 'POST':
        PT = request.form['pt']
        import cv2
        vs = cv2.VideoCapture(0)
        while True:
            ret, frame = vs.read()
            if not ret:
                break
            cv2.imshow('stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite('static/frame.png', frame)
                vs.release()
                cv2.destroyAllWindows()
                break
        
        Start('static/frame.png', PT)
        print('pppppppppppppppppp')
        import csv
        f = open('database.csv', 'r')
        reader = csv.reader(f)
        result = []
        for row in reader:
            result.append(row)
        f.close()
        print(result)
        return render_template('userlog.html', result=result, ImageDisplay="http://127.0.0.1:5000/static/frame.png", ImageDisplay1="http://127.0.0.1:5000/static/result/frame.png")
    return render_template('userlog.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
