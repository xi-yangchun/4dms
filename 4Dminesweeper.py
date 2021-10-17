import pygame
import random
from pygame.locals import*
import sys

pygame.init()                                             # Pygameの初期化
screen = pygame.display.set_mode((630, 520))
clock = pygame.time.Clock() # クロックの設定。異なるPCで異なる速さの動作になることを防ぐ
pygame.display.set_caption("4D MINESWEEPER")                     # タイトルバーに表示する文字
img_bomb=pygame.image.load('datafile_4dms\\bomb.png')
img_bomb=pygame.transform.scale(img_bomb,(32,32))
pygame.display.set_icon(img_bomb)

class Linked_State:
    def __init__(self,parent,model):
        self.focused=False
        self.linklis=[]
        self.sublis=[]
        self.parent=parent
        self.model=model
        self.view=None
    
    def add_link(self,sobj):
        self.linklis.append(sobj)
    
    def add_substate(self,sobj):
        self.sublis.append(sobj)
    
    def focus(self):
        self.focused=True
    
    def add_model(self,model):
        self.model=model
    
    def set_view(self):
        return None
    
    def defocus(self):
        self.focused=False
    
    def submove(self,i):
        for a in range(len(self.sublis)):
            self.sublis[a].focused=False
        self.sublis[i].focused=True
    
    def get_focused(self):
        return self.focused
    
    def move(self,i):
        self.defocus()
        self.linklis[i].focus()
    
    def view_reinit(self,i):
        self.linklis[i].view.reinit()
    
    def act(self,s):
        return None
    
    def show(self):
        return None

class StateMachine:
    def __init__(self,model):
            self.statelis=[]
            self.model=model
            self.curstate=0
            self.mx=0
            self.my=0
    
    def add_state(self,sobj):
        self.statelis.append(sobj)
    
    def set_mpos(self,ax,ay):
        self.mx=ax
        self.my=ay
    
    def get_mpos(self):
        return (self.mx,self.my)
    
    def input_to_mes(self):
        ev=pygame.event.get()
        receive='not_det'
        for a in ev:
            if a.type==pygame.KEYDOWN:
                if a.key==97:#A
                    receive='left'
                elif a.key==119:#W
                    receive='up'
                elif a.key==100:#D
                    receive='right'
                elif a.key==115:#S
                    receive='down'
                elif a.key==122:
                    receive='det'
            if a.type==pygame.MOUSEBUTTONDOWN:
                if a.button==1:
                    receive='click_left'
                elif a.button==3:
                    receive='click_right'
                ax,ay=a.pos
                self.set_mpos(ax,ay)
                
        return receive
    
    def act(self):
        s=self.input_to_mes()
        if self.statelis[self.curstate].get_focused()==True:
            self.statelis[self.curstate].act(s)
        else:
            c=0
            for a in self.statelis:
                if a.get_focused()==True:
                    a.act(s)
                    self.curstate=c
                    break
                c+=1
    
    def show(self):
        if self.statelis[self.curstate]\
        .get_focused()==True:
            self.statelis[self.curstate].show()
        else:
            c=0
            for a in self.statelis:
                if a.get_focused()==True:
                    a.show()
                    self.curstate=c
                    break
                c+=1

class Model:
    def __init__(self):
        return None

class View:
    def __init__(self,parent,model):
        self.parent=parent
        self.model=model
    
    def act(self,receive):
        return None
    
    def show(self):
        return None

