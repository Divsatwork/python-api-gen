import web

urls = (
    '/','home'
)

app = web.application(urls, globals())

render = web.template.render('templates/', base='layout')

class home:
    def GET(self):
        return render.index()

if __name__ == "__main__":
    print 'Starting server at port 8080'
    app.run()