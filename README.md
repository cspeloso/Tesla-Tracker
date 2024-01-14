# Tesla Tracker
## Get Notified When Tesla Cars Get Listed On The Tesla Website

This python script uses Selenium & chromedriver to load and parse through the [inventory page] (https://www.tesla.com/inventory/new/my?arrangeby=relevance&zip=90210&range=200) on the Tesla website, and send you notification when a car in your price range is listed.

### What's the purpose of this?
I use this to keep track of Teslas that get listed on the Tesla website that are in the price range I'm interested in buying at. I decided to make this when I noticed that cars would get listed and bought out within an hour of getting listed.

With this, you can be the first person to know when the Tesla model you want is listed under a certain price and buy it out immediately.

You can use this further to only show cars with a certain color, or RWD/LR/P, or even other things like the seat color. For those, you'd probably have to load the URL that gets pushed out using Selenium and then parse through that page.

For me, that was overkill. I just wanted to see when new cars were listed under a price point.

### How do I set this up?

Here's an example of the config.ini file (I've blurred out my own API keys):

![SCR-20240113-twbn](https://github.com/cspeloso/Tesla-Tracker/assets/36888899/3a993ea4-ef73-4779-8bc4-e6198e950113)


### How does this work?

Once the car gets parsed through, it'll determine if it's a right fit and then send a notification through the service [Pushover] (https://pushover.net/).

Once the script reaches the Pushover notification part, you can change this to do whatever you want with that data.

If you're using this on a website, you can simply just send out an email instead or something. Get creative!

Again, the ideal way to use this for personal use is to set it up as a cronjob using the Pushover service.

On my Mac Mini, I can set this up as a cronjob and then put the computer to sleep and it'll continue to run while in sleep mode.

This is perfect, especially since the Mac Mini M1 consumes to little power even when on ;-)

### Thanks for checking it out!

Let me know if you find this useful! Email me at business@chrispeloso.com if you have any questions or feedback.

Cheers!