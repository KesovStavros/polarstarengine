class dialog:
    def __init__(self):
        self.phrases=[]
        self.id=""
        self.name=""
        self.active=False
        self.phrase=0
    def init(self,name,id,phrases):
        self.phrases=phrases
        self.id=id
        self.name=name
    def start(self):
        self.active=True
    def nextphrase(self):
        self.phrase+=1