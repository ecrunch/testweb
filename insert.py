from testdb import db
from testdb import tester
db.create_all()

test1 = 'test3'
test2 = 'test4'

users = tester.query.all()
print users

taco = tester(test1, test2)
print taco
db.session.add(taco)
db.session.commit()


