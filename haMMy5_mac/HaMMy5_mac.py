import os
import subprocess
import math
import sys

os.system("pip3 install matplotlib")

import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image

window = tk.Tk()
window.geometry("1200x600")
window.title("haMMy gui")
window.resizable(0,0)

defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Adobe Devanagari", size=15)

window.columnconfigure(0, weight=6)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=2)
window.columnconfigure(3, weight=6)
window.columnconfigure(4, weight=2)
window.columnconfigure(5, weight=4)
window.columnconfigure(6, weight=2)
window.columnconfigure(7, weight=8)
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=0)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=2)
window.rowconfigure(4, weight=2)
window.rowconfigure(5, weight=2)
window.rowconfigure(6, weight=2)

file = ""

def update(event=None, value=False):
    global optionsss
    global e2
    global eee
    global clickedd
    global backup
    
    if num_of_states.get() > 10 or num_of_states.get() < 2:
        eee.set("number of states out of range")
    else:
        eee.set("")
        if type(value) == int:
            clickedd.set(value)
        backup.append(int(clickedd.get()))
        if c1.get() == 1:
            optionsss += [tk.StringVar(value=f'{i/(num_of_states.get()+1)}') for i in range(len(optionsss)+1,num_of_states.get()+1)]
            e3 = tk.StringVar(value=e2.get())
            e2.delete(0, tk.END)
            optionsss[backup[-2]-1] = e3
            e2.insert(0, optionsss[int(clickedd.get())-1].get())
        else:
            optionsss = [tk.StringVar(value=f'{i/(num_of_states.get()+1)}') for i in range(1,num_of_states.get()+1)]
            e3 = tk.StringVar(value=e2.get())
            e2.delete(0, tk.END)
            optionsss[backup[-2]-1] = e3
            e2.insert(0, optionsss[int(clickedd.get())-1].get())

num_of_states=tk.IntVar(value=2)
l1 = tk.Label(window, text="number of states to fit: ")
l1.grid(row=3, column=0, sticky=tk.E)

e1 = tk.Entry(window, textvariable = num_of_states, highlightthickness=1,width=2,font='Adobe-Devanagari')
e1.config(highlightbackground = "black", highlightcolor= "blue")
e1.grid(row=3, column=1, sticky=tk.EW)

eee = tk.StringVar()
error = tk.Label(window, textvariable=eee)
error.config(fg= "red")
error.grid(row=5,column=0, columnspan=2, sticky=tk.E)

options = ["traditional                        ", "baum-welch                     "]
clicked = tk.StringVar()
clicked.set("traditional                        ")
dropp = tk.OptionMenu(window, clicked, *options)
dropp.grid(row=4, column=0, columnspan=2, sticky=tk.E)

l2 = tk.Label(window, text="guesses")
l2.grid(row=2, column=3, sticky=tk.SW)
x = []
blue_y = []
orange_y = []
green_y = []
red_y = []
zoooom = False
zoom_x = []
zoom_blue_y = []
zoom_orange_y = []
zoom_red_y = []
zoom_green_y = []


