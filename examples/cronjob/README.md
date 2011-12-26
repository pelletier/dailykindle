# DailyKindle Cronjob example

This example shows you how to daily build and deliver your DailyKindle.

## What you need

* A Unix box.
* An SMTP server (Sendgrid.com is enough for this task).
* Some system management skills.
* Python 3 + Virtualenv

## Let's go

* Create a virtualenv and put all those files in it.
* Download and put somewhere the [kindlegen binary](http://www.amazon.com/gp/feature.html?docId=1000234621)
* Tweak the script.py file according to your SMTP credentials and your
  filesystem paths.
* Run `pip install -r requirements.pip`
* Modify `sources.txt` to your taste.
* Add something like the following line to your crontab (`crontab -e`):

    0 5 * * * cd /home/thomas/dailykindle && /home/thomas/dailykindle/bin/python /home/thomas/dailykindle/script.py

Enjoy your daily news dose!
