# Install ODOO 10 on Debian 8

Follow the next steps to install odoo 10 en debian 

## Install Odoo mode development

I will explain step by step how to install oudoo


## Install Dependencies

```bash
$ apt install git build-essential git-buildpackage python-all-dev postgresql-9.4 postgresql-client-9.4 libldap2-dev libsasl2-dev libssl-dev libxslt1-dev libxml2-dev libpq-dev libjpeg-dev
```

## Install dependencies to frontend

```bash
$ apt install curl

$ sudo curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash 

$ sudo apt install -y nodejs

$ sudo npm install --global npm@latest

$ sudo npm install -g less

$ sudo npm install -g less-plugin-clean-css
```

### Clone the repository

```bash
$ git clone https://github.com/odoo/odoo.git --depth 1 --branch 10.0 --single-branch odoo
```

### Clone repository addons of GEEKOS

```
$ git clone https://github.com/Pdosplusplus/p2-odoo.git
```

### Create a virtualenv:

First install virtualenv. ```Execute next command as root```:

```
$ apt install python-virtualenv
```

Now position in your home:

```
$ cd
```

### Create virtualenv. 

```
$ virtualenv odoo-dev
```

Activate virtualenv. 

```
$ . odoo-dev/bin/activate
```

### Now install dependencies own odoo 10. 

```bash
$ pip install -r /opt/odoo/requirements.txt 
```

### Creater user in postgresql

Now we will create a user to manage the databases. In my case the user will be ```victor```

```
$ createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt victor
```

### Configuration Odoo

Now create the file to run the serve of odoo 

Create a file the name ```odoo.conf``` with the following content:

```
[options]
addons_path = /home/victor/Working/odoo/odoo/addons,/home/victor/Working/odoo/addons,/home/victor/Working/p2-odoo/odoo-10/addons
admin_passwd = admin
csv_internal_sep = ,
data_dir = /home/victor/.local/share/Odoo
db_host = False
db_maxconn = 64
db_name = False
db_password = False
db_port = False
db_template = template1
db_user = victor
dbfilter = .*
demo = {}
email_from = False
geoip_database = /usr/share/GeoIP/GeoLiteCity.dat
import_partial = 
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 60
limit_time_real = 120
limit_time_real_cron = -1
list_db = True
log_db = False
log_db_level = warning
log_handler = :INFO
log_level = info
logfile = None
logrotate = False
longpolling_port = 8072
max_cron_threads = 2
osv_memory_age_limit = 1.0
osv_memory_count_limit = False
pg_path = None
pidfile = None
proxy_mode = False
reportgz = False
server_wide_modules = web,web_kanban
smtp_password = False
smtp_port = 25
smtp_server = localhost
smtp_ssl = False
smtp_user = False
syslog = False
test_commit = False
test_enable = False
test_file = False
test_report_directory = False
translate_modules = ['all']
unaccent = False
without_demo = False
workers = 0
xmlrpc = True
xmlrpc_interface = 
xmlrpc_port = 8069
```
You have change the value of ```addons_path``` for the path where you install odoo example

```
/home/victor/Working/odoo/odoo/addons for /home/your_user/odoo/odoo/addons
/home/victor/Working/odoo/addons for /home/your_user/odoo/addons 
/home/victor/Working/p2-odoo/odoo-10/addons for /home/your_user/p2-odoo/odoo-10/addons 
```

Also yo have change the value of ```db_user``` for you user.

And to finish change the value of ````data_bir``` for ```/home/your_user/.local/share/Odoo```

### Run server

Activate your virtualenv, posicion in the folder of odoo and execute:

```
./odoo-bin -c odoo.conf
```

##### Check your browser in ```https://your-ip:8069/``` or ```https://localhost:8069/```


## SOURCES

http://odooperu.org/?p=944