def refresh(*args):
    global optionss
    global optionsss
    global clickedd
    global drop
    global x
    global blue_y
    global orange_y
    global green_y
    global red_y
    global leftb
    global rightb
    global eee
    global f
    global m_prob
    global cc
    global cc2
    global aa2
    global aa
    global eee
    global f2
    global l22

    if num_of_states.get() > 10 or num_of_states.get() < 2:
        eee.set("number of states out of range")
    else:
        eee.set("")
        menu = drop["menu"]
        menu.delete(0, "end")
        optionss = [i for i in range(1,num_of_states.get()+1)]
        if c1.get() == 1:
            optionsss += [tk.StringVar(value=f'{i/(num_of_states.get()+1)}') for i in range(len(optionsss)+1,num_of_states.get()+1)]
        else:
            optionsss = [tk.StringVar(value=f'{i/(num_of_states.get()+1)}') for i in range(1,num_of_states.get()+1)]
        for i in optionss:
            menu.add_command(label=i, command=lambda value=i: update(value=value))
            
        if file != "":
            aa.clear()
            if c1.get():
                os.system(f'cp executable "{os.path.dirname(file)}"; ./executable {num_of_states.get()} "{file}" {" ".join(map(lambda x: x.get(), optionsss))}; cd; cd "{os.path.dirname(file)}"; rm executable')
            else:
                os.system(f'cp executable "{os.path.dirname(file)}"; ./executable {num_of_states.get()} "{file}"; cd; cd "{os.path.dirname(file)}"; rm executable')
            
            with open(file, 'r') as w:
                x = [float(y.split()[0]) for y in w.read().split('\n')[:-1]]
            ty = x[1]-x[0]
            with open(file[:-4]+"path.dat", 'r') as w:
                t = w.read().split('\n')[:-1]
                orange_y = [float(y.split()[-1]) for y in t]
                blue_y = [float(y.split()[-2]) for y in t]
                red_y = [float(y.split()[-3]) for y in t]
                green_y = [float(y.split()[-4]) for y in t]
                
            with open(file[:-4]+"path.dat", 'w') as w:
                for i in range(len(x)):
                    w.write(f"{x[i]}\t{green_y[i]}\t{red_y[i]}\t{blue_y[i]}\t{orange_y[i]}\n")
                    
            if zoooom == True:
                zoom()
            else:
                aa.clear()
                aa2.clear()
                aa2.set_xlabel('Time (s)')
                aa2.set_ylabel('Intensity')
                aa2.set_title("Green: Donor, Red: Acceptor")
                hh = []
                hhh = []
                for i in range(int(min(x)), int(max(x))+1):
                    hh.append(i)
                    hh.append(i+0.25)
                    hh.append(i+0.5)
                    hh.append(i+0.75)
                    
                    hhh.append(str(i))
                    if max(x)-min(x) <= 2:
                        hhh += [str(i+0.25),str(i+0.5),str(i+0.75)]
                    elif max(x)-min(x) <= 3:
                        hhh += ['',str(i+0.5),'']
                    else:
                        hhh += ['','','']
                    
                hh.append(int(max(x))+1)
                hhh.append(str(int(max(x))+1))

                aa2.set_xticks(hh)
                aa2.set_xticklabels(hhh)
                f2.tight_layout()

                aa.set_xlabel('Time (s)')
                aa.set_ylabel('FRET')
                aa.set_xticks(hh)
                aa.set_xticklabels(hhh)
                f.tight_layout()
                
                aa.plot(x,blue_y,color="#0394fc")
                aa.plot(x,orange_y,color="#ff8c00")
                cc.draw()
                    
                aa2.plot(x,green_y,color="#03fc5e")
                aa2.plot(x,red_y,color="#fc0303")
                cc2.draw()
                
            one = []
            two = []
            three = []
            four = []
            with open(file[:-4]+"dwell.dat", 'r') as w:
                t = w.read().split('\n')[:-1]
                three = [int(y.split()[-1]) for y in t]
                four = list(map(lambda z: round(z*ty, 2), three))
                two = [float(y.split()[-2]) for y in t]
                one = [float(y.split()[-3]) for y in t]

            with open(file[:-4]+"dwell.dat", 'w') as w:
                for i in range(len(one)):
                    w.write(f"{one[i]}\t{two[i]}\t{three[i]}\t{four[i]}\n")
                    
            with open(file[:-4]+"report.dat", 'r') as w:
                m_prob = float(w.read().split('\n')[0].split()[-1])
            l22.set(f"maximum probability found:  {m_prob}")

c1 = tk.IntVar()
c = tk.Checkbutton(window, text='use provided guesses', variable=c1)
c.grid(row=3, column=3, sticky=tk.W)

optionss = [i for i in range(1,num_of_states.get()+1)]
optionsss = [tk.StringVar(value=f'{i/(num_of_states.get()+1)}') for i in range(1,num_of_states.get()+1)]
backup=[1]

clickedd = tk.StringVar()
clickedd.set(1)
drop = tk.OptionMenu(window, clickedd, *optionss, command=update)
drop.grid(row=4, column=3, sticky=tk.W)

e2 = tk.Entry(window, textvariable=optionsss[int(clickedd.get())-1], highlightthickness=1,width=19, font='Adobe-Devanagari')
e2.config(highlightbackground = "black", highlightcolor= "blue")
e2.grid(row=4, column=3, sticky=tk.E)

