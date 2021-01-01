import time
import smtplib
import urllib.request
import datetime
import random
from email.message import EmailMessage
import imghdr
import os

Sender_Email = "xxxx@gmail.com"
Receiver_Email = "xxxx@gmail.com"
Password = "xxxx"
os.chdir("C:\\Users\\xxx\\PycharmProjects\\All_New\\Projects_1\\Email_Self_Sender\\Email_Content")
image_dir = "C:\\Users\\xxx\\PycharmProjects\\All_New\\Projects_1\\Email_Self_Sender\\Email_Images"


def connect():  # Used for checking if there is Internet
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False


def random_line(f_name):  # Used for picking generating random email
    lines = open(f_name, "r", encoding='utf-8').read().splitlines()
    return random.choice(lines)


def send_mail(day_number, today_date1, late_excuse=""):
    file_random = random.choice(os.listdir(image_dir))
    msg2 = EmailMessage()  # creating an object of EmailMessage class
    msg2['Subject'] = f'Day {day_number} of the project'
    msg2['From'] = Sender_Email  # Defining sender email
    msg2['To'] = Receiver_Email  # Defining receiver email
    msg2.set_content(f'''<pre><h3>{random_line('Greeting.txt')} Dani,</h3>
<p style = "font-family:candara,times,helvetica; font-size:14px;">today is day <b>{day_number}</b> since you started this project. 
This is the email for date <b>{today_date1}</b>. 

{random_line('Quote_intro.txt')}
<i>{random_line('Quote.txt')}</i>

{random_line('Picture_intro.txt')}

{random_line('Farewell.txt')} :)
{late_excuse}

Until tomorrow,
<p style = "font-family:candara,times,helvetica; font-size:14px; color:#FF0000;"><i>your fateful servant</i></p></pre>''', subtype="html")
    with open(image_dir + "\\" + file_random, 'rb') as f1:
        image_data = f1.read()
        image_type = imghdr.what(f1.name)
        image_name = f1.name
    msg2.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)  # Login to SMTP server
        smtp.send_message(msg2)  # Sending email using send_message method by passing EmailMessage object
    print(f"Email {day_number} of the project has been sent.")


def send_mail_loop(email_sent_late):
    with open("Day_Count.txt", "r+") as f1:  # Gets current day count and adds 1 day
        day_count = int(f1.read()) + 1
        f1.seek(0)  # rewind
        f1.write(f"{day_count}")
    with open("Day_Date.txt", "r+") as f1:  # Gets current date and adds 1 day to it
        old_date_str = str(f1.read())
        old_date_converted = datetime.date(int(old_date_str[:4]), int(old_date_str[5:7]), int(old_date_str[-2:]))
        new_date = str(old_date_converted + datetime.timedelta(days=1))
        new_date_converted = str(int(new_date[-2:])) + "/" + str(int(new_date[5:7])) + "/" + str(int(new_date[:4]))
        f1.seek(0)  # rewind
        f1.write(f"{new_date}")
        if email_sent_late == 0:
            send_mail(day_count, new_date_converted)
        elif email_sent_late == 1:  # This means email was sent late, adding special apology
            excuse = f"PS: Sorry for sending email late today, {random_line('Late_excuse.txt')} :("
            send_mail(day_count, new_date_converted, excuse)


while True:
    if connect():  # checks if there is Internet connection
        print('Connected to Internet.')
    else:
        print("No Internet.")
        time.sleep(10)
        continue  # Loops to beginning and checks for Internet connection again
    today_date = datetime.date.today()
    with open("Day_Date.txt", "r") as f:
        old_date = str(f.read())
    print(f"Last email was sent on {old_date}")
    if old_date == str(today_date):  # This means email has already been sent today
        print("Today's email already sent. Checking again after 5 hours")
        time.sleep(60 * 60 * 5)
    else:  # This means email has not been sent yet today
        d1 = datetime.date(int(str(today_date)[:4]), int(str(today_date)[5:7]), int(str(today_date)[-2:]))
        d0 = datetime.date(int(str(old_date)[:4]), int(str(old_date)[5:7]), int(str(old_date)[-2:]))
        days_missed = (d1-d0).days
        if days_missed == 1:  # This means last email was sent yesterday.
            while True:
                if connect():  # checks if there is Internet connection again
                    print('Connected to Internet.')
                else:
                    print("No Internet.")
                    time.sleep(10)
                    continue  # Loops to second beginning and checks for Internet connection again
                hour_value = datetime.datetime.now().hour  # Updates hour and minute regularly
                minute_value = datetime.datetime.now().minute
                if hour_value < 10:  # This means it is too early for it to send email
                    print("Too early to send email now. Checking again after 50 minutes")
                    time.sleep(60 * 50)
                elif hour_value < 11:  # Still too early, but almost there
                    print("Too early to send now, but almost time. Checking again after 50 seconds")
                    time.sleep(50)
                elif hour_value == 11 and minute_value == 0:
                    print("11 AM. Sending email.")
                    send_mail_loop(0)
                    break  # Breaks out of loop and starts checking which day it is again
                elif hour_value >= 11:  # This means 11:00 has already passed and no email has been sent
                    print("Sending email, apologies for being late.")
                    send_mail_loop(1)  # Sends special email which has apology at the end :)
                    break  # Breaks out of loop and starts checking which day it is again
        elif days_missed > 1:  # This means more than 1 day has been skipped
            for index in range(days_missed - 1):  # Sending all late emails except one
                print(f"Sending email {index + 1} of {days_missed - 1} total.")
                send_mail_loop(1)
