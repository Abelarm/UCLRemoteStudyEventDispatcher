__author__ = 'Luigi'

class Algorithm:

    def __init__(self,Name):
        self.Name=Name
        self.properties={}
        self.properties['keys']=[]
        #self.loadConf()

    def loadConf(self):

        conf = open('Configurations/Algorithm.yml','r')

        self.properties= dict()

        for line in conf:
            nam = line.split(':')[0]
            typ = line.split(':')[1]

            if typ == '+':
                self.properties[nam]=[]
            else:
                self.properties[nam]=str()

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

    Alg = Algorithm('Antonio',['a','b','c'])


if __name__ == "__main__":
    main()