import web
from app_modules import fileutil

#Our applications end points
urls = (
    '/','home'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base='layout')

#Classes for our endpoints
class home:
    def GET(self):
        filer = fileutil.fileUtil()
        filer.createControllerFile('test.txt',r'C:\Users\Divyansh\Desktop', {'api1':'some api details'})
        del filer
        return render.index()

if __name__ == "__main__":
    print 'Starting server at port 8080'
    app.run()