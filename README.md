# Install ODOO 8.0 on Debian 8

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

Install git

```bash
$ sudo apt install git
```

#### Clone the repository

```bash
$ git clone https://github.com/odoo/odoo.git --depth 1 --branch 8.0
```

#### Configuration Odoo

Copy the configuration base to ```/etc``` ,execute the following commands as root:

```
$ cp /opt/odoo/debian/openerp-server.conf /etc/odoo-server.conf
```

Change owner 

```
$ chown odoo: /etc/odoo-server.conf
```

Change permissions

```
$ chmod 640 /etc/odoo-server.conf
```

### Now edit file ```/etc/odoo-server.conf```

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

Execute the server

```bash
$ /opt/odoo/openerp-server
```

##### Check your browser in ```your-ip:8069``` or ```localhost:8069```


## Create a Module

first create a directory to modules:

```bash
$ mkdir local_addons
```

Now the directory of the module:

```bash
$ cd local_addons
$ mkdir modu_test
```

### The struct basic of a module is:


```bash
name_module/
├── __init__.py
├── __openerp__.py
├── name_module.py 
└── name_module_view.xml
```


### Now create the file ```__openerp__.py``` with the following content:


```python
{
    'name':'Geekos',
    'version': '1.0',
    'depends': ['base_setup'],
    'author': 'Victor Pino victopin0@gmail.com',
    'category': '',
    'description': """
    Module the test
    """,
    'update_xml': [],
    "data" : [
        "modu_test_view.xml",
        ],
    'installable': True,
    'auto_install': False,
}
```


### Create the file ```modu_test.py``` with the following content:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-


from openerp.osv import fields, osv

class modu_test(osv.osv):
    """docstring for modu_test"""
    _name="modu.test"

    _columns={
        'date': fields.date('date'),
        'name': fields.char('name', 
                            size=30, 
                            required=True, 
                            help="Name of the pupil"),
        'di': fields.integer('di',
                            size=10,
                            required=True,
                            help="Document Identification"),
        'note': fields.float('note',
                            size=20,
                            help="Points the pupil"),
        'active': fields.boolean('Active'),
    }

    _defaults = {
    'active': True,
    }
```

### Now cretae the view of the module ```modu_test_view.xml```:


```xml
<?xml version="1.0" encoding="utf-8"?>
<openerp>
    <data>
        <record model="ir.ui.view" id="view_modu_test_form">
            
            <field name="name">modu_test_form</field>
            <field name="model">modu.test</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                
                <form string="modu test">
                    <sheet>
                        <group>
                            <field name="date" select="1"/>
                            <field name="name" select="1"/>
                            <field name="di" select="1"/>
                            <field name="note" select="1"/>
                            <field name="active" select="1"/>
                        </group>
                    </sheet>
                </form>
            
            </field>
        
        </record>
        
        <record model="ir.ui.view" id="modu_tree">

            <field name="name">modu_test_tree</field>
            <field name="model">modu.tree</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                
                <tree string="modu test">
                    <field name="date"/>
                    <field name="name"/>
                    <field name="Document Identification"/>
                    <field name="note"/>
                    <field name="active"/>
                </tree>

            </field>

        </record>
        
        <record model="ir.actions.act_window" id="action_modu_test">
            <field name="name">modu test</field>
            <field name="res_model">modu.test</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>
        
        <menuitem name="modu test" id="menu_modu_test"  action="action_modu_test" sequence="10"/>

        <menuitem name="sub menu" id="menu_modu_test_02" parent="menu_modu_test" action="action_modu_test" sequence="20"/>

    </data>

</openerp>
```

The ```record_form``` is the data of model with of inputs field

and the ```record_tree``` are the head titles

## Create the file ```__init__.py```:

```pyhton
# -*- coding: utf-8 -*-

import modu_test
```

and finnish of created the module

## Install the module

Now add the path the local_addons to the file ```/etc/odoo-server.conf```:

```python
addons_path = /opt/odoo/addons, path-of-local_addons
```

Restart all modules:

```bash
$ /opt/odoo/openerp-server -u all -d <name-database>
```

Install module for console:

```
$ /opt/odoo/openerp-server -d <name-database> -i <name-module>
```

and install for the web

in the browser ```your-ip:8069``` or ```localhost:8069``` search in the input and click at button of install

And finnish test your module

## Relation many2one

La relacion many2one recibe 2 parametros esenciales:

* 1: El objeto que queremos relacionar.
* 2: Y una etiqueta.

Nota: El name del campo many2one debe contener al final, el prefijo "_id" esto debido a acuerdos de la comunidad de odoo

Example:

```python
'country_id':   fields.many2one('scf.country', 
                'Name of state', 
                required=True),
```

## Relation many2many

La relacion many2many recibe 5 parametros esenciales:

* 1: El objeto que queremos relacionar.
* 2: Nombre de la nueva tabla que odoo creara.
* 3: El id del objeto a quien va relacionado.
* 4: El id del objeto a relacionar.
* 5: Una etiqueta.

Nota: El name del campo many2many debe contener al final, el prefijo "_ids" esto debido a acuerdos de la comunidad de odoo

Example:

```python
'cellphone_ids': fields.many2many('scf.cellphone', 
                            'scf.client_cellphone_rel',
                            'client_id',
                            'cellphone_id'),
```

## Relation one2many

La relacion one2many recibe 3 parametros esenciales:

* 1: El objeto que queremos relacionar.
* 2: El id del objeto a quien va relacionado.
* 3: Una etiqueta.

Nota: El name del campo one2many debe contener al final, el prefijo "_ids" esto debido a acuerdos de la comunidad de odoo

Example:

```python
'provider_ids': fields.one2many('scf.provider',
                            'client_id',
                            'Provider'),
```

Y agregar como many2one el id del objeto a quien va relacionado.
en tu tabla muchos.

Example:

```python
'client_id'     fields.many2one('scf.client',
                            'Client',
                            required=True),
```
## SOURCES

http://colibris.es/tutorial/como-instalar-odoo-8-para-debian/

http://juventudproductivabicentenaria.blogspot.com/2015/03/como-desarrollar-un-modulo-en-odoo-8-en.html

