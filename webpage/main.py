from flask import Flask, render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, login_required,current_user, logout_user
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@127.0.0.1/Anonymizer'
app.secret_key = 'abrakndf'
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    username=db.Column(db.String(20),unique=True, nullable=False)
    email=db.Column(db.String(80), unique=True,nullable=False)
    password=db.Column(db.String(120),nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username
    def get_id(self):
        return (self.sno)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter_by(username=username).first()
        if user and password==user.password:
            login_user(user)
            return redirect("dashboard")
        else :
            flash('Invalid Credentials', 'warning ')
            return redirect('/')

    return render_template("login.html")

@app.route('/logout')
def logout():
    # Logout the user
    logout_user()
    return redirect('/')


@app.route("/register", methods=['POST','GET'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        name=request.form.get('name')
        username=request.form.get('username')
        password=request.form.get('password')
        # print(email,password,username,name)
        user=User(name=name,username=username,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registered Successfully!!",'success')
        return redirect("/")
    return render_template("register.html")

@app.route("/main")
@login_required
def main():
    return render_template("main.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", Name=current_user.name, username=current_user.username)

app.run(debug=True)