class animator:
    def __init__(self):
        self.anims = dict()
    def start_anim(self,id):
        for a in self.anims:
            #if a["animid"]==id:
            self.anims[id]["active"]=True
    def add_anim(self,anim_id,obj_id,frames,dposs,loop):
        self.anims[anim_id]={"objid":obj_id,"frames":frames,"deltaposs":dposs,"isloop":loop,"current_frame":0,"active":False}