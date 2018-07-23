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
        fullFilePath = os.path.join(fileLocation,filename)
        self.writeFileHeader(fullFilePath)
        for apiDetail in apis:
            if apiDetail['method'] == None:
                #Give error stating method not passed
                continue
            if apiDetail['method'].lower() == 'get':
                self.writeGETapi(apiDetail, fullFilePath)
            elif apiDetail['method'].lower == 'post':
                self.writePOSTapi(apiDetail, fullFilePath)

    def writeFileHeader(self, fullFilePath):
        with open(fullFilePath, 'w') as fp:
            fp.write(flask_snippets.FLASK_HEADER)
            fp.close()

    def writeGETapi(self, apiDetail, fullFilePath):
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
            with open(fullFilePath, 'a') as fp:
                fp.write(flask_snippets.FLASK_API_ROUTE_HEADER % route)
                fp.write(flask_snippets.FLASK_DEF_DECLARATION %(apiDetail['name'], method_params))
                if apiDetail['response_body'] == {} or apiDetail['response_body'] is None:
                    fp.write(flask_snippets.FLASK_DEF_BODY_WITHOUT_RESPONSE % method_params)
                else:
                    #Write code to add the class with all the fields for response body
                    # fp.write(flask_snippets.FLASK_DEF_BODY % 's')
                    pass
                fp.close()

    def writePOSTapi(self, apiDetail, fullFilePath):
        pass
        
