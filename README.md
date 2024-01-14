This project uses Selenium to & chromedriver to parse through the Tesla inventory page (see here: https://www.tesla.com/inventory/new/my?arrangeby=relevance&zip=90210&range=200). 

I use this to keep track of Teslas that get listed on the Tesla website that are in the price range I'm interested in buying at. I decided to make this when I noticed that cars would get listed and bought out within an hour of getting listed.

with this, you can be the first person to see when the Tesla model you want is listed under a certain price and buy it out immediately.

You can use this further to only show cars with a certain color, or RWD/LR/P, or even other things like the seat color. For those, you'd probably have to load the URL that gets pushed out using Selenium and then parse through that page.
For me, that was overkill.

Here's an example of the config.ini file:

![SCR-20240113-twbn](https://github.com/cspeloso/Tesla-Tracker/assets/36888899/3a993ea4-ef73-4779-8bc4-e6198e950113)