f2 = Figure(figsize=(13,2.375), dpi=100)
aa2 = f2.add_subplot(111, facecolor="black")
aa2.set_xlabel('Time (s)')
aa2.set_ylabel('Intensity')
aa2.set_title("Green: Donor, Red: Acceptor")
aa2.set_xticks([i*0.25 for i in range(5)])
aa2.set_xticklabels(['0', '0.25','0.5','0,75', '1'])
f2.tight_layout()
cc2 = FigureCanvasTkAgg(f2, master=window)
cc2.get_tk_widget().grid(row=0, column=0, columnspan=8, sticky=tk.NW)
cc2.draw()

f = Figure(figsize=(13,2.375), dpi=100)
aa = f.add_subplot(111, facecolor="black")
aa.set_xlabel('Time (s)')
aa.set_ylabel('FRET')
aa.set_xticks([i*0.25 for i in range(5)])
aa.set_xticklabels(['0', '0.25','0.5','0.75', '1'])
f.tight_layout()
cc = FigureCanvasTkAgg(f, master=window)
cc.get_tk_widget().grid(row=1, column=0, columnspan=8, sticky=tk.SW)
cc.draw()

m_prob = 0
def upload(event=None):
    global m_prob
    global cc
    global cc2
    global aa2
    global aa
    global file
    global eee
    global f
    global f2
    global blue_y
    global orange_y
    global green_y
    global red_y
    global x
    global gh
    global l22

    if num_of_states.get() > 10 or num_of_states.get() < 2:
        eee.set("number of states out of range")
    else:
        eee.set("")
        aa.clear()
        aa2.clear()
        filenames = tk.filedialog.askopenfilenames(parent=window, filetypes=[("DAT files", ".dat")])
        try:
            for ff in filenames:
                if c1.get():
                    os.system(f'cp executable "{os.path.dirname(ff)}"; ./executable {num_of_states.get()} "{ff}" {" ".join(map(lambda x: x.get(), optionsss))}; cd; cd "{os.path.dirname(ff)}"; rm executable')
                else:
                    os.system(f'cp executable "{os.path.dirname(ff)}"; ./executable {num_of_states.get()} "{ff}"; cd; cd "{os.path.dirname(ff)}"; rm executable')
                
                with open(ff, 'r') as w:
                    x = [float(y.split()[0]) for y in w.read().split('\n')[:-1]]
                ty = x[1]-x[0]
                
                with open(ff[:-4]+"path.dat", 'r') as w:
                    t = w.read().split('\n')[:-1]
                    orange_y = [float(y.split()[-1]) for y in t]
                    blue_y = [float(y.split()[-2]) for y in t]
                    red_y = [float(y.split()[-3]) for y in t]
                    green_y = [float(y.split()[-4]) for y in t]

                with open(ff[:-4]+"path.dat", 'w') as w:
                    for i in range(len(x)):
                        w.write(f"{x[i]}\t{green_y[i]}\t{red_y[i]}\t{blue_y[i]}\t{orange_y[i]}\n")

                if zoooom == True:
                    zoom()
                    save_g()
                else:
                    leftb.set(str(min(x)))
                    rightb.set(str(max(x)))
                    
                    aa.clear()
                    aa2.clear()

                    aa2.set_xlabel('Time (s)')
                    aa2.set_ylabel('Intensity')
                    aa2.set_title("Green: Donor, Red: Acceptor")
                    hh = []
                    hhh = []
                    for i in range(int(min(x)), int(max(x))+1):
                        hh.append(i)
                        hh.append(i+0.25)
                        hh.append(i+0.5)
                        hh.append(i+0.75)
                        
                        hhh.append(str(i))
                        if max(x)-min(x) <= 2:
                            hhh += [str(i+0.25),str(i+0.5),str(i+0.75)]
                        elif max(x)-min(x) <= 3:
                            hhh += ['',str(i+0.5),'']
                        else:
                            hhh += ['','','']
                        
                    hh.append(int(max(x))+1)
                    hhh.append(str(int(max(x))+1))

                    aa2.set_xticks(hh)
                    aa2.set_xticklabels(hhh)
                    f2.tight_layout()

                    aa.set_xlabel('Time (s)')
                    aa.set_ylabel('FRET')
                    aa.set_xticks(hh)
                    aa.set_xticklabels(hhh)
                    f.tight_layout()
                    
                    aa.plot(x,blue_y,color="#0394fc")
                    aa.plot(x,orange_y,color="#ff8c00")
                    cc.draw()
                    
                    aa2.plot(x,green_y,color="#03fc5e")
                    aa2.plot(x,red_y,color="#fc0303")
                    cc2.draw()
                    file = ff
                    save_g()

                one = []
                two = []
                three = []
                four = []
                with open(ff[:-4]+"dwell.dat", 'r') as w:
                    t = w.read().split('\n')[:-1]
                    three = [int(y.split()[-1]) for y in t]
                    four = list(map(lambda z: round(z*ty, 2), three))
                    two = [float(y.split()[-2]) for y in t]
                    one = [float(y.split()[-3]) for y in t]

                with open(ff[:-4]+"dwell.dat", 'w') as w:
                    for i in range(len(one)):
                        w.write(f"{one[i]}\t{two[i]}\t{three[i]}\t{four[i]}\n")
                    
                with open(ff[:-4]+"report.dat", 'r') as w:
                    m_prob = float(w.read().split('\n')[0].split()[-1])
                l22.set(f"maximum probability found:  {m_prob}")
                
            gh.set(f"file loaded: {os.path.basename(file) if file != '' else 'none'}")
        except:
            pass

