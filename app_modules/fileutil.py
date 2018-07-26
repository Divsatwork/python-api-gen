import os
from snippets import flask_snippets

class fileUtil:

    def createFile(self, filename, fileLocation):
        if filename is None:
            raise ValueError('Please provie a valid filename')
        if fileLocation is None:
            raise ValueError('Please provide a valid location for the file')
        fullFilePath = os.path.join(fileLocation, filename)
        with open(fullFilePath, 'w') as f:
            f.write('')
            f.close()

    def checkFile(self, filename, fileLocation):
        if filename is None or fileLocation is None:
            raise ValueError('File with the provided name and path does not exist')
        fullFilePath = os.path.join(fileLocation, filename)
        return os.path.isfile(fullFilePath)

    def checkDir(self, dirLocation):
        if dirLocation is None:
            raise ValueError('Provided directory location is not valid')
        return os.path.isdir(dirLocation)

    def createControllerFile(self, filename, fileLocation, apis=[]):
        if self.checkFile(filename,fileLocation):
            raise ValueError('Already existing controller exists')
        self.createFile(filename, fileLocation) #File created
        if apis is None or apis == []:
            raise ValueError('No API provided to be written in the controller')
        self.writeFileHeader(filename, fileLocation)
        for apiDetail in apis:
            if apiDetail['method'] == None:
                #Give error stating method not passed
                continue
            if apiDetail['method'].lower() == 'get':
                self.writeGETapi(apiDetail, filename, fileLocation)
            elif apiDetail['method'].lower == 'post':
                self.writePOSTapi(apiDetail, filename, fileLocation)

    def writeFileHeader(self, filename, fileLocation):
        with open(os.path.join(fileLocation,filename), 'w') as fp:
            fp.write(flask_snippets.FLASK_HEADER)
            fp.close()

    def writeGETapi(self, apiDetail, filename, fileLocation):
        if apiDetail['path'] == {} or apiDetail['path'] == None:
            route = apiDetail['route']
            method_params = ''
        else:
            route = apiDetail['route']
            method_params = ''
            for i in apiDetail['path']:
                #apiDetail['path'][i] defines the type of the path variable
                if str(apiDetail['path'][i]).lower() == 'int':
                    route += flask_snippets.FLASK_PATH_VAR_INT % i
                elif str(apiDetail['path'][i]).lower() == 'string':
                    route +=flask_snippets.FLASK_PATH_VAR_STRING % i
                method_params = method_params+str(i)+','
            else:
                method_params = method_params[:-1]
            print route
        with open(os.path.join(fileLocation,filename), 'a') as fp:
            fp.write(flask_snippets.FLASK_API_ROUTE_HEADER % route)
            fp.write(flask_snippets.FLASK_DEF_DECLARATION %(apiDetail['name'], method_params))
            if apiDetail['response_body'] == {} or apiDetail['response_body'] is None:
                fp.write(flask_snippets.FLASK_DEF_BODY_WITHOUT_RESPONSE % method_params)
            else:
                #Write code to write the class with all the fields for response body and also
                #create an __init__ file so that the file can be imported
                # fp.write(flask_snippets.FLASK_DEF_BODY % 's')
                cfilename = apiDetail['response_body']['name']+'.py'
                cf = open(os.path.join(fileLocation,cfilename), 'w')
                cf.write(flask_snippets.FLASK_CLASS_DECLARATION % apiDetail['response_body']['name'])
                cf.write(flask_snippets.FLASK_CLASS_INIT_DEF)
                for response_param in apiDetail['response_body']['fields']:
                    if str == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(flask_snippets.FLASK_CLASS_INIT_SELF_STRING % response_param)
                    elif int == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(flask_snippets.FLASK_CLASS_INIT_SELF_INT % response_param)
                    elif list == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(flask_snippets.FLASK_CLASS_INIT_SELF_LIST % response_param)
                    elif dict == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(flask_snippets.FLASK_CLASS_INIT_SELF_DICT % response_param)
                    else:
                        cf.write(flask_snippets.FLASK_CLASS_INIT_SELF_STRING % response_param)
                cf.close()
                self.createFile('__init__.py', fileLocation)
                fp.write(flask_snippets.FLASK_CLASS_INIT_IMPORT_SNIPPET % apiDetail['response_body']['name'])
                fp.write(flask_snippets.FLASK_DEF_BODY_WITH_RESPONSE % (str(apiDetail['response_body']['name'])+'.'+ str(apiDetail['response_body']['name'])))
                fp.close()

    def writePOSTapi(self, apiDetail, filename, fileLocation):
        pass
