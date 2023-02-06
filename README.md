
# Brokerboss
## Introduction

BrokerBoss is an open-source web application that helps you set up and manage a Mosquitto MQTT broker with ease. With Brokerboss, you can avoid the hassle of dealing with command line tasks or configuration files.

### Screenshots
![broker config](docs/screenshots/Screenshot_broker_config.png?raw=true)
![users](docs/screenshots/Screenshot_users.png?raw=true)
![ACL config](docs/screenshots/Screenshot_ACL.png?raw=true)

### Purpose

The purpose of Brokerboss is to simplify the process of setting up and managing a Mosquitto MQTT broker. It provides a user-friendly interface and REST api endpoints for performing common broker tasks (like restarting the broker or adding users). BrokerBoss allows you to focus on your MQTT projects without getting bogged down in command line commands and configuration files. By using Brokerboss, you can get your broker up and running quickly and easily, freeing up time and resources to concentrate on other important aspects of your projects.

### Features

- Easy setup and configuration of a mosquitto MQTT broker
- User-friendly interface for managing broker tasks
- Avoid the hassle of dealing with command line commands and configuration files
- Manage settings and security options
- Monitor broker activity and connected clients (coming soon)
- Quick and simple access to broker logs
- Start, stop, and restart broker services with a click of a button
-  Start, stop, and restart broker services through the API
- Fast and efficient way to get a broker up and running.
- No need for prior MQTT or broker administration experience
- Enable/Disable API endpoints
- Export and backup configuration files
- Import configuration files (coming soon)
- Quickly and easily configure your Acces Control List
- Add user or pattern based rules to control who has access to what topics

### Who is this for?


### What BrokerBoss is and isn't
BrokerBoss is actively being developed right now. It has all basic features needed to setup and manage your MQTT broker. This project is for people who want to set up an mqtt broker and prefer a graphical user interface to do so.  However, since it is very new and relatively untested it might still contain bugs or security issues. Therefore it is not recommenced to expose BrokerBoss to the internet or to use it in production. Right now it's more suited for home projects like a Broker on your LAN for [Home Assistant](https://www.home-assistant.io/) and even that might be a stretch. As the project expands BrokerBoss will become more resilient and secure.

### Where does this tool come from?
I built this tool after working on an IoT project that needed a lot of broker tweaking. I didn't seem to find the thing I needed and decided to build and open source it. 

## Get started
The easiest way to get started with Brokerboss is to run it using Docker. 
1. To do this, copy or clone the repo to your local machine. 
 
2. Open your terminal (the irony isn't lost on me) and navigate to the folder that contains the repo using cd:
 `cd /the/path/to/the/folder`

3. Build the necessary containers using docker-compose
 `docker-compose build`

4. Start the containers using the command:
 `docker-compose up`

5. Now you should be able to navigate to the BrokerBoss web application with your browser.
 Go to `localhost:5000` in your favourite webbrowser.


#### Requirements
For now you need docker and docker-compose



## Contribute

Do you want to help? That’s awesome. Contributions of all kinds from everyone are welcomed.

Here are some of the things you can do to help.

### Contribute as a community

- Share your experiences with Brokerboss and spread the word about its capabilities. Write about it in your blog, or share your thoughts on social media platforms like Twitter and Facebook.
- If you have an idea for a new feature or have found a bug, please open an issue on the repository.
- Help others in the community by answering questions and providing support in the issue tracker.  

### Contribute as a developer

- Read our [Contribution Guide]()

## Thank you, open source

Brokerboss wouldn't be possible without the contributions of several open source projects. Hopefully this tool can assist others in the same way the open source projects helped us.

# License

BrokerBoss is licensed under the GNU GPLv3 License.