def zoom():
    global zoooom
    global zoom_x
    global zoom_blue_y
    global zoom_green_y
    global zoom_orange_y
    global zoom_red_y
    global aa
    global aa2
    global cc
    global cc2
    global eee
    global f
    global f2

    if num_of_states.get() > 10 or num_of_states.get() < 2:
        eee.set("number of states out of range")
    else:
        eee.set("")
        zoom_x = []
        zoom_blue_y = []
        zoom_green_y = []
        zoom_orange_y = []
        zoom_red_y = []
        zoooom = True
        for i in range(len(x)):
            if x[i] >= float(leftb.get()) and x[i] <= float(rightb.get()):
                zoom_x.append(x[i])
                zoom_blue_y.append(blue_y[i])
                zoom_orange_y.append(orange_y[i])
                zoom_green_y.append(green_y[i])
                zoom_red_y.append(red_y[i])

        aa.clear()

        aa.set_xlabel('Time (s)')
        aa.set_ylabel('FRET')
        
        hh = []
        hhh = []
        for i in range(int(min(zoom_x)), int(max(zoom_x))+1):
            hh.append(i)
            hh.append(i+0.25)
            hh.append(i+0.5)
            hh.append(i+0.75)
                    
            hhh.append(str(i))
            if max(zoom_x)-min(zoom_x) <= 2:
                hhh += [str(i+0.25),str(i+0.5),str(i+0.75)]
            elif max(zoom_x)-min(zoom_x) <= 3:
                hhh += ['',str(i+0.5),'']
            else:
                hhh += ['','','']
                    
        hh.append(int(max(zoom_x))+1)
        hhh.append(str(int(max(zoom_x))+1))

        aa.set_xticks(hh)
        aa.set_xticklabels(hhh)
        f.tight_layout()
        
        aa.plot(zoom_x,zoom_blue_y,color="#0394fc")
        aa.plot(zoom_x,zoom_orange_y,color="#ff8c00")
        cc.draw()

        aa2.clear()

        aa2.set_xlabel('Time (s)')
        aa2.set_ylabel('Intensity')
        
        aa2.set_xticks(hh)
        aa2.set_xticklabels(hhh)
        aa2.set_title("Green: Donor, Red: Acceptor")

        f2.tight_layout()
        
        aa2.plot(zoom_x,zoom_green_y,color="#03fc5e")
        aa2.plot(zoom_x,zoom_red_y,color="#fc0303")
        cc2.draw()

