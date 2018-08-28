from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import urllib

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
#from resources.store import Store, StoreList

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

quoted = urllib.parse.quote('mssql+pyodbc://SQL_API_SERVER/APIDB')
#quoted = urllib.parse.quote('DRIVER={FreeTDS};Server=SQL_API_SERVER;Database=APIDB;UID=sa;PWD=Mitjuk009!S;TDS_Version=8.0;Port=1433;')
# using the above logic I just did the following
quoted = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=KUJTIM_OFFICEPC\SQL_API_SERVER;DATABASE=APIDB;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///sa:Mitjuk009!S@?odbc_connect={}".format(quoted)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth






#api.add_resource(Store, '/store/<string:name>')
#api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
