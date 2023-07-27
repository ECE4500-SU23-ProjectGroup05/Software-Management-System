
# Software Management System

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT) ![Python3Version](https://img.shields.io/badge/python-%3E%3D3.6-green) ![DjangoVersion](https://img.shields.io/badge/Django-%3E%3D3.2-green) 

The Software Monitoring & Management System, part of the Capstone Design Project (Group05) of SJTU UMJI.

### Capstone Design Project

Our capstone design focuses on developing comprehensive solutions for managing information security in large-scale multinational corporations. 

Our project involves designing and implementing the system to ensure the security and integrity of data, software, and networks in the manufacturing domain within the organization.

## Table of Contents

- [Overview](#overview) 
- [Features](#features) 
- [Usage](#usage) 
- [Getting Started](#getting-started) 
- [Requirements](#requirements)
- [Contributing](#contributing) 
- [License](#license) 

## Overview

In many organizations, managing software and patches installations and updates is a complex task and a critical part of business administration.

The **Software Monitoring & Management System** (SMMS) provides a comprehensive solution to **track and manage software and on client devices**. It allows managers to monitor and control software authorization and ensure that all devices have the latest security patches installed.

The SMMS also incorporates a **malware detection function** in admin interface to further enhance the security of the organization's assets.

### Objective

Out system aims at ensuring the security and authorization of all software and patches installed on terminal devices (i.e., clients) within a company. The primary goal is to eliminate potential risks and vulnerabilities that could compromise the company's assets.

## Features

- **Software Tracking & Management**

  The system allows administrators to track and manage software installations on client devices and provides real-time insights into the software installed on each device.

- **Security Patch Monitoring**

  The system can monitor the security patch status of client devices, automatically detect outdated patches, and notify administrators to apply the latest updates promptly.

- **Authorization Control**

  The system ensures that unauthorized software and outdated security patches installed on client devices are reported to the managers, reducing potential vulnerabilities.

- **Malware Detection Function**

  The system incorporates a malware detection function that allows users to upload executable files for safety analysis. It employs RCNN to detect potential malware and security threats.

- **Remote Web Access**

  The server provides a secure web interface that allows users and managers to access the server from anywhere with proper authentication. (SMMS is deployed on LAN by default)

- **User-Friendly Interface**

  The admin web interface is designed with a user-friendly approach, making it intuitive and easy to navigate. Even non-technical users can quickly learn to use it effectively.

- **Data Security and Privacy**

  The system prioritizes data security and privacy. It employs encryption and access control mechanisms to safeguard sensitive information.

- **Scalable and Customizable**

  The SMMS is designed to be scalable and customizable, enabling easy integration with existing software and systems. Organizations can tailor the system to suit their specific needs and scale it according to their requirements.

## Usage

To effectively use the Software Monitoring & Management System (SMMS), follow these steps: 

1. **Start the Server**

   - Follow the instructions provided in the [server-side README](https://github.com/ECE4500-SU23-ProjectGroup05/server_side) to set up the SMMS server on your machine.
   - Ensure that the server is running and ready to accept connections from client devices.

2. **Start the Clients**

   - Refer to the [client-side README](https://github.com/ECE4500-SU23-ProjectGroup05/client_side) for instructions on setting up the SMMS client application on individual client devices.
   - Make sure the clients are connected to the same Local Area Network (LAN) as the server.

3. **Edit Settings (Client-side)**

   - Open the `settings.yml` file in the client application folder and customize the configurations to your preferences.
   - Configure the `server-IP` and `port` fields to match the IP address and port of the SMMS server.

4. **Run the Client Application**

   - Open the client application (`MyClient.exe` on Windows or `MyClient.py` on other platforms) on each client device.
   - The client application will automatically send software information to the server when connected and at intervals specified in the settings.

5. **Access the Server Web Interface**

   - Open your preferred web browser and enter the IP address and port of the SMMS server (e.g., http://192.168.31.236:8000).
   - The server's web interface allows you to monitor and control software authorization from anywhere with proper authentication.

6. **Log in to the Admin User Interface**

   - For more detailed control and monitoring, log in to the admin page using the default credentials:
     - Username: `admin`
     - Password: `admin@uaes`
   - After logging in for the first time, it is essential to change the password immediately for enhanced security.

7. **Configure Email Settings (Server-side)**

   - Open the `settings.yml` file in the server application folder and customize the configurations for email notifications.
   - Replace the `sender` and `pwd` fields with your email address and email credentials for sending notifications.
   - Change the `smtp` server to match the email server you are using.
   - Set the `interval` to the desired number of days for sending notification emails. For example, setting `interval=7` will send notifications every week.

8. **Manage Whitelist (Server-side)**

   - In the admin page, you can import applications using a `.csv` file or manually add them to the whitelist to control authorized software.
   - Make sure to apply changes to the whitelist to update the authorization settings.

9. **Monitor Unauthorized Apps (Server-side)**

   - The admin page allows you to search for unauthorized applications quickly and take appropriate actions.

## Getting Started

To get started with the Software Monitoring & Management System (SMMS), follow these steps:

1. **Clone the Repository**

   - Clone the SMMS server-side repository from GitHub using the following command:

     ```bash
     git clone https://github.com/ECE4500-SU23-ProjectGroup05/server_side.git
     ```

   - Clone the SMMS client-side repository from GitHub using the following command:

     ```bash
     git clone https://github.com/ECE4500-SU23-ProjectGroup05/client_side.git
     ```

2. **Install Python**

   - Make sure you have Python installed on your computer. If you don't have it, go to the Python archives page and download Python: https://www.python.org/downloads/

3. **Install Required Packages (Server-side)**

   - Navigate to the `server_side` folder in the terminal or command prompt and install the necessary Python packages by running:

     ```bash
     pip install -r requirements.txt
     ```

4. **Install Required Packages (Client-side)**

   - Navigate to the `client_side` folder in the terminal or command prompt and install the necessary Python packages by running:

     ```bash
     pip install -r requirements.txt
     ```

5. **Check Router Settings (Server-side)**

   - Ensure that your router's settings do not have "AP isolation" enabled. This setting may prevent client devices from connecting to the server.

6. **Configure Firewall Settings (Server-side)**

   - Before running the server, ensure that your computer's firewall allows Python to receive incoming connections from both Local Area Network (LAN) and Wide Area Network (WAN).

   - Firewall settings may vary based on the operating system you are using. Please refer to your OS documentation or system settings to configure the firewall properly.

7. **Find Your IPv4 Address (Server-side)**

   - Open the terminal or command prompt and find your computer's IPv4 address using the following command:

     ```bash
     ipconfig /all
     ```

   - Locate the `IPv4 Address` in the output.

8. **Start the SMMS Server (Server-side)**

   - In the `server_side` folder, run the SMMS server on your server machine by executing the following command:

     ```bash
     python manage.py runserver YOUR_IPV4_ADDRESS:8000
     ```

   - Replace `YOUR_IPV4_ADDRESS` with your actual IPv4 address obtained from Step 7. The server will start running on port 8000.

   - Make sure the port (8000 in this example) is not blocked by any firewall or network settings.

9. **Access the Web UI (Server-side)**

   - The SMMS web interface enables convenient software management and client device monitoring from any device within the LAN using the server's IP address and port.

   - Open your preferred web browser and enter the IP address and port of the SMMS server (e.g., http://192.168.31.236:8000).

10. **Run the SMMS Client (Client-side)**

    - Follow the instructions provided in the "Run the Client Application" section of the "Usage" instructions above to start the SMMS client on each client device.

Congratulations! You have successfully set up and started using the Software Monitoring & Management System (SMMS). Enjoy the benefits of efficiently tracking, managing, and controlling software and patches on your client devices within the organization.

## Requirements

- Python >= 3.6
- Django framework
- Database (SQLite3 by default)
- Other dependencies (refer to [requirements.txt](./requirements.txt) for the complete list)

## Contributing

Contributions to the Software Management System are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

Guidelines [[How to contribute]](./guidelines/contributions.md) for pull requests and code contributions.

## License

The Software Management System is open-source software licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

Be sure to preserve the copyright when in using.

## Acknowledgments

Special thanks to all contributors who have helped in the development of this system. Our Capstone Design Project is sponsored by UAES.

#### Links to sub-projects

- [ECE4500-SU23-ProjectGroup05/client-side](https://github.com/ECE4500-SU23-ProjectGroup05/client_side) 
- [ECE4500-SU23-ProjectGroup05/server-side](https://github.com/ECE4500-SU23-ProjectGroup05/server_side) 
- [ECE4500-SU23-ProjectGroup05/malware-detection](https://github.com/ECE4500-SU23-ProjectGroup05/mal_detection) 

---

*Note: This README provides an overview of the Software Monitoring & Management System. For detailed installation and usage instructions, please refer to the sub-project documentation.*

