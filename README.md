# phat-beatiful
Don't let the name fool you - a last ditch, bare bones effort using python code to make use of a Pimoroni Phatbeat,<br> ignoring the led's completely and hijacking the buttons to 
navigate an existing playlist consisting of 6 internet radio stations before everything ends in the trash. <br>
For Best Results - use strictly on DietPi OS to avoid long bootups and resource conflicts.  Pi OS is ok for minimal barebones barebuttons.py and flask_web.py only though.
**Pre-requisites:** <br> Install Dietpi OS or Raspbian lite OS, MPD, MPC with a working .conf, GPIO libraries, Python and Utilities, Alsa too. <br> 
Optional:  RPIMonitor, Squeezelite and an MPD Client. <br>
If using the web interface, webserver such as nginx or lightppd is required. <br> To use Flask web page, you need to install Flask with Pip in a virtual environment, along with Tornado, Sqlalchemy and gpizero. <br> Barebones web page is included in flask_web.py script. <br>
**You will not see an annoying LED ever again!**. <br>  The web page runs at port 5000 for testing and can be gussied up a bit to your choosing.
Barebuttons1a.py will handle all the physical buttons on the phat itself.<br>  For a web interface, demo_iframe.html and index.html will generate a wrapper for the flask_web page generated, using port 5000 or 8080 after testing.<br>
A bash script will store demo_iframe and index.html in /var/www (dietpi) or /var/www/html (raspberry pi os) <br>
A sample menu with display to portal for rpi monitor is included - purely optional for demo. <br>
Some early PhatBeats have extra small buttons, so the web page option will assist those without dainty attributes. <br>
If  you don't have a Pimoroni PhatBeat board, ignore the barebuttons1a.py - but feel free to use the flask_web.py for your giggles. <br>
**-OR-BETTER-YET-** if you have 6 buttons lying around just waiting to be used...go have at it.<br>
