from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date, datetime
import pyfirmata
from pyfirmata import *
from pyfirmata import util
from pymata4 import pymata4

board = pymata4.Pymata4()

# inisiaisi untuk tkinker
root = Tk()
root.geometry('1200x700+200+100')
root.title('UAS GUI')
root.state('zoomed')
root.config(background='#fafafa')

# inisiasi untuk pyplot
xar = []
yar = []

# inisialisasi pin untuk sensor ultrasonic
triger_pin = 11
echo_pin = 12
pinlm35 = 0
style.use('ggplot')
fig = plt.figure(figsize=(14, 4.5), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_ylim(0, 100)
line, = ax1.plot(xar, yar, 'r', marker='o')
#ser = serial.Serial('com3', 9600)

def dateandtime():
    global datetimenow
    today = datetime.now()
    datetimenow = today.strftime("%A, %d %m %Y %H:%M:%S")
    l1 = Label(root, text=datetimenow, font=("Arial Bold", 14))
    l1.grid (column=3, row=0)
    root.after(1000, dateandtime)

def animate(i):
    # Untuk Test Save Csv dengan menggunakan increment

    # yar.append(99-i)
    # xar.append(i)
    read = lm35()
    vout = read * (5000/1024.0)
    vout = float(vout)
    temperatur = vout/10
    temperatur = float(temperatur)

    yar.append(temperatur)
    xar.append(i)

    line.set_data(xar, yar)
    
    ax1.set_xlim(0, i+1)

def lm35():
    board.set_pin_mode_analog_input(pinlm35)
    return(board.analog_read(pinlm35))

def teras1():
    a = board.digital_read(13)
    if a == 0:
        board.digital_pin_write(13,1)
    elif a == 1:
        board.digital_pin_write(13,0)
    print('teras1')

def teras2():
    a = board.digital_read(5)
    if a == 0:
        board.digital_pin_write(5,1)
    elif a == 1:
        board.digital_pin_write(5,0)
    print('teras2')

def terasbelakang():
    a = board.digital_read(4)
    if a == 0:
        board.digital_pin_write(4,1)
    elif a == 1:
        board.digital_pin_write(4,0)
    print('terasbelakang')

def dapur():
    a = board.digital_read(10)
    if a == 0:
        board.digital_pin_write(10,1)
    elif a == 1:
        board.digital_pin_write(10,0)
    print('dapur')

def ruangtamu():
    a = board.digital_read(9)
    if a == 0:
        board.digital_pin_write(9,1)
    elif a == 1:
        board.digital_pin_write(9,0)
    print('ruangtamu')

def kamar1():
    a = board.digital_read(8)
    if a == 0:
        board.digital_pin_write(8,1)
    elif a == 1:
        board.digital_pin_write(8,0)
    print('kamar1')

def kamar2():
    a = board.digital_read(7)
    if a == 0:
        board.digital_pin_write(7,1)
    elif a == 1:
        board.digital_pin_write(7,0)
    print('kamar2')

def kamarmandi():
    a = board.digital_read(6)
    if a == 0:
        board.digital_pin_write(6,1)
    elif a == 1:
        board.digital_pin_write(6,0)
    print('kamar mandi')

def loop():
    try:
        time.sleep(1)

        board.sonar_read(triger_pin)
    except Exception:
        board.shutdown()

def sensor_garasi(data):
    data = data[2]

    if data >= 170:
        print('Terdapat Mobil')
    elif data <= 170:
        print('Tidak Ada Mobil')

def save_csv():
    strx=str(xar)
    stry=str(yar)
    tempstr = strx + ";" + stry + "\n"

    # print(tempstr)

    write_file = "output.csv"
    with open(write_file, "w") as output:
        output.write(tempstr)
    exit()
board.set_pin_mode_sonar(triger_pin,echo_pin,loop)

dateandtime()
lm35()
loop()

# plot sensor suhu realtime ke tkinter
plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().grid(column=1, row=1, columnspan=3)
ani = animation.FuncAnimation(fig, animate, interval=1000, blit=False)

# tombol lampu
btnteras1 = Button(root, text="Teras 1", command=teras1)
btnteras2 = Button(root, text="Teras 2", command=teras2)
btnterasbelakang = Button(root, text="Teras Belakang", command=terasbelakang)
btndapur = Button(root, text="Dapur", command=dapur)
btnruangtamu = Button(root, text="Ruang Tamu", command=ruangtamu)
btnkamar1 = Button(root, text="Kamar 1", command=kamar1)
btnkamar2 = Button(root, text="Kamar 2", command=kamar2)
btnkamarmandi = Button(root, text="Kamar Mandi", command=kamarmandi)

btnsavecsv = Button(root, text="Save Ke CSV", command=save_csv)
btncekgarasi = Button(root, text="Cek Garasi", command=sensor_garasi)

btnteras1.grid(column=1, row=2)
btnteras2.grid(column=1, row=3)
btnterasbelakang.grid(column=1, row=4)
btndapur.grid(column=1, row=5)
btnruangtamu.grid(column=3, row=2)
btnkamar1.grid(column=3, row=3)
btnkamar2.grid(column=3, row=4)
btnkamarmandi.grid(column=3, row=5)
btnsavecsv.grid(column=3, row=6)
btncekgarasi.grid(column=3, row=7)

l1 = Label(root, text="Rizdky Oktaviari Pratama Putra / E41192199", font=("Arial Bold", 14))
l1.grid (column=1, row=0)

root.mainloop()