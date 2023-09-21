from flask import Flask, render_template,request,redirect,flash, abort, jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, login_required,current_user, logout_user
import os
import json
import glob
from uuid import uuid4
from datetime import datetime
from background_runner import BackgroundRunner
from flask_executor import Executor
import shutil
from io import BytesIO
from zipfile import ZipFile
app=Flask(__name__)
executor = Executor(app)
background_runner = BackgroundRunner(executor)

# @login_required
# def show_videos():
#     for user in db.session.query(Video_details).filter_by(username=current_user.username):
#         print(user.username)
#     return "Hello World"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://anonymizer:1g%$Y18yj6%4068Mjd@127.0.0.1/anonymizer'
app.secret_key = 'abrakndf'
app.config['UPLOAD_EXTENSIONS']=['.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.m4p', '.m4v', '.avi', '.wmv']
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class Video_details(UserMixin,db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), nullable=False)
    filepath=db.Column(db.String(200), nullable=False)
    outpath=db.Column(db.String(200),nullable=False)
    project_name=db.Column(db.String(200), nullable=False)
    date=db.Column(db.String(20),nullable=True)
    # def __repr__(self):
    #     return '<User %r>' % self.username
    def __init__(self,username,filepath,outpath,project_name,date):
        self.username=username
        self.filepath=filepath
        self.outpath=outpath
        self.project_name=project_name
        self.date=date
    def get_id(self):
        return (self.sno)

class User(UserMixin,db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    username=db.Column(db.String(20),unique=True, nullable=False)
    email=db.Column(db.String(80), unique=True,nullable=False)
    password=db.Column(db.String(120),nullable=False)
    def __init__(self, name,username,email,password):
        self.name=name
        self.username=username
        self.email=email
        self.password=password
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
    # Name type uploaded_on download_link
    data=[]
    i=1
    for user in db.session.query(Video_details).filter_by(username=current_user.username):
        temp=[]
        temp.append(i)
        i=i+1
        temp.append(user.project_name)
        temp.append("audio-video")
        temp.append(user.date)
        temp.append(user.project_name)
        data.append(temp)

    return render_template("dashboard.html", Name=current_user.name, username=current_user.username,data=data)

# @app.route("/show_videos")
# @login_required
# def show_videos():
#     for user in db.session.query(Video_details).filter_by(username=current_user.username):
#         print(user.username)
#     return "Hello World"
@app.route("/download/<filename>")
@login_required
def download(filename):
    stream = BytesIO()
    path=f"/mnt/rds/redhen/gallina/home/sxg1373/anonymizer_storage/output/{filename}"
    dir_list = os.listdir(path)
    if len(dir_list)==0:
        return "Try again later"
    print(path)
    with ZipFile(stream, 'w') as zf:
        for file in dir_list:
            print("this is the file", file)
            zf.write(f"{path}/{file}", os.path.basename(file))
    # shutil.make_archive(f"{filename}", 'zip', path)
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        attachment_filename=f'{filename}.zip'
    )
  
    return filename

@app.route("/upload",methods=['POST','GET'])
@login_required
def upload():
    if request.method=='POST':
        files=request.files
        form=request.form

        upload_key=str(uuid4())
        is_ajax = False
        if form.get("__ajax", None) == "true":
            is_ajax = True

    # Target folder for these uploads.
        # make a different folder on the server gallo in which the user files are stored permanently 
        target = "/mnt/rds/redhen/gallina/home/sxg1373/anonymizer_storage/input/{}".format(form.get("project_name",None))#temporary directory in which files are stored
        outpath = "/mnt/rds/redhen/gallina/home/sxg1373/anonymizer_storage/output/{}".format(form.get("project_name",None))#temporary directory in which files are stored
        print("This is the path of the final result",outpath)
        print(target)
        try:
            os.mkdir(target)
        except:
            if is_ajax:
                print("could not create upload directory")
                return ajax_response(False, "Couldn't create upload directory: {}".format(target))
            else:
                return "Couldn't create upload directory: {}".format(target)

        # make a json object and store all the anonymization parameters in it
        # project_name anonymization_type pitch echo distortion 
        project_info={"project_name": form.get("project_name",None),
        "visual_anonymization": form.get("visual_anonymization",None),
        "pitch": form.get("pitch",None),
        "echo":str(float(form.get("echo",None))),
        "distortion":form.get("distortion",None),
	"status":"0"       
        }
        # print("echo",str(float(form.get("echo",None))/10))
        project_info_json=json.dumps(project_info)
        print(project_info)
        with open(f"{target}/config.json", "w") as outfile:
            outfile.write(project_info_json)
        # save that object into a file in target folder


        for upload in request.files.getlist("file"):
            filename = upload.filename.rsplit("/")[0]
            file_ext=os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                os.rmdir(target)
                if is_ajax:
                    return ajax_response(False, upload_key)
                else:
                    flash("Please add only video files",'failure')
                    return redirect("/main")
            destination = "/".join([target, filename])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)
        now = datetime.now() 

        video_details=Video_details(username=current_user.username, filepath=target,outpath=outpath,project_name=form.get("project_name",None), date=now.strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(video_details)
        db.session.commit()
        if is_ajax:
            return ajax_response(True, upload_key)
        else:
            return redirect("/dashboard")
    
 
def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))

with app.app_context():
    db.create_all()
    app.run(debug=True, port=80000)
