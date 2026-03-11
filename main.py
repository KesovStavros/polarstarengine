from engine import object
from engine import animator
from engine import dialogs
import pygame
pygame.init()
frame = pygame.display.set_mode((500,500))
pygame.display.set_caption("polarstar 2d")
pygame.display.set_icon(pygame.image.load("logo.png"))
asys=animator.animator()
objects=[]
collisions=[]
objup=[]
objdp=[]
svars={}
nvars={}
dialogsl=[]
sounds=[]
run=True
devmode=False
px,py,rpx,rpy=0,0,0,0
psi=(50,50)
ps=0.1
dir=3
curstep=1
move=False
def loaddialogs(dp):
    global dialogsl
    dialogsl=[]
    with open(dp+".kdf","r") as df:
        dr=df.read()
        dl=dr.split("/;/")
        for d in dl:
            dd=d.split("\n")
            do=dialogs.dialog()
            do.init(dd[1],dd[0],dd[2:])
            dialogsl.append(do)
def loadanims(ap):
    global asys
    asys.anims={}
    with open(ap+".kaf","r") as af:
        ar=af.read()
        a=ar.split("/;/")
        for anim in a:
            anima=anim.split("\n")
            loop=False
            if anima[4]=="true":
                loop=True
            asys.add_anim(anima[0],anima[1],anima[2].split(" "),anima[3].split(" "),loop)
        print(asys.anims)
def loadmap(mapn):
    global objects
    global collisions
    global px
    global py
    global ps
    global psi
    global svars
    global nvars
    global sounds
    objects=[]
    collisions=[]
    for s in sounds:
        s.stop()
    sounds=[]
    svars=dict()
    nvars=dict()
    with open(mapn+".kmf","r") as mapf:
        mapr=mapf.read()
        map=mapr.split("\n")
        
        for o in map:
            obj=object.object()
            args=dict()
            oargs=dict()
            ob=o.split("/;/")
            for a in ob:
                if a.split("/:/")[0]=="":pass
                elif a.split("/:/")[0]=="args":
                    for s in a.split("/:/")[1].split("?;?"):
                        args[s.split("?:?")[0]]=s.split("?:?")[1]
                else:
                    oargs[a.split("/:/")[0]]=a.split("/:/")[1]
            print((oargs["type"],oargs["id"],args))
            obj.init(oargs["type"],oargs["id"],args)
            objects.append(obj)
            if oargs["type"]=="var":
                if args["vtype"]=="string":
                    svars[oargs["id"]]=args["value"]
                if args["vtype"]=="number":
                    nvars[oargs["id"]]=float(args["value"])
            if oargs["type"]=="player":
                px=float(args["spawn"].split(",")[0])
                py=float(args["spawn"].split(",")[1])
                ps=float(args["speed"])
                psi=(int(args["scale"].split(",")[0]),int(args["scale"].split(",")[1]))
            if oargs["type"]=="collision":
                try:
                    for x in range(int(args["x1"]),int(args["x2"])):
                        for y in range(int(args["y1"]),int(args["y2"])):
                            collisions.append((x,y))
                except:
                    aaaaaa=0
with open("save.txt","r") as sf:
    cm=sf.read()
    loadmap(cm)
    try:
        loadanims(cm+".anims")
        loaddialogs(cm+".dialogs")
    except:dsdsds=0
