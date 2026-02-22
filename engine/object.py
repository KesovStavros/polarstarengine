class object:
    def __init__(self):
        self.obj_args=[]
        self.id=""
        self.type=""
    def init(self,type,oid,args):
        self.id=oid
        self.obj_args=args
        self.otype=type
    def set_arg(self,name,val):
        self.obj_args[name]=val
    def getobj(self):
        return {"id":self.id,"type":self.otype,"args":self.obj_args}