from models import User, db
from app import app

user_one = { 'first_name':"user_one_first_name" , 'last_name':'last_name_test_sub' }
 
def initial_information():

    alex_rutan = User( first_name = 'alex' , last_name =  'rutan')
    simon_zhang = User( first_name = 'simon' , last_name =  'zhang')
    joel_burton = User( first_name = 'joel' , last_name =  'burtan')
    karmen_ming = User( first_name = 'karmen' , last_name =  'ming')

    return [ alex_rutan, simon_zhang , joel_burton, karmen_ming]

