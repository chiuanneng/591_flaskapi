import flask
from flask_restful import Api
#使用resources呼叫api class
# from resources.resource_mysql import Find_All,PrintHello
from resources.resource_elastic import Question1,Question2,Question3,Question4
from resources.resource_elastic_api import All

app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
#使用api.add_resource( class_name,m ' /url網址(自訂義) ' )
# api.add_resource(PrintHello,'/hello')
# api.add_resource(Find_All,'/find')
api.add_resource(Question1,'/q1')
api.add_resource(Question2,'/q2/<num>')
api.add_resource(Question3,'/q3')
api.add_resource(Question4,'/q4')
api.add_resource(All,"/housedata",endpoint='housedata')
# 測試有無成功開啟
@app.route('/',methods = ['GET'])
def home():
    return "<h1>Hello Flask!!!</h1>"
# 假如使用jupyternotebook記得加上use_reloader=False否則會報錯
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000,use_reloader=False)