class MS_Model(Model):
    def __init__(self):
        self.length=4
        l=self.length
        
        self.arr_neighbor\
        =[[[[0 for a in range(l)] for b in range(l)]
        for c in range(l)] for d in range(l)]
        
        self.arr_bomb\
        =[[[[0 for a in range(l)] for b in range(l)]
        for c in range(l)] for d in range(l)]

        self.arr_flag\
        =[[[[0 for a in range(l)] for b in range(l)]
        for c in range(l)] for d in range(l)]

        self.arr_digged\
        =[[[[0 for a in range(l)] for b in range(l)]
        for c in range(l)] for d in range(l)]

        self.sum_bombs=0
        self.sum_flags=0
        self.rest_bombs=0
        self.rest_flags=0
        self.sum_digged=0
    
    def clear_arrays(self):
        l=self.length
        self.arr_neighbor\
        =[[[[0 for a in range(l)] for b in range(l)]
        for c in range(l)] for d in range(l)]
        
        self.arr_bomb\
        =[[[[0 for a in range(l)] for b in range(l)]
        for c in range(l)] for d in range(l)]

        self.arr_flag\
        =[[[[0 for a in range(l)] for b in range(l)]
        for c in range(l)] for d in range(l)]

        self.arr_digged\
        =[[[[0 for a in range(l)] for b in range(l)]
        for c in range(l)] for d in range(l)]
    
    def set_sum_rest(self,num):
        self.sum_bombs=num
        self.sum_flags=num
        self.rest_bombs=num
        self.rest_flags=num
    
    def put_bombs(self):
        for a in range(self.sum_bombs):
            while True:
                v=random.randint(0,self.length-1)
                w=random.randint(0,self.length-1)
                x=random.randint(0,self.length-1)
                y=random.randint(0,self.length-1)
                if self.arr_bomb[v][w][x][y]==0:
                    self.arr_bomb[v][w][x][y]=1
                    break
    
    def count_neighbor(self):
        for v in range(self.length):
            for w in range(self.length):
                for x in range(self.length):
                    for y in range(self.length):
                        if self.arr_bomb[v][w][x][y]==1:
                            for dv in range(-1,2):
                                for dw in range(-1,2):
                                    for dx in range(-1,2):
                                        for dy in range(-1,2):
                                            bv=(v+dv>=0 and v+dv<=self.length-1)
                                            bw=(w+dw>=0 and w+dw<=self.length-1)
                                            bx=(x+dx>=0 and x+dx<=self.length-1)
                                            by=(y+dy>=0 and y+dy<=self.length-1)
                                            if bv and bw and bx and by:
                                                self.arr_neighbor[v+dv][w+dw][x+dx][y+dy]+=1
    
    def moredig(self,metay,metax,y,x):
        if self.arr_flag[metay][metax][y][x]==1:
            return None
        if self.arr_digged[metay][metax][y][x]==0:
            self.arr_digged[metay][metax][y][x]=1
            self.sum_digged+=1
            if self.arr_neighbor[metay][metax][y][x]>0:
                return None
        for dmy in range(-1,2):
            for dmx in range(-1,2):
                for dy in range(-1,2):
                    for dx in range(-1,2):
                        if dmy==0 and dmx==0 and y==0 and x==0:
                            p=None
                        else:
                            bmy=(metay+dmy>=0 and metay+dmy<=self.length-1)
                            bmx=(metax+dmx>=0 and metax+dmx<=self.length-1)
                            by=(y+dy>=0 and y+dy<=self.length-1)
                            bx=(x+dx>=0 and x+dx<=self.length-1)
                            if bmy and bmx and by and bx:
                                if self.arr_digged[metay+dmy][metax+dmx][y+dy][x+dx]==0:
                                    p=self.moredig(metay+dmy,metax+dmx,y+dy,x+dx)
        return None
    
    def end_digged_bomb(self):
        for a in range(self.length):
            for b in range(self.length):
                for c in range(self.length):
                    for d in range(self.length):
                        if self.arr_bomb[a][b][c][d]==1 and self.arr_digged[a][b][c][d]==1:
                            self.arr_bomb[a][b][c][d]=0

    def dig_all_bomb(self):
        for a in range(self.length):
            for b in range(self.length):
                for c in range(self.length):
                    for d in range(self.length):
                        if self.arr_bomb[a][b][c][d]==1:
                            self.arr_digged[a][b][c][d]=1

class V_Click_To_Start(View):
    def __init__(self,parent,model):
        self.parent=parent
        self.model=model
        self.fontlis=[]
        fn=pygame.font.SysFont('hg創英角ｺﾞｼｯｸubhgp創英角ｺﾞｼｯｸubhgs創英角ｺﾞｼｯｸub',30)
        self.fontlis.append(fn.render('四次元マインスイーパー',False,(255,200,0)))
        self.fontlis.append(fn.render('左クリックで開始',False,(255,200,0)))
        self.img_bg=pygame.image\
        .load('datafile_4dms\\titlebg.png')

    def act(self,receive):
        if receive=='click_left':
            return 'start'
        else:
            return 'not_det'
    
    def show(self):
        screen.blit(self.img_bg,(0,0))
        screen.blit(self.fontlis[0],(150,210))
        screen.blit(self.fontlis[1],(180,250))

