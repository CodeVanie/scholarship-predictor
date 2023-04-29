from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:codevanie123@localhost/scholarship_predictor?charset=utf8mb4")

def load_users_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        users = []
        for row in result.all():
            users.append(row)
            
        return users
    
def load_user_from_db(username):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE Username = '" + username + "'"))
        user = []
        for row in result.all():
            user.append(row)
            
        return user
    
def update_user_from_db(userid, name, user, email, newp):
    with engine.connect() as conn:
        conn.execute(text("UPDATE users SET Fullname = '" + name + "', Username = '" + user + "', Email = '" + email + "', Password = '" + newp + "' WHERE Id = " + str(userid)))
        
        conn.commit()

def load_records_from_db(userid):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users_predict_records WHERE UserId = " + str(userid)))
        records = []
        for row in result.all():
            records.append(row)
            
        return records
    
def load_record_from_db(recid):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users_predict_records WHERE Id = " + str(recid)))
        record = []
        for row in result.all():
            record.append(row)
            
        return record
    
def load_highest_record_id(userid):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT MAX(Id) FROM users_predict_records WHERE userid = " + str(userid)))
        maxid = []
        for row in result.all():
            maxid.append(row)
            
        for i in maxid:
            recid = i[0]
            
        return recid
    
def reg_user_to_db(username, fulln, email, password):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO users (Username, Fullname, Email, Password) VALUES ('"+ username + "', '" + fulln + "', '" + email + "', '" + password + "')"))
        print("User " + username + " successfully added.")

        conn.commit()

def add_pred_record_to_db(userid, result, tf_age, yearlevel, fathereducation, mothereducation, familyincome, familyrelation, traveltime, studytime, freetime, goingout, healthstatus, alcohol, typeofscholarship, gendertype, programcourse, parentcohabitationstatus, homeinternetaccess, extracurricularactivities, engagementromaticrelationship, accuracy, dateandtime):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO users_predict_records (UserId, Result, Age, YearLevel, FatherEducation, MotherEducation, FamilyIncome, FamilyRelation, TravelTime, StudyTime, FreeTime, GoingOut, HealthStatus, AlcoholCons, ScholarType, Gender, Course, CohabStatus, InternetAcc, ExtraCurr, RomanticRel, Accuracy, DateSubmitted) VALUES ("+ str(userid) + ", '" + result + "', " + str(tf_age) + ", '" + yearlevel + "', '" + fathereducation + "', '" + mothereducation + "', '" + familyincome + "', '" + familyrelation + "', '" + traveltime + "', '" + studytime + "', '" + freetime + "', '" + goingout + "', '" + healthstatus + "', '" + alcohol + "', '" + typeofscholarship + "', '" + gendertype + "', '" + programcourse + "', '" + parentcohabitationstatus + "', '" + homeinternetaccess + "', '" + extracurricularactivities + "', '" + engagementromaticrelationship + "', '" + accuracy + "', '" + str(dateandtime) + "')"))
        print("Prediction record successfully added.")

        conn.commit()