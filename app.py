from flask import Flask,render_template,jsonify,json,request
from testdb import db
from testdb import tester
import pdb
import logging
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
import os
db.create_all()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.init_app(app)
users = tester.query.all()
rows = db.session.query(tester).count()



@app.route('/')
def hello_world():
  return render_template('list.html')

@app.route('/getAllData',methods=['POST'])
def getAllList():
	try:
		users = tester.query.all()
		rows = db.session.query(tester).count()
		dataList = []
		for i in range(0,rows):
			dataItem = {
				'test1':users[i].test1
				,'test2':users[i].test2
				,'id': str(users[i].id)
				}
			dataList.append(dataItem)
		
	except Exception,e:
		return str(e)
	# pdb.set_trace()
	return json.dumps(dataList)

@app.route('/getData',methods=['POST'])
def getData():
    logging.info('Here')
    try:
        dataID = request.json['id']
        dataRow = tester.query.filter_by(id=dataID).first()
        dataDetail = {
                'test1':dataRow.test1,
                'test2':dataRow.test2,
                'id':dataRow.id
                }
        return json.dumps(dataDetail)
    except Exception, e:
        return str(e)
	

@app.route("/addData",methods=['POST'])
def addData():
    try:
        json_data = request.json['info']
        test1 = json_data['test1']
        test2 = json_data['test2']

        taco = tester(test1, test2)

        db.session.add(taco)
        db.session.commit()

        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/updateData',methods=['POST'])
def updateData():
    try:
        dataInfo = request.json['info']
        dataRow = tester.query.filter_by(id=dataInfo['id']).first()
        dataRow.test1 = dataInfo['test1']
        dataRow.test2 = dataInfo['test2']

        db.session.commit()

        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@app.route("/deleteData",methods=['POST'])
def deleteData():
    try:
        dataID = request.json['id']
        dataRow = tester.query.filter_by(id=dataID).first()
        db.session.delete(dataRow)
        db.session.commit()

        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))
@app.route('/sms',methods = ['POST'])
def sms():
	number = request.form['From']
	message_body = request.form['Body']
	msg_list = message_body.split(" ")
	
	taco = tester(msg_list[0], msg_list[1])

        db.session.add(taco)
        db.session.commit()

	resp = MessagingResponse()
	if number == '+13125689880':
		resp.message('Hello Casey, {}'.format(msg_list[1]))
	else:
		resp.message('Hello {}, Fuck you'.format(number))
	return str(resp)


if __name__ == '__main__':
  app.run()
