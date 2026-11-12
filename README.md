# phat-beatiful
don't let the name fool you - a last ditch, bare bones effort using python code to make use of a Pimoroni Phatbeat, ignoring the led's completely and hijacking the buttons to 
navigate an existing playlist consisting of 6 internet radio stations before everything ends in the trash.
Pre-requisites: Dietpi or Raspbian lite OS, MPD, MPC with a working .conf, GPIO libraries, Python and Utilities, Alsa too. 
To use Flask web page, you need to install Flask with Pip in a virtual environment, along with Tornado.  Barebones web page is included in flask_web.py script.
You will not see an annoying LED ever again.  The web page runs at port 5000 and can be gussied up a bit to your choosing.
Barebuttons1a.py will handle all the physical buttons on the phat itself.  For a web interface, flask_web.py will generate a web equivalent for the physical buttons, using port 8080.
