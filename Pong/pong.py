import tkinter as tk
from threading import Thread
import math
import random
from tkinter import font as tkFont
import time


class Pong:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.height = 800#int(self.screen_height*0.8)
        self.width = 1000#int(self.screen_width*0.7)

        self.line_width = 20
        self.gameover = False
        self.paused = False
        self.line1 = None   #CanvasID for line1
        self.line2 = None   #CanvasID for line2
        self.line_top = None
        self.line_bot = None
        self.ball = None    #CanvasID for ball
        self.goals1 = None
        self.goals2 = None
        #Einstellungen-----------------------
        self.line_length = 120  #self.height*0.15
        self.line_speed = 25
        self.ball_speed = 35
        self.player1_color = "white"
        self.player2_color = "white"
        self.frame_color = "white"
        self.ball_color = "white"
        self.background = "Black"
        self.single_player_left = False
        self.single_player_right = False
        #-------------------------------------

        self.ball_angle = 10
        self.goals_player1 = 0
        self.goals_player2 = 0
        self.line1up = False
        self.line1down = False
        self.line2up = False
        self.line2down = False
        
        self.font = tkFont.Font(family="Arial Black",size=int(40))

        self.root.geometry(f"{self.width}x{self.height}+{self.screen_width // 2 -self.width // 2}+{self.screen_height // 2 -self.height // 2}")
        self.root.bind("<KeyPress>",self.key_event_down)
        self.root.bind("<KeyRelease>",self.key_event_up)
        self.root.bind("<Key-p>", self.pause)
        #self.root.bind("<Escape>", self.pause)
        self.canvas = tk.Canvas(self.root, bg=self.background, width=self.width, height=self.height)
        self.canvas.pack()

        self.draw_field()
        self.draw_line1()
        self.draw_line2()
        self.draw_ball(300,300)

    def pause(self,event):
        if self.paused:
            self.paused = False
            self.update_gui()
        else:
            self.paused = True


    def draw_field(self):
        self.line_top = self.canvas.create_line(0,self.line_width//2,self.width,self.line_width//2, fill=self.frame_color, width=self.line_width)
        self.line_bot = self.canvas.create_line(0,self.height-self.line_width//2,self.width,self.height-self.line_width//2, fill=self.frame_color, width=self.line_width)
        self.line_mid = self.canvas.create_line(self.width//2,self.line_width*1.5,self.width//2,self.height, fill=self.frame_color, width=self.line_width//1.5, dash=self.line_width)
        self.goals1 = self.canvas.create_text(self.width*0.4,self.height*0.1, text=self.goals_player1, fill=self.frame_color, font=self.font)
        self.goals2 = self.canvas.create_text(self.width*0.6,self.height*0.1, text=self.goals_player2, fill=self.frame_color, font=self.font)

    def draw_line1(self):
        x = self.width*0.04
        length = self.line_length
        y = (self.height//2) - (length//2)
        if self.single_player_right:
            x = self.line_width/2
            y = self.line_width
            length = self.height - 2* self.line_width
        self.line1 = self.canvas.create_line(x,y,x,y+length, fill=self.player1_color,width=self.line_width)

    def draw_line2(self):
        x = self.width*0.96
        length = self.line_length
        y = (self.height//2) - (length//2)
        if self.single_player_left:
            x = self.width - self.line_width/2
            y = self.line_width
            length = self.height - 2* self.line_width
        self.line2 = self.canvas.create_line(x,y,x,y+length,fill=self.player2_color,width=self.line_width)

    def draw_ball(self, x ,y):
        self.ball = self.canvas.create_rectangle(x,y,x+self.line_width,y+self.line_width, fill=self.ball_color,outline=self.ball_color)


    def update_gui(self):
        if not self.gameover:
            event = self.root.after(30,self.update_gui)
            if self.paused:
                self.root.after_cancel(event)
            #---------------------------
            self.check_collision()
            self.move_ball()
            Thread(target=self.move1).start()
            Thread(target=self.move2).start()
            

    def move1(self):
        coords = self.canvas.coords(self.line1)
        if self.line1up:
            if coords[1] > self.line_width:
                self.canvas.move(self.line1,0,-self.line_speed)
        elif self.line1down:
            if coords[3] < self.height-self.line_width:
                self.canvas.move(self.line1,0,self.line_speed)

    def move2(self):
        coords = self.canvas.coords(self.line2)
        if self.line2up:
            if coords[1] > self.line_width:
                self.canvas.move(self.line2,0,-self.line_speed)
        elif self.line2down:
            if coords[3] < self.height-self.line_width:
                self.canvas.move(self.line2,0,self.line_speed)


    def move_ball(self):
        winkel_a = self.ball_angle
        winkel_b = 90
        winkel_c = 180 - winkel_b - winkel_a
        if winkel_c == 0:
            winkel_c += 1
        b = self.ball_speed
        x = b * math.sin(math.radians(winkel_c)) / math.sin(math.radians(winkel_b))
        y = x * math.sin(math.radians(winkel_a)) / math.sin(math.radians(winkel_c))
        self.canvas.move(self.ball,x,y)

    
    def check_collision(self):
        rand = random.randint(-50,50)
        c = self.canvas.coords(self.ball)
        overl = None
        overl = self.canvas.find_overlapping(c[0],c[1],c[2],c[3])
        if c[2] < 0:
            self.goals_player2 +=1
            self.canvas.itemconfig(self.goals2,text=self.goals_player2)
            self.canvas.moveto(self.ball, self.width*0.15,self.height*0.5)
            self.ball_angle = 0+rand
        elif c[0] > self.width:
            self.goals_player1 +=1
            self.canvas.itemconfig(self.goals1,text=self.goals_player1)
            self.canvas.moveto(self.ball, self.width*0.85,self.height*0.5)
            self.ball_angle = 180+rand
        if self.line_bot in overl or self.line_top in overl:
            self.ball_angle = 360 - self.ball_angle
        elif self.line1 in overl:
            self.ball_angle = 0 + rand
            #self.ball_angle = 180 - self.ball_angle + rand
        elif self.line2 in overl:
            self.ball_angle = 180 + rand


    def key_event_down(self, event):
        if event.keysym == "w":
            self.line1up = True
        elif event.keysym == "s":
            self.line1down = True
        elif event.keysym == "Up" or event.keysym == "o":
            self.line2up = True
        elif event.keysym == "Down" or event.keysym == "l":
            self.line2down = True
        

    def key_event_up(self, event):
        if event.keysym == "w":
            self.line1up = False
        elif event.keysym == "s":
            self.line1down = False
        elif event.keysym == "Up" or event.keysym == "o":
            self.line2up = False
        elif event.keysym == "Down" or event.keysym == "l":
            self.line2down = False

    

p = Pong()
p.update_gui()
p.root.mainloop()
