# Install ODOO 8.0  in Debian 8

To install Odoo 8.0 on Debian-based distribution, execute the following commands as root:

```bash
$ wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
$ echo "deb http://nightly.odoo.com/8.0/nightly/deb/ ./" >> /etc/apt/sources.list
$ apt-get update && apt-get install odoo
```

## Create a user to Odoo

```bash
$ adduser --system --home=/opt/odoo --group odoo
```

## Configure Postgresql

Create a user and database to odoo
 
```sql
$ createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo
```

## Install the server to Odoo

Login with the user odoo:

```bash
$ su - odoo -s /bin/bash 
$ cd ..
```

#### Clone the repository

```bash
$ git clone https://github.com/odoo/odoo.git --depth 1 --branch 8.0
```



```

```

```

```

