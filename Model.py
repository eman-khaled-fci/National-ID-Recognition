from database import database
class Model(database.Model):
        National_id = database.Column(database.String(18), primary_key=True)
        name = database.Column(database.String(100), nullable = False)
        image =database.Column(database.String(100000), nullable = False)
        n_of_room=database.Column(database.Integer)
        size_of_room=database.Column(database.String(50))
        time_of_reguest=database.Column(database.String(50), nullable = False)
        time_of_receive=database.Column(database.String(50))
        n_of_day=database.Column(database.Integer)
        total_price=database.Column(database.Integer)
        approve=database.Column(database.Boolean, default=False)


