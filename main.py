from flask import Flask,render_template
from flask_socketio import SocketIO
import serial
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bruh'
socket = SocketIO(app)
#ser= serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
#ser = serial.Serial(port='/dev/cu.usbmordem14101',baudrate=9600)
 # Change the port and baud rate as needed
someList = ['0,0,0,0,0','0,0,0,0,0']
i=0
@app.route('/')
def main():
    return render_template('index.html')

@socket.on('message')
def handlemsg(msg):
    global i
    while True :
        socket.send(someList[i])
        if i == (len(someList) -1):
           ##value= ser.readline()
           ##data = str(value,'UTF-8').strip()
           data = input("votes strung : ")
           if data != (someList[(len(someList)-1)]) :
              someList.append(data)
              print(data)
              i += 1
    ##ser.close()

if __name__ == "__main__" :
    socket.run(app)