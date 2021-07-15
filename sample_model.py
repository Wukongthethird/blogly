from models import User, db


db.drop_all()
db.create_all()    


alex_rutan = User( first_name = 'alex' , last_name =  'rutan')
simon_zhang = User( first_name = 'simon' , last_name =  'zhang')
joel_burton = User( first_name = 'joel' , last_name =  'burtan')
karmen_ming = User( first_name = 'karmen' , last_name =  'ming')
test_users = [ alex_rutan, simon_zhang , joel_burton, karmen_ming]


db.session.add_all(test_users)
db.session.commit()

