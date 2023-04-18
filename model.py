from flask import Flask, render_template, redirect, url_for, request, session
import pickle
import datetime

app = Flask(__name__)
app.secret_key = "GlamourKey"
model = pickle.load(open("model.pkl","rb"))
rlt = "none"

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
        global statement
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

        prediction = model.predict([[int(dd_tt), int(dd_ts), int(sx_f), int(sx_m), 
                                     int(p_cs), int(p_it), int(pcs_a), int(int_n), 
                                     int(err_n), int(err_y)]])
        
        print(int(tf_age), int(dd_yl), int(dd_fe), int(dd_me),
              int(dd_fi), int(dd_fr), int(dd_tt), int(dd_st),
              int(dd_ft), int(dd_go), int(dd_ac), int(dd_hs), 
              int(dd_ts), int(sx_f), int(sx_m), int(p_cs),
              int(p_it), int(pcs_a), int(pcs_d), int(pcs_t), 
              int(pcs_w), int(int_n), int(int_y), int(exc_n), 
              int(exc_y), int(err_n), int(err_y))

        print(prediction)
        # print(int(dd_yl), int(dd_fe), int(dd_me), int(dd_fi), 
        #       int(dd_tt), int(dd_ft), int(dd_go), int(dd_hs), 
        #       int(dd_ts), int(sx_f), int(sx_m), int(pcs_d), 
        #       int(pcs_t), int(err_n), int(err_y))
        print(int(dd_tt), int(dd_ts), int(sx_f), int(sx_m), 
              int(p_cs), int(p_it), int(pcs_a), int(int_n), 
              int(err_n), int(err_y))

        if int(prediction) == 1:
            global statement 
            statement = "You will have a scholarship next Semester!"
        elif int(prediction) == 0:
            statement = "You will not have a scholarship next Semester!"
        else:
            statement = "Model Error"

        yearlevel = ""
        fathereducation= ""
        mothereducation = ""
        familyincome = ""
        traveltime = ""
        studytime = ""
        freetime = ""
        goingout = ""
        alcohol = ""
        healthstatus = ""
        typeofscholarship = ""
        gendertype = ""
        programcourse = ""
        parentcohabitationstatus = ""
        homeinternetaccess = ""
        engagementromaticrelationship = ""
        now = datetime.datetime.now()

        #Year Level
        if int(dd_yl) == 1:
            yearlevel = "1st Year"
        elif int(dd_yl) == 2:
            yearlevel = "2nd Year"
        elif int(dd_yl) == 3:
            yearlevel = "3rd Year"
        elif int(dd_yl) == 4:
            yearlevel = "4th Year"

        #Father Education
        if int(dd_fe) == 1:
            fathereducation = "Primary Education"
        elif int(dd_fe) == 2:
            fathereducation = "Secondary Education"
        elif int(dd_fe) == 3:
            fathereducation = "Undergraduate"
        elif int(dd_fe) == 4:
            fathereducation = "Graduate"

        #Mother Education
        if int(dd_me) == 1:
            mothereducation = "Primary Education"
        elif int(dd_me) == 2:
            mothereducation = "Secondary Education"
        elif int(dd_me) == 3:
            mothereducation = "Undergraduate"
        elif int(dd_me) == 4:
            mothereducation = "Graduate"

        #Family Income
        if int(dd_fi) == 1:
            familyincome = "Less than 12000"
        elif int(dd_fi) == 2:
            familyincome = "12000 - 25000"
        elif int(dd_fi) == 3:
            familyincome = "40000 - 50000"
        elif int(dd_fi) == 4:
            familyincome = "More than 50000"
        
        #Family Relationship
        if int(dd_fr) == 1:
            familyrelation = "1"
        elif int(dd_fr) == 2:
            familyrelation = "2"
        elif int(dd_fr) == 3:
            familyrelation = "3"
        elif int(dd_fr) == 4:
            familyrelation = "4"
        elif int(dd_fr) == 5:
            familyrelation = "5"

        #School Travel time
        if int(dd_tt) == 1:
            traveltime = "Less than 15 mins."
        elif int(dd_tt) == 2:
            traveltime = "15 to 30 mins."
        elif int(dd_tt) == 3:
            traveltime = "30 mins to 1 hour"
        elif int(dd_tt) == 4:
            traveltime = "More than one hour"

        #Study Time
        if int(dd_st) == 1:
            studytime = "Less than 2 hours."
        elif int(dd_st) == 2:
            studytime = "2 to 5 hours."
        elif int(dd_st) == 3:
            studytime = "5 to 10 hours."
        elif int(dd_st) == 4:
            studytime = "More than ten hours."
        
        #Free Time
        if int(dd_ft) == 1:
            freetime = "1"
        elif int(dd_ft) == 2:
            freetime = "2"
        elif int(dd_ft) == 3:
            freetime = "3"
        elif int(dd_ft) == 4:
            freetime = "4"
        elif int(dd_ft) == 5:
            freetime = "5"

        #Going out with Friend
        if int(dd_go) == 1:
            goingout = "1"
        elif int(dd_go) == 2:
            goingout = "2"
        elif int(dd_go) == 3:
            goingout = "3"
        elif int(dd_go) == 4:
            goingout = "4"
        elif int(dd_go) == 5:
            goingout = "5"

        #Alcohol Consumption
        if int(dd_ac) == 0:
            alcohol = "0"
        elif int(dd_ac) == 1:
            alcohol = "1"
        elif int(dd_ac) == 2:
            alcohol = "2"
        elif int(dd_ac) == 3:
            alcohol = "3"
        elif int(dd_ac) == 4:
            alcohol = "4"
        elif int(dd_ac) == 5:
            alcohol = "5"

        #Health Status
        if int(dd_hs) == 1:
            healthstatus = "1"
        elif int(dd_hs) == 2:
            healthstatus = "2"
        elif int(dd_hs) == 3:
            healthstatus = "3"
        elif int(dd_hs) == 4:
            healthstatus = "4"
        elif int(dd_hs) == 5:
            healthstatus = "5"

        #Type of Scholarship
        if int(dd_ts) == 1:
            typeofscholarship = "With High Honors"
        elif int(dd_ts) == 2:
            typeofscholarship = "With Highest Honors"
        elif int(dd_ts) == 3:
            typeofscholarship = "Dean's lister"
        elif int(dd_ts) == 4:
            typeofscholarship = "VPAA lister"
        elif int(dd_ts) == 5:
            typeofscholarship = "President's lister"
        
        #Gender Type
        if int(sx_m) == 1:
            gendertype = "Male"
        else:
            gendertype = "Female"
        
        #Program
        if int(p_cs) == 1:
            programcourse = "CS"
        else:
            programcourse = "IT"

        #parentcohabitationstatus
        if int(pcs_t) or dd_pcs == 1:
            parentcohabitationstatus = "Living Together"
        elif int(pcs_a) or dd_pcs == 2:
            parentcohabitationstatus = "Apart"
        elif int(pcs_d) or dd_pcs == 3:
            parentcohabitationstatus = "Deceased"
        elif int(pcs_w) or dd_pcs == 4:
            parentcohabitationstatus = "Widowed"

        #Home Internet Access
        if int(int_y) == 1:
            homeinternetaccess = "Yes"
        else:
            homeinternetaccess = "No"

        #Extra Curricular Activities
        if int(exc_y) == 1:
            extracurricularactivities = "Yes"
        else:
            extracurricularactivities = "No"

        #Engagement to Romantic Relationship
        if int(err_y) == 1:
            engagementromaticrelationship = "Yes"
        else:
            engagementromaticrelationship = "No"

        #Date and Time
        print("Current date and time:")
        print(now.strftime("%Y-%m-%d %H:%M:%S"))








        print(statement)
        print(parentcohabitationstatus)
        return render_template('htmltopdf.html', rlt=statement, age=tf_age, 
                               yrl=yearlevel, dad=fathereducation, mom=mothereducation, 
                               income=familyincome, relation=familyrelation, tt=traveltime, study=studytime, 
                               free=freetime, out=goingout, health=healthstatus, al=alcohol, scholar=typeofscholarship,
                               gender=gendertype, program=programcourse, parent=parentcohabitationstatus, internet=homeinternetaccess,
                               extra=extracurricularactivities, relationship=engagementromaticrelationship, date=now.strftime("%Y-%m-%d %H:%M:%S"))
    
    return render_template('Fill-Up-Form.html', usr=session["username"])

@app.route("/logs")
def logs():
    return render_template('Logs.html', usr=session["username"])

@app.route("/<rlt>")
def result(rlt):
    return render_template('Fill-Up-Form.html', rlt=rlt, usr=session["username"])

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=8000, debug=True)