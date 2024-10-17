import random
import speech_recognition as sr
import os
import webbrowser
from openai import OpenAI
from config import apikey
import datetime
import smtplib
import openai
import schedule
import time
import threading  # Added for threading

client = OpenAI(api_key=apikey)

chatStr = ""


def chat(ans):
    ans = ans[31:]

    fstr = ""
    global chatStr
    print(chatStr)
    chatStr += f"Sahil: {ans}\n R2: "
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful desktop asistant"},
                  {"role": "user", "content": f"{ans}"}],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            chatStr += chunk.choices[0].delta.content
            fstr += chunk.choices[0].delta.content
            print(fstr)

    return fstr


def chatter(ans):
    fstr = ""
    global chatStr
    print(chatStr)
    chatStr += f"Sahil: {ans}\n R2: "
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful desktop asistant"},
                  {"role": "user", "content": f"{ans}"}],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            chatStr += chunk.choices[0].delta.content
            fstr += chunk.choices[0].delta.content
            print(fstr)

    return fstr


def say(text):
    # Ensure text is not empty and escape special characters
    if text:
        text = text.replace('"', '').replace("'", '')  # Remove any quotes that can cause issues
        os.system(f'say "{text}"')  # Ensure text is enclosed in quotes to prevent shell errors



def takecommand():
    r = sr.Recognizer()
    print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("say anything : ")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"User said : {text}")
            return text
        except:
            print("sorry, could not recognise")
            return ""  # Return empty string to prevent blocking


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('gandhadaurusahil2004@gmail.com', 'deyq awnp cabz leus')
    server.sendmail('gandhadaurusahil2004@gmail.com', to, content)
    server.close()


# Function to set a reminder task
def set_task():
    say("What task do you want to set?")
    task = takecommand()  # Use your voice command function

    say("At what time should I remind you? Please say in HH:MM AM/PM format.")
    time_input = takecommand()  # Use your voice command function

    # Normalize the AM/PM format to uppercase
    time_input = time_input.replace("a.m.", "AM").replace("p.m.", "PM").upper()

    # Add logic to check if the input was parsed correctly (e.g., "230 PM" instead of "2:30 PM")
    # This will insert a colon in the appropriate place if missing
    if len(time_input) in [6, 7]:  # Handle cases like "230 PM" (6 chars with or without space)
        if "AM" in time_input or "PM" in time_input:
            # Insert colon at the correct place, so "230 PM" becomes "2:30 PM"
            time_input = time_input[:-5] + ':' + time_input[-5:]

    try:
        # Attempt to parse the corrected time input
        task_time = datetime.datetime.strptime(time_input, "%I:%M %p").time()
        say(f"Setting a reminder for {task} at {time_input}")

        # Schedule the task
        schedule.every().day.at(task_time.strftime("%H:%M")).do(reminder, task)
    except ValueError:
        say("Sorry, I couldn't understand the time format. Please try again.")



def reminder(task):
    say(f"Reminder: {task}")


# Function to handle the scheduler in a separate thread
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    print('Pycharm')
    say("Hello I am R2 AI")

    # Start the schedule in a separate thread
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.daemon = True  # Allows the thread to exit when the main program exits
    schedule_thread.start()

    while True:
        flag = True
        print("listening")
        ans = takecommand()

        if not ans:  # Skip if the user doesn't say anything
            continue

        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://wikipedia.org"],
                 ["google", "https://www.google.com"],
                 ["instagram", "https://www.instagram.com"],
                 ["xavier institute of engineering website", "https://www.xavier.ac.in"],
                 ["xavier campus", "https://xavier.qualcampus.com/Account/Logon/"]]

        if flag:
            for site in sites:
                if f"open {site[0]}".lower() in ans.lower():
                    say(f"opening {site[0]} sir..")
                    webbrowser.open(site[1])
                    flag = False

                if "open music" in ans:
                    musicPath = "Users/macbookair/Downloads/James Mercy - Vienna (feat. PhiloSofie) [NCS Release]"
                    import subprocess, sys

                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, musicPath])
                    flag = False

                if "the time" in ans:
                    strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                    say(f"sir the time is {strfTime}")
                    flag = False

        if flag:
            apps = [["zoom", "open /Applications/zoom.us.app"], ["contacts", "/System/Applications/Contacts.app"]]
            for app in apps:
                if f"open {app[0]}".lower() in ans.lower():
                    webbrowser.open(app[1])
                    flag = False

                if "open zoom".lower() in ans.lower():
                    say(f"opening zoom")
                    os.system(f"open /Applications/zoom.us.app")
                    flag = False

                if "email" in ans:
                    say(f"to whom")
                    to = takecommand()
                    to = to.lower().replace('attherate', '@')
                    say(f"what should I say in email")
                    content = takecommand()
                    sendEmail(to, content)
                    say(f"email has been sent")
                    flag = False

                if "using artificial intelligence".lower() in ans.lower():
                    chat(ans)
                    flag = False

                if "r2 quit".lower() in ans.lower():
                    exit()

        if flag:
            say(chatter(ans))

        # Check if user wants to set a task
        if "set a task".lower() in ans.lower():
            to = takecommand()
            to = to.lower().replace('p.m', 'PM')
            set_task()
