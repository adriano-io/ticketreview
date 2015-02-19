import flask, flask.views
import os
#from flask import send_from_directory
import functools
import subprocess
import json
import csv

app = flask.Flask(__name__)
# Don't do this!
app.secret_key = "everythingisawesome"

users = {'ace':'ace','adriano':'ace123','erran':'fenech123'}

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('welcome.html')
    
    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('welcome'))
        required = ['username', 'passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('welcome'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        if username in users and users[username] == passwd:
            flask.session['username'] = username
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('welcome'))

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return flask.redirect(flask.url_for('welcome'))
    return wrapper

class Remote(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('remote.html')
    @login_required
    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return flask.redirect(flask.url_for('remote'))

class Deployments(flask.views.MethodView):
    @login_required
    def get(self):
        roles = os.listdir('/home/ansible/roles')
        return flask.render_template("deployments.html", roles=roles)

class Breakfixes(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('breakfixes.html')
    @login_required
    def post(self):
        tags = "--test1 --test2 --test3 "
        roles = "make ansible version (ransack-core 12345 all ping) for testings "
        command = "ansible-playbook " + roles + tags
        text_file = open("Output.txt", "w")
        text_file.write(command)
        text_file.close()
        result = "Successful: " + command
        flask.flash(result)
        return flask.redirect(flask.url_for('breakfixes'))

class Roles(flask.views.MethodView):
    def get(self):
        results = os.listdir('/home/ansible/roles')

class Review(flask.views.MethodView):
    def writeCSV(jsonObject):
        csv_file = csv.writer(open("./erran.csv", "wb+"))
        for item in jsonObject:
            csv_file.writerow([item["account"],
                               item["ticket"],
                               item["catergory"],
                               item["subject"],
                               item["requests"],
                               item["issues"],
                               item["comments"]])    
    @login_required
    def get(self):
        return flask.render_template('review.html')
    @login_required
    def post(self):
        obj = {u"account": flask.request.form['account_number'],
        u"ticket": flask.request.form['ticket_number'],
        u"catergory": flask.request.form['catergory'], 
        u"subject": flask.request.form['subject'],
        u"requests": (flask.request.form.getlist('requests[]')),
        u"issues": (flask.request.form.getlist('issues[]')),
        u"comments": flask.request.form['comments']
        }
        #account = flask.request.form['account_number']
        #ticket = flask.request.form['ticket_number']
        #subject = flask.request.form['subject']
        #requests = flask.request.form['requests']
        #issues = flask.request.form['issues']
        #comments = flask.request.form['comments']
        #command = account + ","+ ticket +","+ subject +","+ requests+","+ issues +","+ comments
        #text_file = open("Output.txt", "w")
        #text_file.write(command)
        #text_file.close()
        #result = "Successful: " + command
        #flask.flash(result)
        flask.flash(json.dumps(obj, indent=4))
        return flask.redirect(flask.url_for('review'))





app.add_url_rule('/', view_func=Main.as_view('welcome'), methods=["GET", "POST"])
app.add_url_rule('/remote/', view_func=Remote.as_view('remote'), methods=['GET', 'POST'])
app.add_url_rule('/breakfixes/', view_func=Breakfixes.as_view('breakfixes'), methods=['GET', 'POST'])
app.add_url_rule('/deployments/', view_func=Deployments.as_view('deployments'), methods=['GET']) 
app.add_url_rule('/review/', view_func=Review.as_view('review'), methods=['GET', 'POST'])

#app.add_url_rule('/ansible/',
   #              view_func=Ansible.as_view('ansible'),
   #              methods=['GET'])

app.debug = True
app.run()
