
# Software Management System

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT) ![Python3Version](https://img.shields.io/badge/python-%3E%3D3.6-green) 

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

Out system aims at ensuring the security and authorization of all software and patches installed on terminal devices (i.e., clients) within a company. 

The primary goal is to eliminate potential risks and vulnerabilities that could compromise the company's assets.

## Features

- **Software Tracking & Management**: The system allows administrators to track and manage software installations on client devices and provides real-time insights into the software installed on each device.
- **Security Patch Monitoring**: The system can monitor the security patch status of client devices, automatically detect outdated patches, and notify administrators to apply the latest updates promptly.
- **Authorization Control**: The system ensures that unauthorized software and outdated security patches installed on client devices are reported to the managers, preventing the use of unapproved applications and reducing potential vulnerabilities.
- **Malware Detection Function**: The system incorporates a malware detection function that allows users to upload executable files for safety analysis. It employs advanced scanning algorithms to detect potential malware and security threats.
- **Remote Web Access**: The server provides a secure web interface that allows users and managers to access the server from anywhere with proper authentication. (SMMS is deployed on LAN by default)
- **User-Friendly Interface**: The admin web interface is designed with a user-friendly approach, making it intuitive and easy to navigate. Even non-technical users can quickly learn to use it effectively.
- **Data Security and Privacy**: The system prioritizes data security and privacy. It employs encryption and access control mechanisms to safeguard sensitive information.
- **Scalable and Customizable**: The SMMS is designed to be scalable and customizable, enabling easy integration with existing software and systems. Organizations can tailor the system to suit their specific needs and scale it according to their requirements.

## Usage

 To be continued...

## Getting Started

 To be continued...

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

## Acknowledgments

Special thanks to all contributors who have helped in the development of this system.

---

*Note: This README provides an overview of the Software Monitoring & Management System. For detailed installation and usage instructions, please refer to the sub-project documentation.*

