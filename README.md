<h1 align='center'>AutoCookie - Automatically loading stolen cookies from ChromePass</h1>
<p align="center">	
    <img src="https://img.shields.io/badge/Platform-Windows-green" />
	<a href="https://github.com/darkarp/autocookie/releases/latest">
	<img src="https://img.shields.io/github/v/release/darkarp/autocookie" alt="Release" />
	</a>
  <a href="#">
    <img src="https://img.shields.io/badge/build-passing-green" alt="Build Status on CircleCI" />
	</a>
    <img src="https://img.shields.io/maintenance/yes/2021" />
	</br>
  
  <a href="https://github.com/darkarp/autocookie/commits/master">
    <img src="https://img.shields.io/github/last-commit/darkarp/autocookie" />
  </a>
  <img alt="Scrutinizer code quality (GitHub/Bitbucket)" src="https://img.shields.io/scrutinizer/quality/g/darkarp/autocookie?style=flat">
  <a href="https://github.com/darkarp/autocookie/blob/master/LICENSE">
    <img src="http://img.shields.io/github/license/darkarp/autocookie" />
  </a>
  </br>
  <a href="https://github.com/darkarp/autocookie/issues?q=is%3Aopen+is%3Aissue">
	<img alt="GitHub issues" src="https://img.shields.io/github/issues/darkarp/autocookie">
</a
<a href="https://github.com/darkarp/autocookie/issues?q=is%3Aissue+is%3Aclosed">
	<img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/darkarp/autocookie">
</a>
</br>
  <a href="https://discord.gg/beczNYP">
    <img src="https://img.shields.io/badge/discord-join-7289DA.svg?logo=discord&longCache=true&style=flat" />
  </a>
  </br>
    <a href="https://i.imgur.com/qaa1BSP.gif" target="_blank">View Demo</a>
    ·
    <a href="https://github.com/darkarp/autocookie/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/darkarp/autocookie/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>  
  
  
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)  
* [Getting started](#getting-started)
  * [Prerequisites](#dependencies-and-requirements)
  * [Installation](#installation)
* [Usage](#usage)
* [Errors, Bugs and Feature Requests](#errors-bugs-and-feature-requests)
* [Learn More](#learn-more)
* [License](#license)
---
## About The project
AutoCookie requires the data acquired using [ChromePass](https://github.com/darkarp/chromepass) or data in the same [format](#the-chromepass-data-format).  


It's a python-based console application that starts a browser with the following features:

  - Automatically detects victims who have cookies on the website you're in.
  - Automatically loads cookies for the chosen victim on that browser session.

---

## Getting started

### Dependencies and Requirements

This is a very simple application, which uses only:

* [Python] - Tested on python 3.6+
* [Firefox] - It requires Firefox to run. Instead of adding support for many browsers, having to deal with the problems of each one, it runs with Firefox, the most stable browser by far to run with selenium.

### Installation

Autocookie can be used in any operating system but it requires the stolen cookies obtained from [ChromePass](https://github.com/darkarp/chromepass) or the same [format](#the-chromepass-data-format).



Clone the repository:
```powershell
git clone https://github.com/darkarp/autocookie
```

Install the dependencies:

```powershell
cd autocookie
pip install -r requirements.txt
```

If any errors occur make sure you're running on the proper environment (if applcable) and that you have python 3.6+
If the errors persist, try:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```  

---

## Usage

AutoCookie is very straightforward. Start by running:
```powershell
> python autocookie.py
```
A browser window will show up. Here, you can navigate to any website you want.  

On the terminal window you will be notified whether any victims were found to have cookies for that particular website.  

All you have to do is either select the victim you'd like to load, or skip loading for that website.

If victims were found for a website and you change the url on the browser, you must skip the prompt on the terminal before it can recognize that the url has changed.

### Notes
>This is a very early release with just the basic functionality.    
`Refactorization` and `support for multiple cookie files from the same ip address`, as well as `command-line parameter-based usage` will be added in the future. 
  
---  

## The ChromePass data format
This format is a base directory called `data`. Inside are folders named after the victim's `ip_address`. Inside there are files named `cookie0.json`, `cookie1.json`.  
An example:  

![Data directory list](https://i.imgur.com/j7fwj5A.png)  

The `login` files are useless for the `AutoCookie`, we're only interested in the `cookie` files.  
Inside the `cookie` json files, the structure is as follows:
```json
{
  "domain_name_1": [{
        "name": "COOKIE_NAME",
        "value": "COOKIE_VALUE",
        "domain": "domain_name"
    }, {
        "name": "COOKIE_NAME",
        "value": "COOKIE_VALUE",
        "domain": "domain_name"
    }],
    "domain_name_2": [{
        "name": "COOKIE_NAME",
        "value": "COOKIE_VALUE",
        "domain": "domain_name"
    }, {
        "name": "COOKIE_NAME",
        "value": "COOKIE_VALUE",
        "domain": "domain_name"
    }, {
        "name": "COOKIE_NAME",
        "value": "COOKIE_VALUE",
        "domain": "domain_name"
    }],
}
```
>The `login` json files are not needed but the whole directory structure must be present.
---
 
## Errors, Bugs and feature requests

If you find an error or a bug, please report it as an issue.
If you wish to suggest a feature or an improvement please report it in the issue pages.

Please follow the templates shown when creating the issue.  

---

## Learn More

For access to a community full of aspiring computer security experts, ranging from the complete beginner to the seasoned veteran,
join our Discord Server: [WhiteHat Hacking](https://discord.gg/beczNYP)

If you wish to contact me, you can do so via: `mario@whitehathacking.tech` 

---

## Disclaimer
I am not responsible for what you do with the information and code provided. This is intended for professional or educational purposes only.

## License
<a href="https://github.com/darkarp/autocookie/blob/master/LICENSE"> MIT </a>
  
---
[Python]: <https://www.python.org/downloads/>
[Firefox]: <https://www.mozilla.org/en-US/firefox/new/>
[![Code Intelligence Status](https://scrutinizer-ci.com/g/darkarp/autocookie/badges/code-intelligence.svg?b=main)](https://scrutinizer-ci.com/code-intelligence)