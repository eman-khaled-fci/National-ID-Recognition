from flask_restful import Resource, reqparse, abort
import werkzeug
import UserDatabase
import imageUtils
from Model import Model
import datetime
user_put_args = reqparse.RequestParser()
user_put_args.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
user_put_args.add_argument("n_of_room", type=int, help="n_of_room")
user_put_args.add_argument("size_of_room", type=str, help="size_of_room")
user_put_args.add_argument("time_of_reguest", type=str, help="time_of_reguest")
user_put_args.add_argument("time_of_receive", type=str, help="time_of_receive")
user_put_args.add_argument("n_of_day", type=int, help="n_of_day")
user_put_args.add_argument("total_price", type=int, help="total_price")
user_put_args.add_argument("approve", type=bool, help="false")
#user_put_args.add_argument("name", type=str, help="your name")
#user_put_args.add_argument("National_id", type=str, help="your National id")
#user_put_args.add_argument("image", type=str, help="your image")
class UserRouter (Resource):
    def get(self, National_id):
        result = UserDatabase.getById(National_id)
        if(result["National_id"]==0):
            abort(404)
        return result
    def patch(self, National_id):
        args = user_put_args.parse_args()
        if(UserDatabase.update(args, National_id)==False):
            abort(404)
        return {"data":"success"}

    def delete(self, National_id):
        if(UserDatabase.delete(National_id)==False):
            abort(404)
        return {"data":"success"}

class UserListRouter(Resource):
    def get(self):
        return UserDatabase.getAll()
    def post(self):
        args = user_put_args.parse_args()
        #UserDao.create(args)
        img = args['file']
        img.save("uploads/temp.jpg")
        name,id,image= imageUtils.extractInfo("uploads/temp.jpg")
        #time=imageUtils.time(self)
        d= {
            'name': name,
            'National_id': id,
            'image': image,
            'time_of_reguest':datetime.datetime.now()
        }
        UserDatabase.create(d)