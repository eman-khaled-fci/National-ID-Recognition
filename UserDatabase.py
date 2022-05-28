from flask_restful import fields, marshal_with
from database import database
from Model import Model
resource_fields = {
    'name': fields.String,
    'National_id': fields.String,
    'image': fields.String,
    'n_of_room':fields.Integer,
    'size_of_room':fields.String,
    'time_of_reguest':fields.String,
    'time_of_receive':fields.String,
    'n_of_day':fields.Integer,
    'total_price':fields.Integer,
    'approve':fields.Boolean
}
@marshal_with(resource_fields)
def getAll():
    result = Model.query.all()
    return result

@marshal_with(resource_fields)
def getById(National_id):
    result = Model.query.get(National_id)
    return result

def create(user):
    database.session.add(Model(**user))
    database.session.commit()
    return True


def update(new_user, National_id):
    user = Model.query.get(National_id)
    if(user == None):
        return False
    if(new_user.n_of_room != None):
        user.n_of_room = new_user['n_of_room']
    if(new_user.size_of_room !=None):
        user.size_of_room = new_user['size_of_room']
    if(new_user.time_of_receive!=None):
        user.time_of_receive = new_user['time_of_receive']
    if(new_user.n_of_day!=None):
        user.n_of_day = new_user['n_of_day']
    if(new_user.total_price!=None):
        user.total_price = new_user['total_price']
    if(new_user.approve!=None):
        user.approve = new_user['approve']
    database.session.commit()
    return True

def delete(National_id):
    user = Model.query.get(National_id)
    if(user==None):
        return False
    database.session.delete(user)
    database.session.commit()
    return True