class S_Click_To_Start(Linked_State):
    def __init__(self,parent,model):
        self.focused=False
        self.linklis=[]
        self.parent=parent
        self.model=model
        self.view=V_Click_To_Start(self,self.model)

    def act(self,receive):
        s=self.view.act(receive)
        if s=='start':
            self.move(0)
    
    def show(self):
        self.view.show()

class S_Setup_BF(Linked_State):
    def __init__(self,parent,model):
        self.focused=False
        self.linklis=[]
        self.parent=parent
        self.model=model
        self.view=None

    def act(self,receive):
        self.model.clear_arrays()
        self.model.set_sum_rest(random.randint(4,8))
        self.model.put_bombs()
        self.model.count_neighbor()
        self.model.sum_digged=0
        self.move(0)
    
    def show(self):
        return None

class V_PlayMain(View):
    def __init__(self,parent,model):
        self.parent=parent
        self.model=model
        self.masu=26
        self.dx=200
        self.dy=10
        self.metay=0
        self.metax=0
        self.y=0
        self.x=0
        self.img_bomb=pygame.image\
        .load('datafile_4dms\\bomb.png')
        self.img_fire=pygame.image\
        .load('datafile_4dms\\fire.png')
        self.img_flag=pygame.image\
        .load('datafile_4dms\\flag.png')
        self.img_bomb=pygame.transform.scale(self.img_bomb,(self.masu,self.masu))
        self.img_fire=pygame.transform.scale(self.img_fire,(self.masu,self.masu))
        self.img_flag=pygame.transform.scale(self.img_flag,(self.masu,self.masu))

        self.fontsty=pygame.font.SysFont('hg創英角ｺﾞｼｯｸubhgp創英角ｺﾞｼｯｸubhgs創英角ｺﾞｼｯｸub',22)
        self.font=(self.fontsty.render('0',False,(0,0,0)))
        self.fontlis=[]
        self.fontlis.append(self.fontsty.render(
            '爆弾の総数:{}個'.format(0),False,(200,200,200)))
        self.fontlis.append(self.fontsty.render(
            '立てた旗:{}本'.format(0),False,(200,200,200)))
        self.fontlis.append(self.fontsty.render(
            '残りの旗:{}本'.format(0),False,(200,200,200)))
    
    def in_field(self,px,py):
        ppx=px-self.dx
        ppy=py-self.dy
        if ppx>=0 and ppx<=self.masu*self.model.length*self.model.length\
            and ppy>=0 and ppy<=self.masu*self.model.length*self.model.length:
            return True
        else:
            return False
    
    def get_arrpos(self,px,py):
        ppx=px-self.dx
        ppy=py-self.dy
        metax=0
        metay=0
        x=0
        y=0
        for a in range(self.model.length):
            if a*self.model.length*self.masu<=ppx and ppx<(a+1)*self.model.length*self.masu:
                metax=a
                ppx+=(-1)*a*self.model.length*self.masu
                break
        for a in range(self.model.length):
            if a*self.model.length*self.masu<=ppy and ppy<(a+1)*self.model.length*self.masu:
                metay=a
                ppy+=(-1)*a*self.model.length*self.masu
                break
        for a in range(self.model.length):
            if a*self.masu<=ppx and ppx<(a+1)*self.masu:
                x=a
                break
        for a in range(self.model.length):
            if a*self.masu<=ppy and ppy<(a+1)*self.masu:
                y=a
                break
        return [metay,metax,y,x]
    
    def get_savedpos(self):
        return [self.metay,self.metax,self.y,self.x]
    
    def draw_grid(self):
        l=self.model.length
        for a in range(l*l+1):
            pygame.draw.line(screen,(150,150,150),(a*self.masu+self.dx,self.dy)
            ,(a*self.masu+self.dx,l*l*self.masu+self.dy),1)
            pygame.draw.line(screen,(150,150,150),(self.dx,a*self.masu+self.dy)
            ,(l*l*self.masu+self.dx,a*self.masu+self.dy),1)

        for a in range(self.model.length+1):
            pygame.draw.line(screen,(150,150,150),(a*l*self.masu+self.dx,self.dy)
            ,(a*l*self.masu+self.dx,l*l*self.masu+self.dy),3)
            pygame.draw.line(screen,(150,150,150),(self.dx,a*l*self.masu+self.dy)
            ,(l*l*self.masu+self.dx,a*l*self.masu+self.dy),3)
    
    def draw_tile(self):
        l=self.model.length
        for my in range(l):
            for mx in range(l):
                for y in range(l):
                    for x in range(l):
                        r=pygame.Rect(self.dx+(l*mx+x)*self.masu,
                        self.dy+(l*my+y)*self.masu,self.masu,self.masu)
                        if self.model.arr_digged[my][mx][y][x]==0:
                            if self.model.arr_flag[my][mx][y][x]==1:
                                pygame.draw.rect(screen,(200,200,200),r)
                                screen.blit(self.img_flag,
                                (self.dx+(l*mx+x)*self.masu,
                                self.dy+(l*my+y)*self.masu))
                            else:
                                pygame.draw.rect(screen,(70,70,70),r)
                        else:
                            if self.model.arr_bomb[my][mx][y][x]==1:
                                pygame.draw.rect(screen,(250,240,0),r)
                                screen.blit(self.img_bomb,
                                (self.dx+(l*mx+x)*self.masu,
                                self.dy+(l*my+y)*self.masu))
                            else:
                                pygame.draw.rect(screen,(0,0,0),r)
                                num_bom=self.model.arr_neighbor[my][mx][y][x]
                                if num_bom>0:
                                    self.font=(self.fontsty.render(str(num_bom)
                                    ,False,(250,50,0)))
                                    screen.blit(self.font,
                                    (self.dx+(l*mx+x)*self.masu+3,
                                    self.dy+(l*my+y)*self.masu+1))

    def draw_property(self):
        self.fontlis[0]=self.fontsty.render(
            '爆弾の総数:{}個'.format(self.model.sum_bombs),
            False,(200,200,200))
        self.fontlis[1]=self.fontsty.render(
            '立てた旗:{}本'.format(self.model.sum_flags-self.model.rest_flags),
            False,(200,200,200))
        self.fontlis[2]=self.fontsty.render(
            '残りの旗:{}本'.format(self.model.rest_flags),
            False,(200,200,200))
        screen.blit(self.fontlis[0],(10,10))
        screen.blit(self.fontlis[1],(10,40))
        screen.blit(self.fontlis[2],(10,70))

    def act(self,receive):
        if receive=='click_left' or receive=='click_right':
            if receive=='click_left':
                receive='cl_in_field'
            elif receive=='click_right':
                receive='cr_in_field'
            p=self.parent.parent.get_mpos()
            px=p[0]
            py=p[1]
            if self.in_field(px,py)==True:
                s=self.get_arrpos(px,py)
                self.metay=s[0]
                self.metax=s[1]
                self.y=s[2]
                self.x=s[3]
                return receive
            else:
                return 'not_det'
        else:
            return 'not_det'
    
    def show(self):
        screen.fill((0,0,0))
        self.draw_tile()
        self.draw_grid()
        self.draw_property()

