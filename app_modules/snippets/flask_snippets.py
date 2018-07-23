#This file will contain code snippets for flask environment

FLASK_HEADER = '''from flask import Flask,request
import json
app = Flask(__name__)'''

FLASK_API_ROUTE_HEADER = '''\n\n@app.route("/%s")''' #replace %s with the route
FLASK_DEF_DECLARATION = ''' \ndef %s(%s):''' #replace the function name and the function parameters
FLASK_DEF_BODY_WITH_RESPONSE = '''\n\t#Write logic here\n\treturn json.dumps(%s())''' #%s to replace response class name
FLASK_DEF_BODY_WITHOUT_RESPONSE = '''\n\t#Write logic here\n\treturn %s'''

#Path variables. Here %s replaces with the variable name.
FLASK_PATH_VAR_INT = '/<int:%s>'
FLASK_PATH_VAR_STRING = '/<string:%s>'
FLASK_PATH_VAR_FLOAT = '/<float:%s>'
FLASK_PATH_VAR_PATH = '/<path:%s>'

#Class declarations. Mostly for Response bodies
FLASK_CLASS_DECLARATION = '\n\nclass %s():'
FLASK_CLASS_INIT_DEF = '''\n\tdef __init__():'''
FLASK_CLASS_INIT_SELF_INT = '''\n\t\tself.%s = 0'''#%s to have variable name
FLASK_CLASS_INIT_SELF_STRING = '''\n\t\tself.%s = ""'''
FLASK_CLASS_INIT_SELF_DATE = '''\n\t\tself.%s = ""'''



