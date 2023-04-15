from database import render_template,request,flash,redirect,make_response,app,Do,Users,db
import datetime

app.config['SECRET_KEY']='EGRGTHTH'
db.create_all()

@app.route('/',methods=['GET','POST'])
def home():
     return render_template("index.html",does=Do.query.all(),items=len(Do.query.all()),user=request.cookies.get('user'))

@app.route("/login",methods=['GET', 'POST'])
def login():
   if request.method=='POST':
      Found=False
      for user in Users.query.all():
           if request.form.get('username') == user.username and request.form.get('password') == user.password:
            Found=True
            flash("login successfully", "success")
            response=make_response(redirect('/'))
            response.set_cookie("user",request.form.get('username'))
            return response

      if Found==False:
         return redirect("/login")
         flash("username or password invalid", "danger")
   else:
      return render_template("login.html")

@app.route("/register",methods=['GET', 'POST'])
def register():
   if request.method=='POST':
      Found=False
      for user in Users.query.all():
           if request.form.get('username') == user.username and request.form.get('password') == user.password:
              Found=True
              return redirect('/register')

      if Found==False:
          if request.form.get("password")==request.form.get("re_password"):
              user = Users(username=request.form.get('username'), password=request.form.get('password'))
              db.session.add(user)
              db.session.commit()
              flash("registered successfully", "success")
              return redirect("/login")
          else:
              return redirect("/register")
   else:
      return render_template("register.html",user=request.cookies.get('user'))

@app.route("/logout")
def logout():
    response=make_response(redirect('/login'))
    response.delete_cookie('user')
    return response

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=="POST":
        found=False
        for do in Do.query.all():
            if request.form.get("topic")==do.topic:
                found = True
                flash("this topic exist","warning")
                return redirect("/add")
        if found==False:
            date_of_register = datetime.datetime.now()
            topic = request.form.get("topic")
            date = request.form.get("date")
            time = request.form.get("time")
            description = request.form.get("description")
            do=Do(topic=topic,date=date,time=time,description=description,date_of_register=date_of_register,user=request.cookies.get('user'))
            db.session.add(do)
            db.session.commit()
            flash("topic added successfully in your list.","success")
            return redirect("/")
    else:
        return render_template("add.html",user=request.cookies.get('user'))

@app.route('/show_details/<int:do_id>',methods=['GET','POST'])
def show_details(do_id):
    do = Do.query.get(do_id)
    return render_template("show.html",do=do,user=request.cookies.get('user'))

@app.route('/delete/<int:do_id>',methods=['GET','POST'])
def delete(do_id):
    do=Do.query.get(do_id)
    db.session.delete(do)
    db.session.commit()
    return redirect("/")

@app.route('/edit/<int:do_id>',methods=['GET','POST'])
def edit(do_id):
    do = Do.query.get(do_id)
    if request.method=="POST":
        do.topic=request.form.get("topic")
        do.date=request.form.get("date")
        do.time=request.form.get("time")
        do.description=request.form.get("description")
        db.session.commit()
        return redirect("/")
    else:
        return render_template("edit.html",do=do,user=request.cookies.get('user'))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=1111,debug=True)