class S_PlayMain(Linked_State):
    def __init__(self,parent,model):
        self.focused=False
        #0:gameover, 1:gameclear 
        self.linklis=[]
        self.sublis=[]
        self.parent=parent
        self.model=model
        self.view=V_PlayMain(self,model)

    def act(self,receive):
        s=self.view.act(receive)
        if s=='cl_in_field':
            t=self.view.get_savedpos()
            dst=self.model.arr_digged[t[0]][t[1]][t[2]][t[3]]
            est=self.model.arr_flag[t[0]][t[1]][t[2]][t[3]]
            if dst==0 and est==0:
                self.model.moredig(t[0],t[1],t[2],t[3])
                if self.model.arr_bomb[t[0]][t[1]][t[2]][t[3]]==1:
                    self.move(0)
                else:
                    if self.model.sum_digged>=(self.model.length**4)-self.model.sum_bombs:
                        self.move(1)
        elif s=='cr_in_field':
            t=self.view.get_savedpos()
            dst=self.model.arr_flag[t[0]][t[1]][t[2]][t[3]]
            if dst==0 and self.model.rest_flags>0:
                self.model.arr_flag[t[0]][t[1]][t[2]][t[3]]=1
                self.model.rest_flags+=-1
            elif dst==1:
                self.model.arr_flag[t[0]][t[1]][t[2]][t[3]]=0
                self.model.rest_flags+=1
    
    def show(self):
        self.view.show()