while run:
    ckey=""
    if move==True:
        objdp=[]
        objup=[]
        rpx=px
        rpy=py
        if dir==0:py-=ps
        elif dir==1:px+=ps
        elif dir==2:px-=ps
        else:py+=ps
        if (int(px),int(py)) in collisions:
            px=rpx
            py=rpy
        for obj in objects:
            try:#if obj.getobj()["args"]["pos"]:
                if obj.getobj()["args"]["pos"]:
                    if int(obj.getobj()["args"]["pos"].split(",")[1])<py:
                        objdp.append(obj)
                    else:
                        objup.append(obj)
            except:
                objdp.append(obj)
    frame.fill((0,0,0))
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            run=False
        if e.type==pygame.KEYDOWN:
            if pygame.KMOD_LCTRL == pygame.key.get_mods():
                if e.key==pygame.K_d:
                    devmode=True
            if e.key==pygame.K_w:
                dir=0
                move=True
            if e.key==pygame.K_d:
                dir=1
                move=True
            if e.key==pygame.K_a:
                dir=2
                move=True
            if e.key==pygame.K_s:
                dir=3
                move=True
            ckey=e.unicode
        if e.type==pygame.KEYUP:move=False
    for ob in objdp:
        o=ob.getobj()
        if o["type"]=="label":
            if o["args"]["ltype"]=="string":
                frame.blit(pygame.font.Font(o["args"]["font"],int(o["args"]["scale"])).render(svars[o["args"]["string"]],True,(255,255,255)),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
            if o["args"]["ltype"]=="number":
                frame.blit(pygame.font.Font(o["args"]["font"],int(o["args"]["scale"])).render(nvars[o["args"]["number"]],True,(255,255,255)),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
            if o["args"]["ltype"]=="text":
                frame.blit(pygame.font.Font(o["args"]["font"],int(o["args"]["scale"])).render(o["args"]["text"],True,(255,255,255)),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
        if o["type"]=="collision":
            if devmode==True:
                pygame.draw.rect(frame,(0,0,255),(int(o["args"]["x1"]),int(o["args"]["x2"])-int(o["args"]["x1"]),int(o["args"]["y1"]),int(o["args"]["y2"])-int(o["args"]["y1"])),10)
        if o["type"]=="bg":
            wasanim=False
            for a in asys.anims:
                if asys.anims[a]["objid"]==o["id"] and asys.anims[a]["active"]==True:
                    frame.blit(pygame.transform.scale(pygame.image.load("textures/"+asys.anims[a]["frames"][int(asys.anims[a]["current_frame"])]),(int(500),int(500))),(int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[0]),int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[1])))
                    if asys.anims[a]["current_frame"]<len(asys.anims[a]["frames"])-1:
                        asys.anims[a]["current_frame"]+=0.05
                    elif asys.anims[a]["isloop"]==True:
                        asys.anims[a]["current_frame"]=0
                    else:
                        asys.anims[a]["active"]=False
                        asys.anims[a]["current_frame"]=0
                    wasanim=True
            if wasanim==False:frame.blit(pygame.transform.scale(pygame.image.load(o["args"]["img"]),(500,500)),(0,0))
        if o["type"]=="NPC":
            wasanim=False
            for a in asys.anims:
                #print(asys.anims)
                if asys.anims[a]["objid"]==o["id"] and asys.anims[a]["active"]==True:
                    frame.blit(pygame.transform.scale(pygame.image.load("textures/"+asys.anims[a]["frames"][int(asys.anims[a]["current_frame"])]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[0]),int(o["args"]["pos"].split(",")[1])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[1])))
                    if asys.anims[a]["current_frame"]<len(asys.anims[a]["frames"])-1:
                        asys.anims[a]["current_frame"]+=0.05
                    elif asys.anims[a]["isloop"]==True:
                        asys.anims[a]["current_frame"]=0
                    else:
                        asys.anims[a]["active"]=False
                        asys.anims[a]["current_frame"]=0
                    wasanim=True
            if wasanim==False:frame.blit(pygame.transform.scale(pygame.image.load(o["args"]["front"]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
        if o["type"]=="trigger":
            if devmode==True:
                pygame.draw.rect(frame,(255,0,0),(int(o["args"]["x1"]),int(o["args"]["x2"])-int(o["args"]["x1"]),int(o["args"]["y1"]),int(o["args"]["y2"])-int(o["args"]["y1"])),10)
            statement=True
            keystat=True
            try:
                if not ckey==o["args"]["key"]:
                    keystat=False
            except:cbjhswde=0
            try:
                if o["args"]["operator"]=="=":
                    if not svars[o["args"]["v1"]]==svars[o["args"]["v2"]]:
                        statement=False
                if o["args"]["operator"]=="==":
                    if not nvars[o["args"]["v1"]]==nvars[o["args"]["v2"]]:
                        statement=False
                if o["args"]["operator"]==">=":
                    if not nvars[o["args"]["v1"]]>=nvars[o["args"]["v2"]]:
                        statement=False
                if o["args"]["operator"]=="<=":
                    if not nvars[o["args"]["v1"]]<=nvars[o["args"]["v2"]]:
                        statement=False
            except:ajajjajajajajajJA=0
            ox=0
            oy=0
            if o["args"]["taoid"]=="player":
                ox=px
                oy=py
            else:
                for obbb in objects:
                    if obbb.id==o["args"]["taoid"]:
                        try:
                            ox,oy=obbb.obj_args["pos"].split(",")
                        except:
                            ox,oy=0,0
            maxacts=0
            try:
                aaaaaaaaa=ob.obj_args["activatedtimes"]
            except:
                ob.obj_args["activatedtimes"]=0
            if ob.obj_args["maxactivs"]=="inf":
                maxacts=ob.obj_args["activatedtimes"]+10
            else:
                maxacts=int(ob.obj_args["maxactivs"])
            if keystat == True and statement == True and int(ox) in range(int(o["args"]["x1"]),int(o["args"]["x2"])) and int(oy) in range(int(o["args"]["y1"]),int(o["args"]["y2"])) and ob.obj_args["activatedtimes"]<=maxacts:
                ob.obj_args["activatedtimes"]+=1
                if o["args"]["trigtype"]=="sound":
                    if o["args"]["loop"]=="False":
                        snd=pygame.mixer.Sound(o["args"]["sound"])
                        snd.play()
                        sounds.append(snd)
                    else:
                        snd=pygame.mixer.music(o["args"]["sound"])
                        snd.play()
                        sounds.append(snd)
                if o["args"]["trigtype"]=="vchange":
                    if o["args"]["ctype"]=="+":
                        if o["args"]["vtype"]=="string":
                            svars[o["args"]["v1"]]=svars[o["args"]["v1"]]+svars[o["args"]["v2"]]
                        else:
                            nvars[o["args"]["v1"]]+=nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="=":
                        if o["args"]["vtype"]=="string":
                            svars[o["args"]["v1"]]=svars[o["args"]["v2"]]
                        else:
                            nvars[o["args"]["v1"]]=nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="-":
                        nvars[o["args"]["v1"]]=nvars[o["args"]["v1"]]-nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="*":
                        nvars[o["args"]["v1"]]=nvars[o["args"]["v1"]]*nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="/":
                        nvars[o["args"]["v1"]]=nvars[o["args"]["v1"]]/nvars[o["args"]["v2"]]
                if o["args"]["trigtype"]=="animation":
                    asys.start_anim(o["args"]["anim"])
                    #pygame.draw.rect(frame,(255,255,0),(int(o["args"]["x1"]),int(o["args"]["x2"]),int(o["args"]["1"]),int(o["args"]["x2"])))
                elif o["args"]["trigtype"]=="dialog":
                    for d in dialogsl:
                        if d.id==o["args"]["dialog"]:
                            d.start()
                elif o["args"]["trigtype"]=="move":
                    #print("m "+o["args"]["moid"])
                    if o["args"]["moid"]=="player":
                        px+=int(o["args"]["xm"])
                        py+=int(o["args"]["ym"])
                    else:
                        #print("b")
                        for obbb in objects:
                            if o["args"]["moid"]==obbb.getobj()["id"]:
                                try:
                                    opos=obbb.obj_args["pos"].split(",")
                                    nposx,nposy=opos
                                    npos=str(int(nposx)+int(o["args"]["xm"]))+","+str(int(nposy)+int(o["args"]["ym"]))
                                    obbb.obj_args["pos"]=npos
                                except:adjsdjs=0
        if o["type"]=="door":
            if devmode==True:
                pygame.draw.rect(frame,(0,255,0),((int(o["args"]["x1"]),int(o["args"]["x2"])-int(o["args"]["x1"]),int(o["args"]["y1"]),int(o["args"]["y2"])-int(o["args"]["y1"]))),10)
            x1=int(o["args"]["x1"])
            x2=int(o["args"]["x2"])
            y1=int(o["args"]["y1"])
            y2=int(o["args"]["y2"])
            try:
                x1=x1+int(o["args"]["pos"].split(",")[0])
                x2=x2+int(o["args"]["pos"].split(",")[0])
                y1=y1+int(o["args"]["pos"].split(",")[1])
                y2=y2+int(o["args"]["pos"].split(",")[1])
            except:ffdfd=0
            if int(px) in range(int(x1),int(x2)) and int(py) in range(y1,y2):
                loadmap(o["args"]["map"])
                try:
                    loadanims(o["args"]["map"]+".anims")
                    loaddialogs(o["args"]["map"]+".dialogs")
                except:
                    aaaaaaaaaaa=0
                try:
                    if o["args"]["save"]=="True":
                        with open("save.txt","w") as sf:
                            sf.writelines([o["args"]["map"])
                except:drtrjdjjs=0
        if o["type"]=="image":
            wasanim=False
            for a in asys.anims:
                #print(asys.anims)
                if asys.anims[a]["objid"]==o["id"] and asys.anims[a]["active"]==True:
                    frame.blit(pygame.transform.scale(pygame.image.load("textures/"+asys.anims[a]["frames"][int(asys.anims[a]["current_frame"])]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[0]),int(o["args"]["pos"].split(",")[1])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[1])))
                    if asys.anims[a]["current_frame"]<len(asys.anims[a]["frames"])-1:
                        asys.anims[a]["current_frame"]+=0.05
                    elif asys.anims[a]["isloop"]==True:
                        asys.anims[a]["current_frame"]=0
                    else:
                        asys.anims[a]["active"]=False
                        asys.anims[a]["current_frame"]=0
                    wasanim=True
            if wasanim==False:frame.blit(pygame.transform.scale(pygame.image.load(o["args"]["front"]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
        if o["type"]=="NPC":
            wasanim=False
            for a in asys.anims:
                #print(asys.anims)
                if asys.anims[a]["objid"]==o["id"] and asys.anims[a]["active"]==True:
                    frame.blit(pygame.transform.scale(pygame.image.load("textures/"+asys.anims[a]["frames"][int(asys.anims[a]["current_frame"])]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[0]),int(o["args"]["pos"].split(",")[1])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[1])))
                    if asys.anims[a]["current_frame"]<len(asys.anims[a]["frames"])-1:
                        asys.anims[a]["current_frame"]+=0.05
                    elif asys.anims[a]["isloop"]==True:
                        asys.anims[a]["current_frame"]=0
                    else:
                        asys.anims[a]["active"]=False
                        asys.anims[a]["current_frame"]=0
                    wasanim=True
            if wasanim==False:frame.blit(pygame.transform.scale(pygame.image.load(o["args"]["front"]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
    if move==False:
        if dir==3:frame.blit(pygame.transform.scale(pygame.image.load("textures/player/pidle.png"),psi),(px,py))
        if dir==2:frame.blit(pygame.transform.scale(pygame.image.load("textures/player/pidlel.png"),psi),(px,py))
        if dir==1:frame.blit(pygame.transform.scale(pygame.image.load("textures/player/pidler.png"),psi),(px,py))
        if dir==0:frame.blit(pygame.transform.scale(pygame.image.load("textures/player/pidleb.png"),psi),(px,py))
    else:
        if curstep<=3.9:curstep+=0.1
        else:curstep=1.0
        if dir==3:frame.blit(pygame.transform.scale(pygame.image.load("textures/player/pstepfw"+str(int(curstep))+".png"),psi),(px,py))
        if dir==2:frame.blit(pygame.transform.scale(pygame.image.load("textures/player/pstepl"+str(int(curstep))+".png"),psi),(px,py))
        if dir==1:frame.blit(pygame.transform.scale(pygame.image.load("textures/player/pstepr"+str(int(curstep))+".png"),psi),(px,py))
        if dir==0:frame.blit(pygame.transform.scale(pygame.image.load("textures/player/pstepb"+str(int(curstep))+".png"),psi),(px,py))
    for ob in objup:
        o=ob.getobj()
        if o["type"]=="label":
            if o["args"]["ltype"]=="string":
                frame.blit(pygame.font.Font(o["args"]["font"],int(o["args"]["scale"])).render(svars[o["args"]["string"]],True,(255,255,255)),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
            if o["args"]["ltype"]=="number":
                frame.blit(pygame.font.Font(o["args"]["font"],int(o["args"]["scale"])).render(nvars[o["args"]["number"]],True,(255,255,255)),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
            if o["args"]["ltype"]=="text":
                frame.blit(pygame.font.Font(o["args"]["font"],int(o["args"]["scale"])).render(o["args"]["text"],True,(255,255,255)),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
        if o["type"]=="collision":
            if devmode==True:
                pygame.draw.rect(frame,(0,0,255),(int(o["args"]["x1"]),int(o["args"]["x2"])-int(o["args"]["x1"]),int(o["args"]["y1"]),int(o["args"]["y2"])-int(o["args"]["y1"])),10)
        if o["type"]=="door":
            if devmode==True:
                pygame.draw.rect(frame,(0,255,0),((int(o["args"]["x1"]),int(o["args"]["x2"])-int(o["args"]["x1"]),int(o["args"]["y1"]),int(o["args"]["y2"])-int(o["args"]["y1"]))),10)
            x1=int(o["args"]["x1"])
            x2=int(o["args"]["x2"])
            y1=int(o["args"]["y1"])
            y2=int(o["args"]["y2"])
            try:
                x1=x1+int(o["args"]["pos"].split(",")[0])
                x2=x2+int(o["args"]["pos"].split(",")[0])
                y1=y1+int(o["args"]["pos"].split(",")[1])
                y2=y2+int(o["args"]["pos"].split(",")[1])
            except:ffdfd=0
            if int(px) in range(int(x1),int(x2)) and int(py) in range(y1,y2):
                loadmap(o["args"]["map"])
                try:
                    loadanims(o["args"]["map"]+".anims")
                    loaddialogs(o["args"]["map"]+".dialogs")
                except:aajajajajajaaj=0
                try:
                    if o["args"]["save"]=="True":
                        with open("save.txt","w") as sf:
                            sf.writelines([o["args"]["map"])
                except:drtrjdjjs=0
        if o["type"]=="trigger":
            if devmode==True:
                pygame.draw.rect(frame,(255,0,0),(int(o["args"]["x1"]),int(o["args"]["x2"])-int(o["args"]["x1"]),int(o["args"]["y1"]),int(o["args"]["y2"])-int(o["args"]["y1"])),10)
            statement=True
            keystat=True
            try:
                if not ckey==o["args"]["key"]:
                    keystat=False
            except:cbjhswde=0
            try:
                if o["args"]["operator"]=="=":
                    if not svars[o["args"]["v1"]]==svars[o["args"]["v2"]]:
                        statement=False
                if o["args"]["operator"]=="==":
                    if not nvars[o["args"]["v1"]]==nvars[o["args"]["v2"]]:
                        statement=False
                if o["args"]["operator"]==">=":
                    if not nvars[o["args"]["v1"]]>=nvars[o["args"]["v2"]]:
                        statement=False
                if o["args"]["operator"]=="<=":
                    if not nvars[o["args"]["v1"]]<=nvars[o["args"]["v2"]]:
                        statement=False
            except:ajajjajajajajajJA=0
            ox=0
            oy=0
            if o["taoid"]=="player":
                ox=px
                oy=py
            else:
                for obbb in objects:
                    if obbb.id==o["taoid"]:
                        try:
                            ox,oy=obbb.obj_args["pos"].split(",")
                        except:
                            ox,oy=0,0
            maxacts=0
            try:
                aaaaaaaaa=ob.obj_args["activatedtimes"]
            except:
                ob.obj_args["activatedtimes"]=0
            if ob.maxactivs=="inf":
                maxacts=ob.obj_args["activatedtimes"]+10
            else:
                maxacts=int(ob.obj_args["maxactivs"])
            if keystat==True and statement==True and int(ox) in range(int(o["args"]["x1"]),int(o["args"]["x2"])) and int(oy) in range(int(o["args"]["y1"]),int(o["args"]["y2"])) and ob.obj_args["activatedtimes"]<=maxacts:
                ob.obj_args["activatedtimes"]+=1
                if o["args"]["trigtype"]=="sound":
                    if o["args"]["loop"]=="False":
                        snd=pygame.mixer.Sound(o["args"]["sound"])
                        snd.play()
                        sounds.append(snd)
                    else:
                        snd=pygame.mixer.music(o["args"]["sound"])
                        snd.play()
                        sounds.append(snd)
                if o["args"]["trigtype"]=="vchange":
                    if o["args"]["ctype"]=="+":
                        if o["args"]["vtype"]=="string":
                            svars[o["args"]["v1"]]=svars[o["args"]["v1"]]+svars[o["args"]["v2"]]
                        else:
                            nvars[o["args"]["v1"]]+=nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="=":
                        if o["args"]["vtype"]=="string":
                            svars[o["args"]["v1"]]=svars[o["args"]["v2"]]
                        else:
                            nvars[o["args"]["v1"]]=nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="+":
                        if o["args"]["vtype"]=="string":
                            svars[o["args"]["v1"]]=svars[o["args"]["v1"]]+svars[o["args"]["v2"]]
                        else:
                            nvars[o["args"]["v1"]]+=nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="=":
                        if o["args"]["vtype"]=="string":
                            svars[o["args"]["v1"]]=svars[o["args"]["v2"]]
                        else:
                            nvars[o["args"]["v1"]]=nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="-":
                        nvars[o["args"]["v1"]]=nvars[o["args"]["v1"]]-nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="*":
                        nvars[o["args"]["v1"]]=nvars[o["args"]["v1"]]*nvars[o["args"]["v2"]]
                    if o["args"]["ctype"]=="/":
                        nvars[o["args"]["v1"]]=nvars[o["args"]["v1"]]/nvars[o["args"]["v2"]]
                if o["args"]["trigtype"]=="animation":
                    asys.start_anim(o["args"]["anim"])
                elif o["args"]["trigtype"]=="dialog":
                    for d in dialogsl:
                        if d.id==o["args"]["dialog"]:
                            d.start()
                elif o["args"]["trigtype"]=="move":
                    if o["args"]["moid"]=="player":
                        px+=int(o["args"]["xm"])
                        py+=int(o["args"]["ym"])
                    else:
                        for obbb in objects:
                            if o["args"]["moid"]==obbb.getobj()["id"]:
                                try:
                                    opos=obbb.obj_args["pos"].split(",")
                                    nposx,nposy=opos
                                    npos=str(int(nposx)+int(o["args"]["xm"]))+","+str(int(nposy)+int(o["args"]["ym"]))
                                    obbb.obj_args["pos"]=npos
                                    #print("moved "+o["args"]["moid"]+"to" + npos)
                                except:print("error")
        if o["type"]=="image":
            wasanim=False
            for a in asys.anims:
                #print(asys.anims)
                if asys.anims[a]["objid"]==o["id"] and asys.anims[a]["active"]==True:
                    frame.blit(pygame.transform.scale(pygame.image.load("textures/"+asys.anims[a]["frames"][int(asys.anims[a]["current_frame"])]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[0]),int(o["args"]["pos"].split(",")[1])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[1])))
                    if asys.anims[a]["current_frame"]<len(asys.anims[a]["frames"])-1:
                        asys.anims[a]["current_frame"]+=0.05
                    elif asys.anims[a]["isloop"]==True:
                        asys.anims[a]["current_frame"]=0
                    else:
                        asys.anims[a]["active"]=False
                        asys.anims[a]["current_frame"]=0
                    wasanim=True
            if wasanim==False:frame.blit(pygame.transform.scale(pygame.image.load(o["args"]["front"]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
        if o["type"]=="NPC":
            wasanim=False
            for a in asys.anims:
                #print(asys.anims)
                if asys.anims[a]["objid"]==o["id"] and asys.anims[a]["active"]==True:
                    frame.blit(pygame.transform.scale(pygame.image.load("textures/"+asys.anims[a]["frames"][int(asys.anims[a]["current_frame"])]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[0]),int(o["args"]["pos"].split(",")[1])+int(asys.anims[a]["deltaposs"][int(asys.anims[a]["current_frame"])].split(";")[1])))
                    if asys.anims[a]["current_frame"]<len(asys.anims[a]["frames"])-1:
                        asys.anims[a]["current_frame"]+=0.05
                    elif asys.anims[a]["isloop"]==True:
                        asys.anims[a]["current_frame"]=0
                    else:
                        asys.anims[a]["active"]=False
                        asys.anims[a]["current_frame"]=0
                    wasanim=True
            if wasanim==False:frame.blit(pygame.transform.scale(pygame.image.load(o["args"]["front"]),(int(o["args"]["scale"].split(",")[0]),int(o["args"]["scale"].split(",")[1]))),(int(o["args"]["pos"].split(",")[0]),int(o["args"]["pos"].split(",")[1])))
    for d in dialogsl:
        if d.active==True:
            move=False
            pygame.draw.rect(frame,(255,255,255),(0,350,500,500))
            pygame.draw.rect(frame,(0,0,0),(10,340,490,490))
            fnt1 = pygame.font.Font("arialmt.ttf",10)
            fnt2 = pygame.font.Font("arialmt.ttf",30)
            frame.blit(fnt1.render(d.name,True,(255,255,255)),(10,340))
            frame.blit(fnt2.render(d.phrases[d.phrase],True,(255,255,255)),(10,360))
            for e in pygame.event.get():
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_RETURN: d.nextphrase()
                    break
            if d.phrase==len(d.phrases):
                d.active=False
                d.phrase=0
    if devmode==True:
        frame.blit(pygame.font.Font("arialmt.ttf",10).render(str(px)+"  "+str(py),True,(255,255,255)),(0,0))
        print(pygame.mouse.get_pos())
    pygame.display.update()
    #for o in objects:
    #    print(o.getobj())
