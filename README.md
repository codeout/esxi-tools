# ESXi tools for JANOG44 hackathon

## Requirements

* Python 3.x
  * Hopefully. Haven't tested all versions.
  * Tested 3.7.3 only
* Python 2.x won't be supported


## Installation

```shell
$ pip install -r requirements.txt
```


## How to use

### 1. Network diagram server

1. Start server

```shell
$ PASSWORD="Your ESXi password" python diagram.py -H ESXI_HOST -u ESXI_USER
```

2. Access to http://localhost:5000/static/index.html


### 2. List mac address

```shell
$ PASSWORD="Your ESXi password" python diagram.py -H ESXI_HOST -u ESXI_USER PORTGROUP_NAME
```
