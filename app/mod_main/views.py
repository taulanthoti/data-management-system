from flask import Blueprint, render_template, request, redirect, url_for, Response, flash
from app import mongo
from bson import ObjectId
import json

mod_main = Blueprint('main', __name__)

from werkzeug import secure_filename

from os.path import join, dirname, realpath, os

UPLOAD_FOLDER = join(dirname(realpath(__file__)), "../static/uploads/")

@mod_main.route('/', methods=['GET','POST'])
def index():
	if request.method == 'GET':
		audits = mongo.db.audits.find()
		return render_template('home.html',audits=audits)

@mod_main.route('/remove/', methods=['GET','POST'])
def remove():
    if request.method == 'POST':
    	audit_id = request.form["audit_id"]
    	mongo.db.audits.remove({"_id": ObjectId(audit_id)})
    	return Response(json.dumps({"removed": True}), mimetype='application/json')


@mod_main.route('/newAudit',methods=['GET','POST'])
def newAudit():
	db = mongo.db.audits
	if request.method == 'GET':
		return render_template('newAudit.html')
	elif request.method == 'POST':
		data = request.form.to_dict()
		db.insert(data)
	else:
		return "bad request"
	flash('New Audit has been successfully submitted!')
	return redirect(url_for("main.index")) 

@mod_main.route('/auditEdit/<string:audit_id>',methods=['GET','POST'])
def auditEdit(audit_id):
	db = mongo.db.audits
	if request.method == 'GET':		
		audit = db.find_one({"_id":ObjectId(audit_id)})
		return render_template('auditEdit.html',audit=audit)
	elif request.method == 'POST':
		# reference_number = request.form['reference_number']
		# audit_type = request.form['audit_type']
		# description = request.form['description']
		# audit_teamleader = request.form['audit_teamleader']
		# audit_st_date = request.form['audit_st_date']
		# ref_num = request.form['ref_num']
		# audit_end_date = request.form['audit_end_date']
		# followup_refnum = request.form['followup_refnum']
		# doc_review = request.form['doc_review']
		# place = request.form['place']
		# audit_teammembers = request.form['audit_teammembers']
		# change_ref_num = request.form['change_ref_num']
		# auditee_participants = request.form['auditee_participants']
 	# 	audit_title = request.form['audit_title']
 	# 	version_date = request.form['version_date']
 	# 	auditee = request.form['auditee'] 		 
		# db.update({"_id": ObjectId(audit_id)},{'$set':{"reference_number":reference_number,"audit_type":audit_type,"description":description,"audit_teamleader":audit_teamleader,"audit_st_date":audit_st_date,"ref_num":ref_num,"audit_end_date":audit_end_date,"followup_refnum":followup_refnum,"doc_review":doc_review,"place":place,"audit_teammembers":audit_teammembers,"change_ref_num":change_ref_num,"auditee_participants":auditee_participants,"audit_title":audit_title,"version_date":version_date,"auditee":auditee}})
		
		file = request.files['document1']
		file2 = request.files['document2']
		file3 = request.files['document3']

		filename = file.filename
		filename2 = file2.filename
		filename3 = file3.filename
		
		file.save(os.path.join(UPLOAD_FOLDER, filename))
		file2.save(os.path.join(UPLOAD_FOLDER, filename2))
		file3.save(os.path.join(UPLOAD_FOLDER, filename3))
	flash('Audit updated successfully!')
	return redirect(url_for("main.index")) 

@mod_main.route('/newNC/<string:audit_id>',methods=['GET','POST'])
def newNC(audit_id):
	db = mongo.db.audits
	if request.method == 'GET':
		return render_template('newNC.html')
	elif request.method == 'POST':
		data = request.form.to_dict()
		data['audit_id'] = audit_id
		db.insert(data)
	flash('Non-Conformity has been successfully submitted!')
	return redirect(url_for("main.index")) 

@mod_main.route('/login', methods=['GET','POST'])
def login():
	return render_template('login.html')

@mod_main.route('/forgot-password', methods=['GET','POST'])
def forgotPassword():
	return render_template('forgot-password.html')

@mod_main.route('/user', methods=['GET'])
def user():
	return render_template('user.html')

@mod_main.route('/admin', methods=['GET'])
def admin():
	return render_template('admin.html')

@mod_main.route('/editNC',methods=['GET'])
def editnc():
	return render_template('editNC.html')

@mod_main.route('/editCA',methods=['GET'])
def editca():
	return render_template('editCA.html')
