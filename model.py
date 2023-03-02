from flask import Flask, render_template, redirect, url_for, request, session
import pickle

app = Flask(__name__)
app.secret_key = "GlamourKey"
model = pickle.load(open("model.pkl","rb"))

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        session["username"] = username
        session["password"] = password
        return redirect(url_for("home"))
    else:
        if "username" in session:
            return redirect(url_for("home", usr=session["username"]))
        
        return render_template("Login.html")

@app.route('/home')
def home():
    if "username" in session:
        username = session["username"]
        return render_template('Home.html', usr=username)
    else:
        return redirect(url_for("login"))

@app.route('/form', methods=['POST','GET'])
def form():
    if request.method == "POST":
        p_cs = 0
        p_it = 0
        sx_m = 0
        sx_f = 0
        pcs_t = 0
        pcs_a = 0
        pcs_d = 0
        pcs_w = 0
        int_y = 0
        int_n = 0
        exc_y = 0
        exc_n = 0
        err_y = 0
        err_n = 0
        tf_age = request.form["tf_age"]
        dd_sx = request.form["dd_sx"]
        if dd_sx == "Male":
            sx_m = 1
        else: 
            sx_f = 1
        dd_program = request.form["dd_program"]
        if dd_program == "CS":
            p_cs = 1
        else: 
            p_it = 1
        dd_yl = request.form["dd_yl"]
        dd_pcs = request.form["dd_pcs"]
        if dd_pcs == "Living Together":
            pcs_t = 1
        elif dd_pcs == "Apart":
            pcs_a = 1
        elif dd_pcs == "Deceased":
            pcs_d = 1
        else:
            pcs_w = 1
        dd_fe = request.form["dd_fe"]
        dd_me = request.form["dd_me"]
        dd_fi = request.form["dd_fi"]
        dd_ia = request.form["dd_ia"]
        if dd_ia == "Yes":
            int_y = 1
        else:
            int_n = 1
        dd_tt = request.form["dd_tt"]
        dd_st = request.form["dd_st"]
        dd_ft = request.form["dd_ft"]
        dd_ec = request.form["dd_ec"]
        if dd_ec == "Yes":
            exc_y = 1
        else:
            exc_n = 1
        dd_fr = request.form["dd_fr"]
        dd_rr = request.form["dd_rr"]
        if dd_rr == "Yes":
            err_y = 1
        else:
            err_n = 1
        dd_go = request.form["dd_go"]
        dd_ac = request.form["dd_ac"]
        dd_hs = request.form["dd_hs"]
        dd_ts = request.form["dd_ts"]

        prediction = model.predict([[int(dd_yl), int(dd_fe), int(dd_me), int(dd_fi), 
                                     int(dd_tt), int(dd_ft), int(dd_go), int(dd_hs), 
                                     int(dd_ts), int(sx_f), int(sx_m), int(pcs_d), 
                                     int(pcs_t), int(err_n), int(err_y)]])
        
        print(int(tf_age), int(dd_yl), int(dd_fe), int(dd_me),
              int(dd_fi), int(dd_fr), int(dd_tt), int(dd_st),
              int(dd_ft), int(dd_go), int(dd_ac), int(dd_hs), 
              int(dd_ts), int(sx_f), int(sx_m), int(p_cs),
              int(p_it), int(pcs_a), int(pcs_d), int(pcs_t), 
              int(pcs_w), int(int_n), int(int_y), int(exc_n), 
              int(exc_y), int(err_n), int(err_y))
        print(prediction)
        if int(prediction) == 1:
            statement = "You will have a scholarship next Semester!"
        elif int(prediction) == 0:
            statement = "You will not have a scholarship next Semester!"
        else:
            statement = "Model Error"
        return redirect(url_for('result', rlt=statement))
    
    return render_template('Fill-Up-Form.html')

@app.route("/logs")
def logs():
    return render_template('Logs.html')

@app.route("/<rlt>")
def result(rlt):
    return render_template('result.html', rlt=rlt)

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=8000, debug=True)