class V_Gameover(V_PlayMain):
    def __init__(self,parent,model):
        self.parent=parent
        self.model=model
        self.masu=26
        self.dx=200
        self.dy=10
        self.counter=0

        self.fontsty=pygame.font.SysFont('hg創英角ｺﾞｼｯｸubhgp創英角ｺﾞｼｯｸubhgs創英角ｺﾞｼｯｸub',22)
        self.font=(self.fontsty.render('0',False,(0,0,0)))
        self.fontlis=[]
        self.fontsty2=pygame.font.SysFont('hg創英角ｺﾞｼｯｸubhgp創英角ｺﾞｼｯｸubhgs創英角ｺﾞｼｯｸub',30)
        self.fontlis.append(self.fontsty2.render('ゲームオーバー',False,(0,0,0)))
        self.fontlis.append(self.fontsty2.render('左クリックで再挑戦',False,(0,0,0)))

        self.img_bomb=pygame.image\
        .load('datafile_4dms\\bomb.png')
        self.img_fire=pygame.image\
        .load('datafile_4dms\\fire.png')
        self.img_flag=pygame.image\
        .load('datafile_4dms\\flag.png')
        self.img_bomb=pygame.transform.scale(self.img_bomb,(self.masu,self.masu))
        self.img_fire=pygame.transform.scale(self.img_fire,(self.masu,self.masu))
        self.img_flag=pygame.transform.scale(self.img_flag,(self.masu,self.masu))

        self.img_gov=pygame.image\
        .load('datafile_4dms\\gov.png')

    def act(self,receive):
        if self.counter<10:
            self.counter+=1
            return 'not_det'
        elif self.counter>=10 and self.counter<20:
            if self.counter==10:
                s='unit_fire'
            else:
                s='not_det'
            self.counter+=1
            return s
        elif self.counter>=20 and self.counter<30:
            if self.counter==20:
                s='bomb_leak'
            else:
                s='not_det'
            self.counter+=1
            return s
        elif self.counter>=30 and self.counter<40:
            if self.counter==30:
                s='all_fire'
            else:
                s='not_det'
            self.counter+=1
            return s
        else:
            if receive=='click_left':
                self.counter=0
                return 'retry'
    
    def draw_unit_fire(self):
        l=self.model.length
        for my in range(l):
            for mx in range(l):
                for y in range(l):
                    for x in range(l):
                        r=pygame.Rect(self.dx+(l*mx+x)*self.masu,
                        self.dy+(l*my+y)*self.masu,self.masu,self.masu)
                        if self.model.arr_digged[my][mx][y][x]==1:
                            if self.model.arr_bomb[my][mx][y][x]==1:
                                pygame.draw.rect(screen,(250,240,0),r)
                                screen.blit(self.img_fire,
                                (self.dx+(l*mx+x)*self.masu,
                                self.dy+(l*my+y)*self.masu))
    
    def show(self):
        if self.counter<10:
            screen.fill((0,0,0))
            self.draw_tile()
            self.draw_grid()
        elif self.counter>=10 and self.counter<20:
            screen.fill((0,0,0))
            self.draw_tile()
            self.draw_unit_fire()
            self.draw_grid()
        elif self.counter>=20 and self.counter<30:
            screen.fill((0,0,0))
            self.draw_tile()
            self.draw_grid()
        elif self.counter>=30 and self.counter<40:
            screen.fill((0,0,0))
            self.draw_tile()
            self.draw_unit_fire()
            self.draw_grid()
        else:
            screen.blit(self.img_gov,(0,0))
            screen.blit(self.fontlis[0],(200,210))
            screen.blit(self.fontlis[1],(180,260))

