# Install ODOO 10 on Debian 8

To install Odoo 10 on Debian-based distribution in mode production execute the following commands as root:

```bash
$ wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
$ echo "deb http://nightly.odoo.com/10.0/nightly/deb/ ./" >> /etc/apt/sources.list.d/odoo.list
$ apt-get update && apt-get install odoo
```

## Configure Postgresql

Create a user and database to odoo
 
```sql
$ createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo
```



## Install Odoo mode development


## Create a user to Odoo

```bash
$ adduser --system --home=/opt/odoo --group odoo
```


Login with the user odoo:

```bash
$ su - odoo -s /bin/bash 
$ cd /opt/
```

Install git

```bash
$ sudo apt install git
```

#### Clone the repository

```bash
$ git clone https://github.com/odoo/odoo.git --depth 1 --branch 10.0 --single-branch odoo
```

#### Create a virtualenv:

First install virtualenv. ```Execute next command as root```:

```
$ apt install python-virtualenv
```

Now position in your home:

```
$ cd
```

Create virtualenv. 

```
$ virtualenv odoo-dev
```

Activate virtualenv. 

```
$ . odoo-dev/bin/activate
```

Make sure you have installed:

```bash

$ apt install curl

$ sudo curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash 

$ sudo apt install -y nodejs

$ sudo npm install --global npm@latest

$ sudo npm install -g less

$ sudo npm install -g less-plugin-clean-css
```

and

```bash
$ apt install build-essential git-buildpackage python-all-dev postgresql-9.4 postgresql-client-9.4 libldap2-dev libsasl2-dev libssl-dev libxslt1-dev libxml2-dev libpq-dev libjpeg-dev
```

Now install dependencies. 

```bash
$ pip install -r /opt/odoo/requirements.txt 
```

Now move to /opt/

```bash
$ deactive
```

and ```execute this command as root```:

```bash
$ mv odoo-dev /opt/
```

Change owner ```execute this comman as root```:

```bash
$ sudo choown odoo: odoo-dev
```


### Configuration Odoo

Copy the configuration base to ```/etc/odoo``` ,execute the following commands as root:


```
$ cp /opt/odoo/debian/odoo.conf /etc/odoo/odoo.conf
```

Change owner 

```
$ chown odoo: /etc/odoo/odoo.conf
```

Change permissions

```
$ chmod 640 /etc/odoo/odoo.conf
```

### Now edit file ```/etc/odoo/odoo.conf```

Change the field ```db_password = False``` for:

```bash
db_password = "your-password"
```

##### NOTE: The password corresponds to the user created in postgres


Change the path the addons:

```bash
addons_path = /opt/odoo/addons
``` 

Add a log file:

```bash
logfile = /var/log/odoo/odoo-server.log 
``` 

Now create the directory:

```
$ mkdir /var/log/odoo
```

Change owner

```
$ chown odoo:root /var/log/odoo/
```

And finnish the configuration the server


## Test the server the Odoo

Login with the user odoo

```bash
$ su - odoo -s /bin/bash
```

Activate virtualenv:

```bash
$ . /opt/odoo-dev/bin/activate
```

Execute the server

```bash
$ /opt/odoo/odoo-bin
```

##### Check your browser in ```https://your-ip:8069/``` or ```https://localhost:8069/```


## SOURCES

http://odooperu.org/?p=944
