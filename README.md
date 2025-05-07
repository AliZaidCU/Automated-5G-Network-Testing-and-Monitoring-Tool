[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/B0ZgLxsN)
# SYSC3010 Lab4 Mini-Project
This repository was created by former TAs Roger Selzler and Yousef Yassin for Part3 of Lab4 of the SYSC3010 course at Carleton University. The main goals are:
1. Demonstrate how to build a distributed embedded system using technologies that may be useful for students' own projects
2. Use git as a team, where each student changes files in their own branches and then merges their branch into the main branch once the new features are implemented. Each pull request should be reviewed by a student *other than* the student who created the branch.

# Important Note
This mini project requires project requires the use of pyrebase and cloud resources similar to that of lab 3. Remember to install packages and execute code withn a Virtual Environment. Please refer to Lab 3's instructions and resources before trying to do this mini project.

# What does it do?
It allows ```users``` to remotely set the LED colors from the SenseHAT attached to a ```device``` (RPi).


## Technical information
### Deployment diagram
<p align="center" width="100%">
   <img src="images/deployment_diagram.png" width="80%" margin-left="auto" margin-right="auto">
</p>

### DB Schema
<p align="center" width="100%">
   <img src="images/db_schema_sample.png" width="60%" margin-left="auto" margin-right="auto">
</p>

### Sequence diagram
<p align="center" width="100%">
   <img src="images/sequence_diagram.png" width="100%" margin-left="auto" margin-right="auto">
</p>

## The scripts
### The [backend.py](backend.py)
The [backend.py](backend.py) script has the ```Backend()``` class, which contains all the operations related to the database. For example: setting up users, devices, and configurations, as well as setting up the LED colors. It uses the configuration file (```mydbconfig.py```) to set and get values from the firebase database.

### The [device.py](device.py)
The [device.py](device.py) script should be executed on your RPi. It also interacts with the database using functions defined in [backend.py](backend.py) and user configuration information from ```mydbconfig.py```. When you execute the script for the first time, the device and user will be added to the database, and the LED display will be initialized with initial RGB colors.

