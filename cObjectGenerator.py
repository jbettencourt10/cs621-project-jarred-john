import logging
class cObjectGenerator:

    def __init__(self, objectName):
        self.params = []
        self.objectName = objectName
    #Param is a tuple, where first is param name, second is type of variable
    def addParam(self, param):
        self.params.append(param)

    def generateCFile(self):
        logging.info("Generating C File for: " + self.objectName)
        file = self.objectName + ".cpp"
        with open(file, 'w') as fout:
            fout.write("class " + self.objectName + " { \n")
            fout.write("  public:\n")
            for x in self.params:
                fout.write("    " + x[0] + " " + x[1] + ";\n")

            fout.write("};")
