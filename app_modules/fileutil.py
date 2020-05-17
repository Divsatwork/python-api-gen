import os
from .snippets import flask_snippets

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
        if str != type(dirLocation):
            raise ValueError('Provided directory location is not valid')
        if os.path.isdir(dirLocation):
            pass
        else:
            self.makeDir(dirLocation)

    def makeDir(self, dirLocation):
        if dirLocation is None:
            raise ValueError('No valid dir location provided')
        os.mkdir(dirLocation)

    def createControllerFile(self, filename, fileLocation, apis=[]):
        if self.checkFile(filename,fileLocation):
            # raise ValueError('Already existing controller exists')
            pass
        self.checkDir(fileLocation)
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
            elif apiDetail['method'].lower() == 'post':
                self.writePOSTapi(apiDetail, filename, fileLocation)
        self.writeFileFooter(filename, fileLocation)

    def writeFileHeader(self, filename, fileLocation):
        with open(os.path.join(fileLocation,filename), 'w') as fp:
            fp.write(flask_snippets.FLASK_HEADER)
            fp.close()

    def writeFileFooter(self, filename, fileLocation):
        with open(os.path.join(fileLocation,filename), 'a') as fp:
            fp.write(flask_snippets.FLASK_FOOTER)

    def writeGETapi(self, apiDetail, filename, fileLocation):
        print('Writing GET API: ', apiDetail['name'])
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

        with open(os.path.join(fileLocation,filename), 'a') as fp:
            fp.write(flask_snippets.FLASK_API_GET_ROUTE_HEADER % route)
            fp.write(flask_snippets.FLASK_DEF_DECLARATION %(apiDetail['name'], method_params))

            if apiDetail['parameters'] is not None and type(apiDetail['parameters']) is dict:
                for item in apiDetail['parameters'].items():
                    #Gives a list of the parameters
                    #[(name, {type:int, required: true}), (id, {type:string, required:false})]
                    # one item = one tuple
                    if item[1]['required'] == True:
                        fp.write(flask_snippets.FLASK_DEF_BODY_REQ_PARAM_REQUIRED % item[0])
                        fp.write(flask_snippets.FLASK_DEF_BODY_REQ_PARAM_REQUIRED_TYPE %(item[0],item[1]['type']))
                    else:
                        fp.write(flask_snippets.FLASK_DEF_BODY_REQ_PARAM_NOT_REQUIRED % item[0])

            if apiDetail['response_body'] == {} or apiDetail['response_body'] is None:
                fp.write(flask_snippets.FLASK_DEF_BODY_WITHOUT_RESPONSE)
            else:
                #Write code to write the class with all the fields for response body and also
                #create an __init__ file so that the file can be imported.
                cfilename = apiDetail['response_body']['name']+'.py'
                self.checkDir(os.path.join(fileLocation,'responses'))
                cf = open(os.path.join((os.path.join(fileLocation,'responses')),cfilename), 'w')
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
                self.createFile('__init__.py', os.path.join(fileLocation,'responses'))
                fp.write(flask_snippets.FLASK_CLASS_INIT_IMPORT_SNIPPET.format(class_name=str(apiDetail['response_body']['name'])))
                fp.write(flask_snippets.FLASK_DEF_BODY_WITH_RESPONSE % (str(apiDetail['response_body']['name'])+'.'+ str(apiDetail['response_body']['name'])))
            

    def writePOSTapi(self, apiDetail, filename, fileLocation):
        print('Writing POST API')
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
            print (route)
        with open(os.path.join(fileLocation,filename), 'a') as fp:
            fp.write(flask_snippets.FLASK_API_POST_ROUTE_HEADER % route)
            fp.write(flask_snippets.FLASK_DEF_DECLARATION %(apiDetail['name'], method_params))
            if apiDetail['response_body'] == {} or apiDetail['response_body'] is None:
                fp.write(flask_snippets.FLASK_DEF_BODY_WITHOUT_RESPONSE)
            else:
                #Write code to write the class with all the fields for response body and also
                #create an __init__ file so that the file can be imported.
                cfilename = apiDetail['response_body']['name']+'.py'
                self.checkDir(os.path.join(fileLocation,'responses'))
                cf = open(os.path.join((os.path.join(fileLocation,'responses')),cfilename), 'w')
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
                self.createFile('__init__.py', os.path.join(fileLocation,'responses'))
                fp.write(flask_snippets.FLASK_CLASS_INIT_IMPORT_SNIPPET.format(class_name=str(apiDetail['response_body']['name'])))
                fp.write(flask_snippets.FLASK_DEF_BODY_WITH_RESPONSE % (str(apiDetail['response_body']['name'])+'.'+ str(apiDetail['response_body']['name'])))
                fp.close()