class S_Gameover(Linked_State):
    def __init__(self,parent,model):
        self.focused=False
        self.linklis=[]
        self.sublis=[]
        self.parent=parent
        self.model=model
        self.view=V_Gameover(self,self.model)
    
    def act(self,receive):
        s=self.view.act(receive)
        if s=='bomb_leak':
            self.model.end_digged_bomb()
            self.model.dig_all_bomb()
        if s=='retry':
            self.move(0)
    
    def show(self):
        self.view.show()

class V_Gameclear(V_PlayMain):
    def __init__(self,parent,model):
        self.parent=parent
        self.model=model
        self.masu=26
        self.dx=200
        self.dy=10
        self.counter=0

        self.fontsty=pygame.font.SysFont('hg創英角ｺﾞｼｯｸubhgp創英角ｺﾞｼｯｸubhgs創英角ｺﾞｼｯｸub',22)
        self.font=(self.fontsty.render('0',False,(0,0,0)))
        self.fontlis=[]
        self.fontsty2=pygame.font.SysFont('hg創英角ｺﾞｼｯｸubhgp創英角ｺﾞｼｯｸubhgs創英角ｺﾞｼｯｸub',30)
        self.fontlis.append(self.fontsty2.render('ゲームクリア',False,(255,200,0)))
        self.fontlis.append(self.fontsty2.render('左クリックで再挑戦',False,(255,200,0)))

        self.img_bomb=pygame.image\
        .load('datafile_4dms\\bomb.png')
        self.img_fire=pygame.image\
        .load('datafile_4dms\\fire.png')
        self.img_flag=pygame.image\
        .load('datafile_4dms\\flag.png')
        self.img_bomb=pygame.transform.scale(self.img_bomb,(self.masu,self.masu))
        self.img_fire=pygame.transform.scale(self.img_fire,(self.masu,self.masu))
        self.img_flag=pygame.transform.scale(self.img_flag,(self.masu,self.masu))

        self.img_bg=pygame.image\
        .load('datafile_4dms\\titlebg.png')
    
    def act(self,receive):
        if self.counter<10:
            self.counter+=1
            return 'not_det'
        else:
            if receive=='click_left':
                self.counter=0
                return 'retry'
    
    def show(self):
        if self.counter<10:
            screen.fill((0,0,0))
            self.draw_tile()
            self.draw_grid()
        else:
            screen.blit(self.img_bg,(0,0))
            screen.blit(self.fontlis[0],(200,210))
            screen.blit(self.fontlis[1],(180,260))

class S_Gameclear(Linked_State):
    def __init__(self,parent,model):
        self.focused=False
        self.linklis=[]
        self.sublis=[]
        self.parent=parent
        self.model=model
        self.view=V_Gameclear(self,self.model)
    
    def act(self,receive):
        s=self.view.act(receive)
        if s=='retry':
            self.move(0)
    
    def show(self):
        self.view.show()

model=MS_Model()
statemachine=StateMachine(model)
scts=S_Click_To_Start(statemachine,model)
statemachine.add_state(scts)
ssbn=S_Setup_BF(statemachine,model)
statemachine.add_state(ssbn)
scts.add_link(ssbn)
splm=S_PlayMain(statemachine,model)
statemachine.add_state(splm)
ssbn.add_link(splm)
sgov=S_Gameover(statemachine,model)
statemachine.add_state(sgov)
splm.add_link(sgov)
sgcl=S_Gameclear(statemachine,model)
statemachine.add_state(sgcl)
splm.add_link(sgcl)

sgov.add_link(ssbn)
sgcl.add_link(ssbn)

statemachine.statelis[0].focus()

p=False
while(p==False):
    clock.tick(20)
    screen.fill((200,200,200))
    statemachine.act()
    statemachine.show()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('unko')
            pygame.quit()
            sys.exit()