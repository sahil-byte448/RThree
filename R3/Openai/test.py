from yagmail import  SMTP

yag = SMTP("gandhadaurusahil2004@gmail.com", "deyq awnp cabz leus")
yag.send(to="anasfodkar5@gmail.com",subject="Great!")

Zoom.py
import schedule
import time
import webbrowser

def open_link(link):
    webbrowser.open('https://us04web.zoom.us/j/6273187683')

def demo_meeting():
    open_link('MY ZOOM MEETING URL')

schedule.every().tuesday.at("14:51").do(demo_meeting)

while 1:
    schedule.run_pending()
    time.sleep(1)
