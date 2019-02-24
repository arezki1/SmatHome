import grovepi
from grovepi import *
from grove_rgb_lcd import *
from firebase import firebase
from firebase.firebase import FirebaseApplication
import dweepy
from subprocess import call
from math import isnan
import pyrebase
import threading
led = 5 #connect the light led to port 5
buzzer = 8 #connect the buzzer to port 7
ultrasonic_ranger = 6 #connect the distance sensor to port 8
dht_sensor_port = 1 # connect the DHt sensor to port 2
dht_sensor_type = 0
# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0
setRGB(0,255,0)

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0

grovepi.pinMode(light_sensor,"INPUT")

#setting up the configuration of the firebase account
config = {
  "apiKey": "AIzaSyBsVIa3I1VS8eDykYwcggUVz9cH-xkwfC4",
  "authDomain": "ca1firebaseproject-532d7.firebaseapp.com",
  "databaseURL": "https://ca1firebaseproject-532d7.firebaseio.com",
  "projectId": "ca1firebaseproject-532d7",
  "storageBucket": "gs://ca1firebaseproject-532d7.appspot.com"
  
};

#initialise the firebase instance
firebase2 = pyrebase.initialize_app(config)

#get the database instance
db = firebase2.database()

#set up the buzzer 
grovepi.pinMode(buzzer,"OUTPUT")

#get an instance of the firebase api
firebase1 = firebase.FirebaseApplication('https://ca1firebaseproject-532d7.firebaseio.com/', None)
while True:     # in case of IO error, restart
    try:

                #handle the light sensor
        
                def lighter():
                      # get the temperature and Humidity from the DHT sensor
##                    #[ temp,hum ] = grovepi.dht(dht_sensor_port,dht_sensor_type)
##                    #print("temp =", temp, "C\thumidity =", hum,"%")
##                    # check if we have nans
##                    # if so, then raise a type error exception
##                    
##                    #if isnan(temp) is True or isnan(hum) is True:
##                        
##                     #   raise TypeError('nan error')
##                        
##
##                    #temp = str(temp)
##                    #hum = str(hum)                 
##                    
##                  
##                    #return the temperature and humidity json object
##                    #def weatherInfo():
##                     #   return {"Temperature":temp," Humidity":hum}
##                       
##                    #method to call to post to firebase
##                    #def postFirebase(dic):                                             
##                       # firebase1.post("temp1",dict)
##                        
##                    #set up and return a python dictionary to hold all our data 
##                   # def getReading():
##                    #    dict={}
##                     #   dict["data"]=weatherInfo()
##                      #  return dict
##                    
##                    #store all the data in dictionary
##                    #
##                   # try:
##                        #dict=getReading()
##                        #print("the dict is ", dict)
##                    #except json.JSONDecodeError:
##                        
##                       # print ("error")             
##                                       
##
##                    #call metthod to post data to firebase here
##                    #postFirebase(dict)
##                  #  time.sleep(5)
##                    
##                    #check if the data was sent, then print out its content
##                   # if(postFirebase):
##                       # print (" Posted ",dict)


                     #from here we are seting up the condition to set up the light 
                    def stream_text(message):                 
                        print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
                        text(message["data"])
                        
                    db.child("thresh").stream(stream_text)
                    
                    def text(value):
                        print("the Threshold is ",value)
                            #setText(value)                   
                                          
                
                         # Get sensor value
                        light_value = grovepi.analogRead(light_sensor)
                         # Calculate resistance of sensor in K
                        resistance = (float)(1023 - light_value) * 10 / light_value
                        print("the light is ",resistance)

                        #set up the threshold to 10
                        threshold = value

                        # Turn on LED once sensor exceeds threshold resistance
                        if resistance < threshold:
                            # Send HIGH to switch on LED

                            try:
                                grovepi.digitalWrite(led,1)
                            except:
                                grovepi.digitalWrite(led,0)
                        else:
                            # Send LOW to switch off LED
                            grovepi.digitalWrite(led,0)
                        
                    
                        #print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
                    

                tlight = threading.Thread(target=lighter)
                tlight.start()             


                # From here we are setting a new thread to manipulate mehtods that read data from firebase
                def read():

                    # Here we are getting the text message from the user and set the screen to it
                    time.sleep(.5)
                    def text1():
                        def stream_text(message):                 
                            print("The message is ",message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
                            text(message["data"])
                            
                        db.child("message").stream(stream_text)
                        
                        def text(value):                            
                            setText(value)
                    text1()
       
                    ## set the light brightnes
                    def stream_handler(message):                    
                
                        print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
                        light(message["data"])
                    
                                    
                    db.child("light").stream(stream_handler)
   
                    def light(value):
                                       
                        grovepi.analogWrite(led,value*2)

                    #set the buzzer on/off
                        
                    def stream_handler2(message):                    
                
                        print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
                        buzz(message["data"])
                       
                    
                                    
                    db.child("buzzer").stream(stream_handler2)

                    def buzz(value):
                        print(value)
                        if(value=="on"):
                            print "hi"
                            try:
                                
                                grovepi.digitalWrite(buzzer,1)

                                time.sleep(0.5)
                                grovepi.digitalWrite(buzzer,0)
                                
                            except:
                                grovepi.digitalWrite(buzzer,0) 
                            
                        else:
                            grovepi.digitalWrite(buzzer,0)                      
                
                t1 = threading.Thread(target=read)
                
                # Start Threadt1              
                t1.start()
                
               
                
    except (IOError, TypeError) as e:
                print(str(e))
                # and since we got a type error
                # then reset the LCD's text
                setText("")
    except KeyboardInterrupt as e:
                 print(" Exited ",str(e))
                    # since we're exiting the program
                    # it's better to leave the LCD with a blank text
                 setText("")
                 #break out of the system
                 break
    
    break             
                        