The next time you execute the [device.py](device.py) script, it will get the color values for the LED display from the database and set the SenseHAT LED display accordingly. While the script is running, it will *listen* for changes in the database by using [firebase streams](https://github.com/nhorvath/Pyrebase4#streaming). In other words, whenever any authorized user changes the LED color using the GUI, a message is received by [device.py](device.py), and the callback function associated with the Firebase stream updates the pixel(s) accordingly.

## Authorizing users to control your sense hat LED display
Registered users in the database can be authorized to control your sense hat LED display. In fact, you should authorize your teammates to control your device. You can achieve this by creating a file with the code below (with their respective emails).
```
from backend import Backend
from mydbconfig import *
backend = Backend(config, email, firstname, lastname)

# Add each of your teammates'
backend.add_authorized_users('my_group_mate1_email@cmail.carleton.ca' )
backend.add_authorized_users('my_group_mate2_email@cmail.carleton.ca' )

```

## The [frontend.py](frontend.py)
The [frontend.py](frontend.py) script provides a GUI implemented using [dash](https://dash.plotly.com/). Like the [device.py](device.py) script, [frontend.py](frontend.py) interacts with the database using functions defined in [backend.py](backend.py) and user configuration information from ```mydbconfig.py```. When you execute the [frontend.py](frontend.py) file, a [flask](https://flask.palletsprojects.com/en/2.0.x/) server runs in the background (note that dash is built on top of Flask, so you will not see the Flask code directly). The GUI can be accessed from your local network through the address ```<frontend_ip>:8050```, where ```frontend_ip``` is the IP address of the device where the [frontend.py](frontend.py) script is being executed. It can be run at the same RPi as the [device.py](device.py) script, or on your own computer.

Once you know the **IP address** of the device where you are running the [frontend.py](frontend.py) script, you can access it through your local network by typing the URL (```<frontend_ip>:8050```) in a web browser (from your smartphone, or computer, or through the web browser of your RPi, ...).  This is how it will look like if accessed from your smartphone:

<p align="center" width="100%">
   <img src="images/lab4_frontend_sample.png" width="40%" margin-left="auto" margin-right="auto">
</p>


Note that the GUI can be run from any computer and can change the LED colors of any device for which the user is authorized. The idea of this project is that any one of your teammates can change the SenseHAT pixels of your RPi.

# Install
There are packages required for this mini-project. You can manually install them  using the command below, **or** using bash (from your RPi) using the [install.sh](install.sh) script by running the command ```./install.sh```. **Important: you must create and activate a VENV virtual environment (see Lab3 Instructions that explain how to create and activate a Python virtual environment) prior to running the [install.sh](install.sh) script, since it launches pip.**

```
pip3 install pyrebase4 dash dash_daq dash-extensions coloredlogs
```

# Config
To use the Firebase database, you need to first create a Firebase database as performed in Lab3. The schema for the database is shown above and it will be populated automatically when the [device.py](device.py) script is run by each user.
Once the database is up and running, you need to provide the configuration information for the database, and for each user. A sample file can be found in [here](dbconfig.py). You should then copy the file
```
cp dbconfig.py mydbconfig.py
``` 
and edit its contents. The file should contain:
1. Your ```email```
2. Your ```firstname```
3. Your ```lastname```
4. The firebase configuration ```config```

**> These variables are used by many files and should be set for things to work properly.**

The ```mydbconfig.py``` file should not be included in the repository since it has sensitive information about the user and database. In addition, each student will have in common the config variable (database configuration), but the user information should be different for each student. To avoid pushing the file to your remote repository, just include the file in the ```.gitignore``` file. You must create the ```.gitignore```  file and add one line for each file to be ignored when pushing local changes to the repo. You can even ignore other directories and patterns in files. For example, the ```__pycache__``` should not be included in your repository. Your ```.gitignore``` file will look like this:
```
mydbconfig.py
*__pycache__*
```

# Deliverables

Before you get started, 
1. Assign a student to create the Firebase real-time database. 
2. Share the connection details amongst all members of the team. Everyone will need this information for their ```mydbconfig.py``` files so that their [backend.py](backend.py) script knows how to access the shared Firebase real-time DB.

## Each student

### Setup
#### Step 1
Create your ```mydbconfig.py``` file. It should have the connection configuration information for your team's Firebase database and your own user information (name, email). This file should not be included in the GitHub repository. More information in the [Config](#config) section.

#### Step 2

Execute the [device.py](device.py) script on your RPi. The owner of the Firebase database should be able to visualize the new entries in his database. More information about how the [device.py](device.py) script works can be found [here](device.py).

#### Step 3
Create a file to give authorization to your teammates to control your Raspberry pi. Each student should have their own file, and it should not be included in your repository. You can execute it as many times as you want, but you only need to do it once (once all users have executed [Step 2](#step-2)). More information about authorizing other users to control your device can be found [above](#authorizing-users-to-control-your-sense-hat-led-display).

#### Step 4
Execute the [frontend.py](frontend.py) script to control your authorized devices. Since you executed the [device.py](device.py) script on your RPi, you have at least one device to control. Once your teammates give authorization for you to control their devices, you will see more device options to control. 

You can execute this file on your RPi, then verify the RPi IP address, and access it from your computer's web browser using the URL ```<RPI_IP_address>:8050```.

<details><summary>For advanced users 😎 </summary>
<p>
You can execute the [frontend.py](frontend.py) script from your own computer. To access it from your local network you just need the IP address of your computer instead of the RPi. In addition, you need to install the required packages. The required packages can be found in the installation script [install.sh](install.sh).
</p>
</details>

<!--
Once the database is setup and the mydbconfig.py is set, each student should run the [device.py](device.py) so that their device is registered on the database. 

The device (RPi) will be registered under the user configuration. But, each student should give authorization to their teammates to control their own SenseHAT display/device (see instructions above) -->

### GitHub and git tasks
1. Open at least 4 issues and assign a label to each
2. Assign the issues to your team members, ensuring each member receives at least one issue.
3. Each team member should create a new branch to work on their assigned issue(s)
4. Commit all your changes to your newly created branch
5. Once the code reflects your final solution, create a pull request to merge your new branch with the main branch and resolve your assigned issue.
6. Before merging the pull request, have at least one *other* teammate review your code. You can discuss any concerns in the pull request's "discussions" section on GitHub.
7. Once you and your teammates are satisfied with the solution, merge the pull request. Ensure the person who merges the pull request is different than the one who opened it originally.

### Issues
1. Capability to erase all LEDs.
   - Add a function in the [device.py](device.py) script to continuously check the joystick and set all the values of the LEDs to ```[0,0,0]``` if/when the joystick is pressed down.
     - Inside this newly created function you should call (```clear_leds(device_id)```) from the Backend to clear all LEDs. **DO NOT** call the ```sense.set_pixels(...)```  function (otherwise the database will not be updated). The device ID can be acquired with the function ```get_device_id()```, which is also found in the Backend class.
2. Update the header/title string in the GUI
    - Update the ```subheader``` value from the [frontend.py](frontend.py) script to list the names of each group member instead of Just one name. **BONUS** list the members who have access to your pi.
3. Add image samples
   - Take nice screenshots from your teammates' LED screens and add them to the [images](images) folder.
4. Update the README
   - Create a new "main" section, after [Deliverables](#deliverables), called "Demonstration". Using markdown, display the images that you took under this new section.
   - Create a [table of contents](https://gist.github.com/jonschlinkert/ac5d8122bfaaa394f896) for this README that, at the very least, contains all the top-level headers (What does it do?, Install, Config, etc.). Place the table of contents before the [What does it do?](#what-does-it-do) section. 

<!--**Note**: Issues 3 and 4 should be completed by a single student (in a single issue) if you belong to a team of three. If you belong to a team of four, they should be addressed separately by two different students, and in separate issues.-->

# 5G OA&M Automation and IP Protocol Simulation Platform

## Overview
This platform provides OA&M automation, KPI monitoring, event simulation, and IP protocol simulation for 5G/LTE networks, with a web dashboard for visualization.

## Project Structure
- `main.py` — Entry point to start the platform
- `platform.py` — Main controller, wires all modules together
- `oam.py` — OA&M automation module
- `kpi.py` — KPI monitoring module
- `event.py` — Event simulation module
- `ip_sim.py` — IP traffic simulation module
- `dashboard.py` — Web dashboard module
- `requirements.txt` — Python dependencies

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the platform:
   ```bash
   python main.py
   ```

## Notes
- The dashboard runs on Streamlit (default port 8501).
- Some features require `scapy` and `streamlit` to be installed.
- Logs are written to `oam_platform.log`.

