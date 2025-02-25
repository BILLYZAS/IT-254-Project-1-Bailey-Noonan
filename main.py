import serial
import time
import speech_recognition as sr

# Connect to Arduino on COM3
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Give Arduino time to initialize

# Function to listen and recognize voice commands
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'turn on' or 'turn off'... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Error with speech recognition: {e}")
        return None

# Main loop to continuously listen for commands
while True:
    command = recognize_speech()
    if command:
        if "turn on" in command:
            ser.write(b'1\n')  # Send '1' to Arduino
            print("Sent: turn on")
        elif "turn off" in command:
            ser.write(b'0\n')  # Send '0' to Arduino
            print("Sent: turn off")
        elif "quit" in command:
            print("Exiting program.")
            break

# Close the serial connection
ser.close()
