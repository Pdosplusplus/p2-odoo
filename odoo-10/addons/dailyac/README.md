# Module to Manage a Control dialy of the Activities


Create the struc basic of module with the generator of odoo:


```bash
$ /opt/odoo/odoo-bin scaffold <module name> <where to put it>

Real:

$ /opt/odoo/odoo-bin scaffold dailyac ~/p2-odoo/
```  

Ok the above created our skeleton, now create our model

 
## Model Activity

Edit the file dailyac/models/````models.py``` and copy the following content:

```python
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Activity(models.Model):

    _name = 'dailyac.activity'

    day = fields.Date(string="Día", required=True)

    name = fields.Char(string="Nombre de Actividad", required=True)

    objetive = fields.Char(string="Objetivo", required=True)
    
    description = fields.Text(string="Descripción")

    result = fields.Text(string="Resultado")

    who_summon = fields.Many2one('res.partner',
    ondelete='set null', string="Quién generó la convocatoria ?", index=True)

    responsible_id = fields.Many2one('res.users',
    ondelete='set null', string="Responsable", index=True)
```

We create the "Activity" model with all its attributes

Now will created the view to this model

## Data files

Create the file dailyac/views/```activity.xml```


First add the data file that allows us to create and edit the activities of the activity model:

```xml
<odoo>
    <data>
      <!-- Data file para crear y modificar registros -->
      <record model="ir.ui.view" id="activity_form_view">
        
        <field name="name">activity.form</field>
        <field name="model">dailyac.activity</field>
        
        <field name="arch" type="xml">
     
          <form string="Activity Form">
            <sheet>

              <group>
                <field name="day"/>
                <field name="name"/>
                <field name="objetive"/>
                <field name="result"/>
                <field name="who_summon"/>
                <field name="responsible_id"/>
              </group>

			  <!--Este data file nos permite crear
			      un cuaderno con pestañas, cada page
			      es una pestaña -->
              <notebook>
                
                <page string="Descripción">
                  <field name="description"/>
                </page>

                <page string="About">
                  This is an example of notebooks
                  Este es un ejemplo de cuadernos
                </page>

              </notebook>


            </sheet>
          </form>

        </field>
      
      </record>
``` 


Ok Now adds the data file ```search``` that makes it possible to search for registered activities:

```xml
	<!-- Record searh 
	  @ Para realizar la busqueda de los registros
	  @ Definimos por que campos se haran las busquedas
	-->
	<record model="ir.ui.view" id="activity_search_view">

	<field name="name">activity.search</field>
	<field name="model">dailyac.activity</field>

	<field name="arch" type="xml">
	    <search>
	        <field name="name"/>
	        <field name="description"/>
	    </search>
	</field>

	</record>
```

Where each ```<field/>``` is the element by which it will filter the date


Now add the data file ```<tree>```that which shows the list of registered elements:


```xml
	  <record model="ir.ui.view" id="activity_tree_view">
          <field name="name">activity.tree</field>
          <field name="model">dailyac.activity</field>
          <field name="arch" type="xml">
              <tree string="Actividad Tree">
                <field name="day"/>
                <field name="name"/>
                <field name="objetive"/>
                <field name="description"/>
                <field name="result"/>
                <field name="who_summon"/>
                <field name="responsible_id"/>
              </tree>
          </field>
      </record>
```


Now add the data file ```ir.actions.act_window``` that is the element that links the tree and form, also the order of showing them, if first the tree or the form:

```xml
  <record model="ir.actions.act_window" id="activity_list_action">
      
      <field name="name">Actividades</field>
      <field name="res_model">dailyac.activity</field>
      <field name="view_type">form</field>
      <field name="view_mode">tree,form</field>
      <field name="help" type="html">
          <p class="oe_view_nocontent_create">Registra la primera actividad
          </p>
      </field>

  </record>
```

Ok now we have to add the menus that link to your module

First add the top menu:

```xml
	<!-- top level menu: no parent -->
      <menuitem id="main_dailyac_menu" name="Actividad"/>
```


Add the left side parent menu:

```xml
	  <!-- A first level in the left side menu is needed
           before using action= attribute -->
      <menuitem id="dailyac_menu" name="Actividades Diarias"
                parent="main_dailyac_menu"/>
```

And to finish we add the submenu that takes us to the actions of our module

```xml
		<menuitem id="activity_menu" name="Actividad" 
            parent="dailyac_menu"
            action="activity_list_action"/>
    </data>
</odoo>
```

Add the view activity to dailyac/```__manifest__.py```:

```
	'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/activity.xml'
    ],
```

