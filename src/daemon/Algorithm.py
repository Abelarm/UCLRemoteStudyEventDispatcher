__author__ = 'Luigi'

#Class that represents an Algorithm of the framework
class Algorithm:

    def __init__(self,Name):
        self.Name=Name
        self.properties={}
        self.properties['keys']=[]

    def getKeys(self):
        return self.properties['keys']

    def getVersion(self):
        return self.properties['version']

    def getPath(self):
        try:
            return self.properties['path']
        except KeyError:
            return False

    def __str__(self):
        return 'Name: '+self.Name + ',Properties:' + str(self.properties)


def main():
     Alg = Algorithm('TEST',['a','b','c'])


if __name__ == "__main__":
    main()