import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory,flash
import play_game
import read_data
import make_json
import mongo
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = "custom"
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.debug = True
app.secret_key = "Nothing"
FACT = 'The German government decided to ally with the Austro-Hungarian Empire.'
OG = 'The German government decided to ally with the Austro-Hungarian Empire.'
F = ""
O = ""
CURR = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/custom/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'file' not in request.files:
            
            flash('No file part')
            return redirect('/custom')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            
            flash('No selected file')
            return redirect('/custom')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            make_json.make(filename.split('.')[0], custom=True)
            
            
    return redirect('custom-game')


@app.route("/")
def HomePage():
    if "email" in session:
        check = True
    else:
        check = False
    return render_template('Index.html', check=check)

@app.route("/login")
def login():
    if "email" in session:
        return redirect(url_for("custom"))
    return render_template('Login.html')

# @app.route("/Dashboard")
# def Dashboard():
#     return "dashboard"

@app.route('/login_action', methods=['POST'])
def login_action():

    email = request.form['email']
    password = request.form['password']
    check, role = mongo.Login(email, password)
    if check:
        print("User exists")
        session['email'] = email
        if role == "Teacher":
            session['game'] = "True"
            print("game editing")
        print("session started")
        print(role)
        return "Success"
    else:
        print("User Does not exists")

        return {"error": "User does not exists"}


@app.route('/sign_action', methods=['POST'])
def sign_action():

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    Role = request.form['Role']
    print(Role)
    if mongo.Register(email, name, password,Role):
        print("User Account Created")
        return "User Account Created"
    else:
        print("Error Occured")
        return "Error Occured"

@app.route("/play-ww1")
def play_ww1():
    return render_template('W1.html') 

@app.route("/out")
def out():
    session.clear()
    return render_template('Index.html',check=False) 

@app.route("/play-ww2")
def play_ww2():
    return render_template('W2.html') 

@app.route("/custom")
def custom():
    if "game" in session:
        print("if entered")
        return render_template('custom.html')
    if "email" in session : return render_template("custom.html",check=True)
    return render_template("Index.html",check=False)

@app.route("/custom-game")
def cust_game():
    lst = os.listdir('custom_data')
    st = set()
    for i in lst:
        t = i.split('_')[2:]
        st.add('_'.join(t))
    print(st)
    return render_template('custom_game.html', val=list(st)) 


@app.route("/act",methods=["POST"])
def act():
    global CURR
    CURR = None
    global FACT
    tp = read_data.get_data('ww1_f')
    gd = tp['game_data']
    cd = tp['content_data']
    number = int(request.form['number'])
    data = play_game.play(number, 'ww1_f')
    # print(data)
    if number == 6  :
        FACT = OG
    if "options" not in data:
        FACT = OG
        print(data)
        return data
    ops = data['options']
    tdct = {}
    counter = ['y','n']
    for i in ops:
        tdct[counter[0]] = {
            'val': cd[i],
            'next': ops[i]['next'],
            'more':cd[ops[i]['more']]
        }
        del counter[0]
    res = {
        'question':cd[data['question']],
        'fact':FACT,
        'chap':cd[data['chapter']],
        'options':tdct
    }
    FACT = cd[data['fact']]
    # print(res)
   # ans = {"question":"Second"}
    return res

@app.route('/play_custom/<name>')
def my_view_func(name):
    global CURR
    CURR = name 
    tp = read_data.get_data(name, custom=True)
    gd = tp['game_data']
    cd = tp['content_data']
    res = play_game.play(1, name, custom=True)
    ops = res['options']
    tdct = {}
    counter = ['y','n']
    for i in ops:
        tdct[counter[0]] = {
            'val': cd[i],
            'next': ops[i]['next'],
            'more':cd[ops[i]['more']]
        }
        del counter[0]
    global F,O
    F,O = [cd[res['fact']]]*2
    res = {
        'question':cd[res['question']],
        'fact':None,
        'chap':cd[res['chapter']],
        'options':tdct
    }
    print(res)
   # ans = {"question":"Second"}
    res['name'] = name
    return render_template('play_custom.html', val=res)


@app.route("/cust",methods=["POST"])
def cust():
    global F
    tp = read_data.get_data(CURR, custom=True)
    gd = tp['game_data']
    cd = tp['content_data']
    number = int(request.form['number'])
    data = play_game.play(number, CURR, custom=True)
    print(data)
    if number == 6  :
        F = O
    if "options" not in data:
        F = O
        return data
    ops = data['options']
    tdct = {}
    counter = ['y','n']
    for i in ops:
        tdct[counter[0]] = {
            'val': cd[i],
            'next': ops[i]['next'],
            'more':cd[ops[i]['more']]
        }
        del counter[0]
    res = {
        'question':cd[data['question']],
        'fact':F,
        'chap':cd[data['chapter']],
        'options':tdct
    }
    F = cd[data['fact']]
    print(res)
   # ans = {"question":"Second"}
    return res

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run()
