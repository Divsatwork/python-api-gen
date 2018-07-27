import web
from app_modules import fileutil
import json

#Our applications end points
urls = (
    '/','home',
    '/controller','controller'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base='layout')

#Classes for our endpoints
class home:
    def GET(self):
        return render.index()

class controller:
    def GET(self):
        return json.dumps({'message':"Method not allowed"})

    def POST(self):
        x = json.loads(web.data())
        filer = fileutil.fileUtil()
        if x['location'] == None or (unicode!=type(x['location'])):
            raise ValueError("Please provide a valid path")
        filer.createControllerFile('final.py', x['location'], x['list'])
        # print x['list']
        del filer
        return "ok"

if __name__ == "__main__":
    print 'Starting server at port 8080'
    app.run()