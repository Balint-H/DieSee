import blob_count as bc
from objc_util import *
from scene import *
import manu_pic as mp
from os import path
import os
import ui
import time
import console
    

global score
global flash
global thr
thr = 128
score = 0
flashG =False
class MyScene (Scene):
    def setup(self):
        global flashG
        self.background_color = '#445ea1'
        score_font = ('Futura', 60)
        self.score_label = LabelNode(str(score), score_font, parent=self)
        self.image_show = SpriteNode('processed.jpg', scale=0.3, parent=self)
        self.score_label.position = (self.size.w/4, self.size.h/3*2)
        self.image_show.z_position = 1
        self.image_show.position = (self.size.w/3*2, self.size.h/3*2)
        self.score_label.z_position = 1
        self.flash = flashG
        
        
    @ui.in_background
    def touch_began(self, touch):
        global score
        global flashG
        global thr
        mp.camera(flashG)
        time.sleep(0.1)
        score, im = bc.count_blobs(thr)
        self.image_show.texture = Texture(im)
        self.image_show.scale = 0.3
        self.score_label.text = str(score)
def flash_switch(sender):
    global flashG
    flashG = not flashG 
    
def slider_func(sender):
    global thr
    sender.superview['label'].text = str('{0:1.0f}'.format(sender.value*256))
    thr = sender.value*256
    score, im = bc.count_blobs(thr)
    sender.superview['tappy'].scene.image_show.texture = Texture(im)
    sender.superview['tappy'].scene.image_show.scale = 0.3
    sender.superview['tappy'].scene.score_label.text = str(score)

v = ui.load_view('DieSee.pyui')
v['tappy'].scene = MyScene()
v.present(orientations=['landscape'])



