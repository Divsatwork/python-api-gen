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

    def createControllerFile(self, filename, fileLocation, apis={}):
        if self.checkFile(filename,fileLocation):
            raise ValueError('Already existing controller exists')
        self.createFile(filename, fileLocation) #File created
        if apis is None or apis == {}:
            raise ValueError('No API provided to be written in the controller')
        #Write header
        f = open(os.path.join(fileLocation, filename), 'a')
        f.write(flask_snippets.FLASK_HEADER)
        #Write API header
        f.write(flask_snippets.FLASK_API_ROUTE_HEADER % 'test')
        f.close()
