import RPi.GPIO as GPIO
from picamera import PiCamera
import yagmail
from dotenv import load_dotenv
import os
import time
import threading

EXIT_FLAG = False

GPIO.setmode(GPIO.BCM)

print("Waiting 2 seconds to initialize the camera...")
camera = PiCamera()
camera.resolution = (1280, 720)
camera.rotation = 180
time.sleep(2)
print("Camera setup OK.")
if os.path.exists("photo_logs.txt"):
	os.remove("photo_logs.txt")
print("Log file removed.")
load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
yag = yagmail.SMTP(email, password)
print("Email sender setup OK.")
RED_LED = 17
PIR_PIN = 4
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print("GPIOs setup OK.")
print("Everything has been setup.")

time.sleep(1)

print("\nEnter q to quit anytime\n")

def check_program_state():
    global EXIT_FLAG
    while True:
        program_state = input()
        if program_state in ['Q', 'q']:
            EXIT_FLAG = True
            break
        
threading.Thread(target=check_program_state).start()

def take_photo():
	filename = f"/home/anish/camera/img_{int(time.time())}.jpg"
	camera.capture(filename)
	with open("photo_logs.txt", "a") as f:
		f.write(filename + "\n")

def send_email_with_photo():
	with open("photo_logs.txt", "r") as f:
		filename = f.readlines()[-1]
		yag.send(to=email,
				subject="Movement detected!",
				contents="Here's a photo taken by your Raspberry Pi",
				attachments=filename[0:len(filename) - 1])


last_time_photo_taken = 60
start_time = time.time()
end_time = time.time()

while not EXIT_FLAG:
	time.sleep(0.1)
	state = GPIO.input(PIR_PIN)
	if state == GPIO.HIGH:
		if int(end_time - start_time) >= 3 and last_time_photo_taken >= 10:
			GPIO.output(RED_LED, GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(RED_LED, GPIO.LOW)
			take_photo()
			send_email_with_photo()
			last_time_photo_taken = 0
			start_time = time.time()
			end_time = time.time()
		else:
			last_time_photo_taken += 0.1
			end_time = time.time()
		# print("high: " + " " + str(end_time - start_time))
	else:
		last_time_photo_taken += 0.1
		start_time = time.time()
		end_time = time.time()
		# print("low: " + " " + str(end_time - start_time))
	
GPIO.cleanup()
		
