from tkinter import *
from tkinter import messagebox
from math import *
import math
from random import *
from time import *

#переменные
MAX_X = 500
MAX_Y = 500
MIN_X = 0
MIN_Y = 0
indent = 20
BR = 0 #радиус шарика
CR = 0 #радиус большого шарика
BN = 0 #число маленьких шариков
CN = 0 #число больших шаров
BM = 0 #масса маленького шарика
CM = 0 #масса большого шарика
B_speed = 0 #начальная скорость маленьких шариков
C_speed = 0 #начальная скорость больших шариков
N_steps = 0
balls_array = []
balls_clustered = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
bar_chart = []
bar_chart_percents = []
time = 1
energy = 0
paint = True

#функции и классы
class Ball():
    def __init__(self, x, y, dx, dy, Radius, Mass, Color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.R = Radius
        self.m = Mass
        self.color = Color
        self.instance = canvas.create_oval(self.x-self.R,self.y-self.R,self.x+self.R,self.y+self.R,fill=self.color)
    def update_coords(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        #периодические граничные условия:
        if(self.x>MAX_X):
            self.x -= MAX_X-MIN_X
        if(self.x<MIN_X):
            self.x += MAX_X-MIN_X
        if(self.y>MAX_Y):
            self.y -= MAX_Y-MIN_Y
        if(self.y<MIN_Y):
            self.y += MAX_Y-MIN_Y
        if(paint==True):
            canvas.coords(self.instance, self.x-self.R, self.y-self.R, self.x+self.R, self.y+self.R)
            canvas.itemconfig(self.instance, fill=self.color)

def add_balls():
    i = 0
    while(i<BN):
        fi = uniform(0, math.pi*2)
        b = Ball(uniform(MIN_X,MAX_X),uniform(MIN_Y,MAX_Y),B_speed*sin(fi),B_speed*cos(fi),BR,BM,'blue')
        balls_array.append(b)
        collided = False
        j=0
        while(j<i):
            if(collision(j,i)==True):
                collided = True
            j+=1
        if(collided==False):
            i+=1
        else:
            canvas.delete(balls_array[i].instance)
            del balls_array[i]

def add_big_balls():
    i = 0
    while(i<CN):
        fi = uniform(0, math.pi*2)
        b = Ball(uniform(MIN_X,MAX_X),uniform(MIN_Y,MAX_Y),C_speed*sin(fi),C_speed*cos(fi),CR,CM,'yellow')
        balls_array.append(b)
        collided = False
        j=0
        while(j<i):
            if(collision(j+BN,i+BN)==True):
                collided = True
            j+=1
        if(collided==False):
            i+=1
        else:
            canvas.delete(balls_array[i+BN].instance)
            del balls_array[i+BN]

def paint_clusters():
    i = BN
    while(i<BN+CN):
        j = BN
        i_in_cluster = False
        while(j<BN+CN):
            if(cluster(i,j)==True):
                i_in_cluster = True
            j += 1
        if(i_in_cluster == True):
            balls_array[i].color = 'Red'
        else:
            balls_array[i].color = 'Yellow'
        i += 1

def main_loop():
    for i in range(BN+CN):
        balls_array[i].update_coords()
    for i in range(BN+CN):
        j = i
        while(j<BN+CN):
            if(collision(i,j)==True):
                resolve_collision(i, j)
            j += 1

    paint_clusters()
    calc_energy()
    calc_impuls()
    calc_clusters()
    global time
    time += 1
    label3.config(text='время =' + str(time))
    if (time==N_steps):
        save_percents()
        messagebox.showinfo('статистика сохранена!')
    root.after(1, main_loop)

def set_labels():
    global label1, label2, label3
    label1 = Label(root, text='initial text', justify = LEFT)
    label1.place(x = MAX_X+20, y = indent)
    label2 = Label(root, text='initial text', justify = LEFT)
    label2.place(x = MAX_X+20, y = indent*2)
    label3 = Label(root, text='объемная доля маленьких ='+str((math.pi*BR*BR*BN)/((MAX_X-MIN_X)*(MAX_Y-MIN_Y))), justify = LEFT)
    label3.place(x = MAX_X+20, y = indent*3)
    label4 = Label(root, text='объемная доля больших ='+str((math.pi*CR*CR*CN)/((MAX_X-MIN_X)*(MAX_Y-MIN_Y))), justify = LEFT)
    label4.place(x = MAX_X+20, y = indent*4)

    #оси координат для графика
    canvas.create_line(indent,700,indent,MAX_Y+indent,arrow=LAST)
    canvas.create_line(indent,700,MAX_X,700,arrow=LAST)
    for i in range (20):
        g = canvas.create_rectangle(indent*(i+1), MAX_Y+200-balls_clustered[i]*100/time, indent*(i+2), MAX_Y+200, fill='skyblue')
        bar_chart.append(g)
        canvas.create_text(indent*(i+1.5), MAX_Y+210, text = str(i), fill="black", font=("Helvectica", "10"))
        p = canvas.create_text(indent*(i+1.5), MAX_Y+200-balls_clustered[i]*100/time-10, text = str(balls_clustered[i]*100/time), fill="black", font=("Helvectica", "8"))
        bar_chart_percents.append(p)

def calc_energy():
    global energy
    energy = 0
    for a in range (BN+CN):
        energy += balls_array[a].dx*balls_array[a].dx*balls_array[a].m/2
        energy += balls_array[a].dy*balls_array[a].dy*balls_array[a].m/2
    label1.config(text='общая энергия =' + str(energy))

def calc_impuls():
    impuls = 0
    for a in range (BN+CN):
        impuls += balls_array[a].dx*balls_array[a].m
        impuls += balls_array[a].dy*balls_array[a].m
    label2.config(text='общий импульс =' + str(impuls))

def calc_clusters():
    in_cluster = 0
    a = BN
    while a<(BN+CN):
        if(balls_array[a].color=='Red'):
            in_cluster += 1
        a += 1
    balls_clustered[in_cluster] += 1
    a = balls_clustered[:]
    for i in range (20):
        a[i] *= 100/time
        a[i] = int(a[i])
    for i in range (20):
        canvas.coords(bar_chart[i],indent*(i+1), MAX_Y+200-balls_clustered[i]*100/time, indent*(i+2), MAX_Y+200)
        canvas.coords(bar_chart_percents[i],indent*(i+1.5), MAX_Y+200-balls_clustered[i]*100/time-10)
        canvas.itemconfig(bar_chart_percents[i], text = str(int(balls_clustered[i]*100/time))+'%')

def save_percents():
    a = balls_clustered[:]
    for i in range (20):
        a[i] *= 100/time
    with open('logfile', 'w') as logfile:
        logfile.write('BR='+str(BR)+', CR='+str(CR)+', BN='+str(BN)+', CN='+str(CN)+'\n'+'энергия='+str(energy)+'\n')
        for i in range (20):
            logfile.write(str(i)+' = '+str(a[i])+'\n')

def collision(a, b):
    if(a==b):
        return False
    else:
        x_diff = (balls_array[a].x-balls_array[b].x)
        y_diff = (balls_array[a].y-balls_array[b].y)
        collision_dist_sq = (balls_array[a].R + balls_array[b].R)*(balls_array[a].R + balls_array[b].R)#дистанция означающая столкновение квадрат
        dist_sq = ((x_diff*x_diff)+(y_diff*y_diff)) # квадрат расстояния между центрами
        if(dist_sq <= collision_dist_sq):
            return True
        else:
            return False

def cluster(a, b):
    if(a==b):
        return False
    else:
        x_diff = (balls_array[a].x-balls_array[b].x)
        y_diff = (balls_array[a].y-balls_array[b].y)
        cluster_dist_sq = (balls_array[a].R + balls_array[b].R + BR)*(balls_array[a].R + balls_array[b].R + BR) #дистанция считающаяся кластером квадрат
        dist_sq = ((x_diff*x_diff)+(y_diff*y_diff)) # квадрат расстояния между центрами
        if(dist_sq < cluster_dist_sq):
            return True
        else:
            return False

def resolve_collision(a, b):
    nx = balls_array[b].x - balls_array[a].x #a.x-b.x
    ny = balls_array[b].y - balls_array[a].y #a.x-b.x
    n_mag = sqrt(nx*nx+ny*ny)
    unx = nx/n_mag # x компонента единичного нормального вектора
    uny = ny/n_mag # y компонента единичного нормального вектора
    utx = -uny     # x компонента единичного тангенциального вектора
    uty = unx      # y компонента единичного тангенциального вектора
    v1n = unx*balls_array[a].dx + uny*balls_array[a].dy    #v1n = (un умножить скалярно v1) = нормальная скорость первого шара
    v1t = utx*balls_array[a].dx + uty*balls_array[a].dy    #v1t = (ut умножить скалярно v1) = тангенциальная скорость первого шара
    v2n = unx*balls_array[b].dx + uny*balls_array[b].dy    #все аналогично для второго шара
    v2t = utx*balls_array[b].dx + uty*balls_array[b].dy
    v1n_after = (v1n*(balls_array[a].m-balls_array[b].m)+2*balls_array[b].m*v2n)/(balls_array[a].m+balls_array[b].m) #нормальная компонента 1го после
    v2n_after = (v2n*(balls_array[b].m-balls_array[a].m)+2*balls_array[a].m*v1n)/(balls_array[a].m+balls_array[b].m) #нормальная компонента 2го после
    alfa_un = atan2(uny, unx) # угол нормального вектора в нашей системе координат
    alfa_ut = atan2(uty, utx) # угол тангенциального вектора в нашей системе координат
    v1n_after_x = v1n_after*cos(alfa_un)
    v2n_after_x = v2n_after*cos(alfa_un)
    v1t_after_x = v1t*cos(alfa_ut)
    v2t_after_x = v2t*cos(alfa_ut)
    v1n_after_y = v1n_after*sin(alfa_un)
    v2n_after_y = v2n_after*sin(alfa_un)
    v1t_after_y = v1t*sin(alfa_ut)
    v2t_after_y = v2t*sin(alfa_ut)

    #определение величины наезда шарика на другой при столкновении
    x_diff = (balls_array[a].x-balls_array[b].x)
    y_diff = (balls_array[a].y-balls_array[b].y)
    dist = sqrt(x_diff*x_diff+y_diff*y_diff)
    cross = (balls_array[a].R+balls_array[b].R)-dist
    cross_x = unx*cross
    cross_y = uny*cross

    #корректировка наезда шарика на другой
    balls_array[a].x -= cross_x/2
    balls_array[a].y -= cross_y/2
    balls_array[b].x += cross_x/2
    balls_array[b].y += cross_y/2

    #присвоение скоростей получившихся после удара
    balls_array[a].dx = v1n_after_x + v1t_after_x
    balls_array[a].dy = v1n_after_y + v1t_after_y
    balls_array[b].dx = v2n_after_x + v2t_after_x
    balls_array[b].dy = v2n_after_y + v2t_after_y

def start_command():
    global CN, CR, CM, BN, BR, BM, C_speed, B_speed, N_steps
    CN = int(entry_CN.get())
    CR = int(entry_CR.get())
    CM = int(entry_CM.get())
    BN = int(entry_BN.get())
    BR = int(entry_BR.get())
    BM = int(entry_BM.get())
    C_speed = int(entry_C_speed.get())
    B_speed = int(entry_B_speed.get())
    N_steps = int(entry_N_steps.get())

    entry_window.destroy()
    entry_window.quit()

#начало выполнения
entry_window = Tk()
entry_window.title("Динамика шариков на плоскости")
entry_window.geometry("500x500")

lb_CN = Label(entry_window, text="Число больших шариков ")
lb_CN.grid(row=0, column=3, pady=5)
entry_CN = Entry(entry_window, width=20)
entry_CN.grid(row=0, column=4)

lb_CR = Label(entry_window, text="Радиус больших шариков ")
lb_CR.grid(row=1, column=3, pady=5)
entry_CR = Entry(entry_window, width=20)
entry_CR.grid(row=1, column=4)

lb_CM = Label(entry_window, text="Масса больших шариков ")
lb_CM.grid(row=2, column=3, pady=5)
entry_CM = Entry(entry_window, width=20)
entry_CM.grid(row=2, column=4)

lb_CSpeed = Label(entry_window, text="Скорость больших шариков ")
lb_CSpeed.grid(row=3, column=3, pady=5)
entry_C_speed = Entry(entry_window, width=20)
entry_C_speed.grid(row=3, column=4)

lb_BN = Label(entry_window, text="Число маленьких шариков ")
lb_BN.grid(row=5, column=3, pady=5)
entry_BN = Entry(entry_window, width=20)
entry_BN.grid(row=5, column=4)

lb_BR = Label(entry_window, text="Радиус маленьких шариков ")
lb_BR.grid(row=6, column=3, pady=5)
entry_BR = Entry(entry_window, width=20)
entry_BR.grid(row=6, column=4)

lb_BM = Label(entry_window, text="Масса маленьких шариков ")
lb_BM.grid(row=7, column=3, pady=5)
entry_BM = Entry(entry_window, width=20)
entry_BM.grid(row=7, column=4)

lb_BSpeed = Label(entry_window, text="Скорость маленьких шариков ")
lb_BSpeed.grid(row=8, column=3, pady=5)
entry_B_speed = Entry(entry_window, width=20)
entry_B_speed.grid(row=8, column=4)

lb_N_steps = Label(entry_window, text="Сохранить статистику после N шагов ")
lb_N_steps.grid(row=10, column=3, pady=5)
entry_N_steps = Entry(entry_window, width=20)
entry_N_steps.grid(row=10, column=4)

start_button = Button(text='запустить', command = start_command)
start_button.grid(row=12, column=4)

entry_window.mainloop()

root = Tk()
root.title('динамика шаров на плоскости')
canvas = Canvas(root, width = 900, height = 750, bg = 'white')
canvas.pack()

#квадрат в котором идет симуляция
canvas.create_rectangle(MIN_X, MIN_Y, MAX_X, MAX_Y)

add_balls()
add_big_balls()
set_labels()
main_loop()

#бесконечный цикл окна
root.mainloop()
