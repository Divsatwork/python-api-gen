import web
from app_modules import fileUtil
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
        filer = fileUtil.fileUtil()
        if x['location'] == None or (str!=type(x['location'])):
            raise ValueError("Please provide a valid path")
        if x['controllerFileName'] is None or type(x['controllerFileName']) is not str:
            raise ValueError("Please provide a valid file name for the controller")
        filer.createControllerFile(x['controllerFileName'], x['location'], x['list'])
        # print x['list']
        del filer
        return "ok"

if __name__ == "__main__":
    print ('Starting server at port 8080')
    app.run()