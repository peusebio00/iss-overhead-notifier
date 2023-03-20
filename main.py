import smtplib
import requests
from datetime import datetime

MY_LAT = 38.707008
MY_LONG = -9.135640
EMAIL = "pedroeusebio45@gmail.com"
PASSWORD = "exirpfsmroawwchf"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
iss_data = response.json()

iss_latitude = float(iss_data["iss_position"]["latitude"])
iss_longitude = float(iss_data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.


def is_within_5():
    calc1 = abs(MY_LAT - iss_latitude)
    calc2 = abs(MY_LONG - iss_longitude)
    if calc1 <= 5 and calc2 <= 5:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
sun_data = response.json()
sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now().hour


def is_night():
    if sunset <= time_now or sunrise > time_now:
        return True


# If the ISS is close to my current position
if is_within_5() and is_night():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs="teste123teste12@yahoo.com",
            msg="Subject: ISS Overhead Notification\n\nLook up! The ISS is flying over your current location."
        )

# and it is currently dark
# Then email me to tell me to look up.