def reset():
    global zoooom
    global aa
    global aa2
    global cc
    global cc2
    global leftb
    global rightb
    global eee
    global f
    global f2

    if num_of_states.get() > 10:
        eee.set("number of states out of range")
    else:
        eee.set("")
        leftb.set(min(x))
        rightb.set(max(x))
        zoooom = False
        aa.clear()

        hh = []
        hhh = []
        for i in range(int(min(x)), int(max(x))+1):
            hh.append(i)
            hh.append(i+0.25)
            hh.append(i+0.5)
            hh.append(i+0.75)
                    
            hhh.append(str(i))
            if max(x)-min(x) <= 2:
                hhh += [str(i+0.25),str(i+0.5),str(i+0.75)]
            elif max(x)-min(x) <= 3:
                hhh += ['',str(i+0.5),'']
            else:
                hhh += ['','','']
                    
        hh.append(int(max(x))+1)
        hhh.append(str(int(max(x))+1))

        aa.set_xlabel('Time (s)')
        aa.set_ylabel('FRET')
        aa.set_xticks(hh)
        aa.set_xticklabels(hhh)
        f.tight_layout()
        
        aa.plot(x,blue_y,color="#0394fc")
        aa.plot(x,orange_y,color="#ff8c00")
        cc.draw()

        aa2.clear()
        
        aa2.set_xlabel('Time (s)')
        aa2.set_ylabel('Intensity')
        aa2.set_title("Green: Donor, Red: Acceptor")
        aa2.set_xticks(hh)
        aa2.set_xticklabels(hhh)

        f2.tight_layout()
        
        aa2.plot(x,green_y,color="#03fc5e")
        aa2.plot(x,red_y,color="#fc0303")
        cc2.draw()

def save_g(event=None):
    global f
    global f2
    global file
    f.savefig(f'{os.path.basename(file)[:-4]}_haMMyfit.png')
    f2.savefig(f'{os.path.basename(file)[:-4]}_fluorophoreintensity.png')
    im2 = Image.open(f'{os.path.basename(file)[:-4]}_haMMyfit.png')
    im1 = Image.open(f'{os.path.basename(file)[:-4]}_fluorophoreintensity.png')
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    dst.save(f'{file[:-4]}path_plot.png')
    os.system(f'rm "{os.path.basename(file)[:-4]}_haMMyfit.png"')
    os.system(f'rm "{os.path.basename(file)[:-4]}_fluorophoreintensity.png"')

def alll(event=None):
    refresh()
    update()

button = tk.Button(window, text='load data', command=upload, height=3)
button.grid(row=2,column=7,rowspan=2, sticky=tk.SW, padx=(57, 0))

button3 = tk.Button(window, text='save graphs', command=save_g,height=3)
button3.grid(row=2,column=7,rowspan=2, sticky=tk.S, padx=(36, 0))

button2 = tk.Button(window, text='↻', command=alll, width=3,height=3)
button2.grid(row=2,column=7,rowspan=2, sticky=tk.S, padx=(200, 0))

ll2 = tk.Label(window, text="graph scaling")
ll2.grid(row=2, column=5,sticky=tk.S)

leftb=tk.StringVar()
leftb.set("0.0")
oops = tk.Entry(window, textvariable = leftb, highlightthickness=1,width=4,font='Adobe-Devanagari')
oops.config(highlightbackground = "black", highlightcolor= "blue")
oops.grid(row=3, column=4, rowspan=2, sticky=tk.E)

rightb=tk.StringVar()
rightb.set("1.0")
oopss = tk.Entry(window, textvariable = rightb, highlightthickness=1,width=4,font='Adobe-Devanagari')
oopss.config(highlightbackground = "black", highlightcolor= "blue")
oopss.grid(row=3, column=6, rowspan=2, sticky=tk.W)

zoomm = tk.Button(window, text='zoom', command=zoom)
zoomm.grid(row=3,column=5, sticky=tk.NSEW)
full = tk.Button(window, text='fullscreen', command=reset)
full.grid(row=4,column=5, sticky=tk.NSEW)

l22 = tk.StringVar()
l22.set(f"maximum probability found:  {m_prob}")
l2 = tk.Label(window, textvariable=l22)
l2.grid(row=4,column=7, columnspan=2)

gh = tk.StringVar()
gh.set(f"file loaded: {os.path.basename(file) if file != '' else 'none'}")
gg = tk.Label(window, textvariable=gh)
gg.grid(row=5,column=7, columnspan=2)

window.mainloop()
