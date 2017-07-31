# Module to Manage and Control the all projects of the Cooperatives


# Requirements that the module must meet

* Registry of hours man.
* The load of deliverables and activities of first level and second.
* Calculation rules.
* Calculate percentages of progress.
* Audit module.


Create the struc basic of module with the generator of odoo:


```bash
$ /opt/odoo/odoo-bin scaffold <module name> <where to put it>

Real:

$ /opt/odoo/odoo-bin scaffold agili ~/p2-odoo/
```  

Ok the above created our skeleton, now create our model

 
## Model Project

Edit the file agili/models/```models.py``` and copy the following content:

```python
# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions

class Project(models.Model):

    _name = 'agili.project'

    name = fields.Char(string="Nombre del Proyecto", required=True)

    description = fields.Text(string="Descripción")

    start_date = fields.Date(string="Fecha de inicio", required=True)

    end_date = fields.Date(string="Fecha de Fin", required=True)

    hour_man = fields.Integer(string="Horas hombres")

    responsible_id = fields.Many2one('res.users',
    ondelete='set null', string="Responsable", index=True)

    porcen_project = fields.Float(string="Avance del proyecto")

    activity_ids = fields.One2many(
        'agili.activity', 'project_id', string="Actividades")

    activities_count = fields.Integer(string="Numero de actividades", 
        compute='_get_activities_count', store=True)

    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "El nombre del proyecto no puede ser la descripción."),

        ('name_unique',
        'UNIQUE(name)',
        "El nombre del proyecto es unico"),
    ]

    state = fields.Selection([
        ('process', "En proceso"),
        ('stopped', "Detenido"),
        ('done', "Terminado"),
    ], string="Estado", default='process')

    @api.multi
    def action_process(self):
        self.state = 'process'

    @api.multi
    def action_stopped(self):
        self.state = 'stopped'

    @api.multi
    def action_done(self):
        self.state = 'done'

    #Función para calcular cuantas acitvidades hay en proyecto
    @api.depends('activity_ids')
    def _get_activities_count(self):
        for r in self:
            r.activities_count = len(r.activity_ids)
```


## Model Activity

Edit the file agili/models/```models.py``` and copy the following content:

```python
class Activity(models.Model):

    _name = 'agili.activity'

    name = fields.Char(string="Nombre de Actividad", required=True)
    
    ac_start_date = fields.Date(string="Fecha de inicio", required=True)

    ac_end_date = fields.Date(string="Fecha de Fin", required=True)
   
    objetive = fields.Char(string="Objetivo", required=True)
    
    description = fields.Text(string="Descripción")

    result = fields.Text(string="Resultado")

    ac_hour_man = fields.Integer(string="Horas hombres")

    responsible_id = fields.Many2one('res.users',
    ondelete='set null', string="Responsable", index=True)

    project_id = fields.Many2one('agili.project',
        ondelete='cascade', string="Proyecto", required=True)

    ac_state = fields.Selection([
        ('process', "En proceso"),
        ('stopped', "Detenida"),
        ('done', "Terminada"),
    ], string="Estado", default='process')

    @api.multi
    def action_process(self):
        self.state = 'process'

    @api.multi
    def action_confirm(self):
        self.state = 'stopped'

    @api.multi
    def action_done(self):
        self.state = 'done'
```


We create the "Project" and "Activity" model with all its attributes

Now will created the view to this models

## View Project 

Create the file agili/views/```project.xml```

First add the data file that allows us to create and edit the activities of the Project model:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
  <data>

    <!-- Data file form 

    @ function: Crear y modificar registros 
    @ Descrip: Este data file define como sera el formulario, que datos seran registrados por el usuario etc
    -->
    <record model="ir.ui.view" id="project_form_view">

      <field name="name">project.form</field>
      <field name="model">agili.project</field>
      <field name="arch" type="xml">

        <form string="Project Form">
          <!-- State

            @Description: Añadimos la logica y funcionamiento para trabajar con el estado de un proyecto. Con los siguientes botones controlamos el estado.
          -->
          <header>

            <button name="action_process" type="object"
            string="En Proceso"
            states="stopped,done"/>
            <button name="action_stopped" type="object"
            string="Detenido" states="process,done"
            class="oe_highlight"/>
            <button name="action_done" type="object"
            string="Terminado" states="stopped,process"
            class="oe_highlight"/>

            <field name="state" widget="statusbar"/>

          </header>

          <sheet>
            <!-- Agrupamos los campos generales de un proyecto -->
            <group string="General">
              <field name="name"/>
              <field name="description"/>
              <field name="responsible_id"/>
            </group>

            <!-- Agrupamos los campos que generan la toma de decisiones-->
            <group string="Control">
              <field name="start_date"/>
              <field name="end_date"/>
              <field name="hour_man"/>
              <field name="porcen_project" widget="progressbar"/>
            </group>
        
            <!-- Notebook
              @Function: Crear un cuaderno, agrupar mejor la información.

              @Description: Este data file nos permite crear un cuaderno con paginas; donde cada page es una pestaña. 
            -->
            <notebook>
              <!-- Page Actividades 
  
                @Function: Añadir actividades a un proyecto

                @Description: Esta page del notebook nos permite añadir actividades al proyecto y mostramos una lista de ellos solo con los campos necesarios.
              -->
              <page string="Actividades">
                <field name="activity_ids">
                  <tree string="Añade una actividad al proyecto">
                    <field name="name"/>
                    <field name="objetive"/>
                    <field name="ac_hour_man"/>
                    <field name="responsible_id"/>
                  </tree>
                </field>
              </page>
            </notebook>

          </sheet>
        </form>

      </field>

    </record>
```

Ok Now adds the data file search that makes it possible to search for registered projects:

```xml
<!-- Record search 
      @Function: Para realizar la busqueda de los registros
      
      @Description: Con elrecord search definimos de que manera seran buscado los registros, definiendo por cuales campos se haran las busquedas, añadiendo domain entre otros.
    -->
    <record model="ir.ui.view" id="project_search_view">

      <field name="name">project.search</field>
      <field name="model">agili.project</field>

      <field name="arch" type="xml">
        <search>
          <field name="name"/>
          <field name="hour_man"/>
          <field name="description"/>

          <!-- Filter
          
            @Function: Añadir condiciones a las busuqedes

            @Description: En este caso añadimos un filter para que solo sean mostrados los proyectos del usuario logueado.
          -->
          <filter name="my_activities" 
                  string="Mis proyectos"
                  domain="[('responsible_id', '=', uid)]"/>

          <!-- Invocamos al filter creado anteriormente -->
          <group string="Group By">
            <filter name="by_responsible" 
                    string="Responsable" 
                  context="{'group_by': 'responsible_id'}"
            />
          </group>
        </search>

      </field>

    </record>
```

Now add the data file <tree> that which shows the list of registered elements:

```xml
    <!-- Record tree

      @Function: Listar la información en una tabla

      @Description: Record para mostrar la información en una tabla, donde cada field es una columna.
    -->
    <record model="ir.ui.view" id="project_tree_view">
      <field name="name">project.tree</field>
      <field name="model">agili.project</field>

      <field name="arch" type="xml">
        <tree string="Project Tree">
          <field name="name"/>
          <field name="start_date"/>
          <field name="end_date"/>
          <field name="responsible_id"/>
          <field name="hour_man"/>
          <field name="porcen_project" widget="progressbar"/>
        </tree>
      </field>

    </record>
```

Now add the data file calendar, This to have a better vision of the projects:

```xml
<!-- Record Calendar

       @Function: Mostrar mediante un calendario las fechas de inicio y fin de los proyectos
    -->
    <record model="ir.ui.view" id="project_calendar_view">
      <field name="name">project.calendar</field>
      <field name="model">agili.project</field>
      <field name="arch" type="xml">
        
        <calendar string="project Calendar" 
                  date_start="start_date" 
                  date_stop="end_date"
                  color="responsible_id">

          <field name="name"/>

        </calendar>

      </field>
    </record>
```

Now add the record graph, This to make comparisons through graphs of the projects:

```xml
<!-- Record graph

      @Function: Generar graficos (torta, barras..)

      @Description: Grafica comparativas de cuantas actividades tiene un proyecto con respecto a otro.
    -->
    <record model="ir.ui.view" id="project_graph_view">
      <field name="name">project.graph</field>
      <field name="model">agili.project</field>
      <field name="arch" type="xml">
        
        <graph string="Actividades de un proyecto">
          <field name="activity_ids
            "/>
          <field name="activities_count" type="measure"/>
        </graph>

      </field>

    </record>
```

Now add the data file ir.actions.act_window that is the element that links the tree and form, also the order of showing them, if first the tree or the form:


```xml
      <!-- Tag actions.act_window 
      
        @Function: Este tag o record tiene como funcion contralar el flujo de los views a las acciones de los mismos

        @Descripcion: Una de las cosa que ahce este record es definir el modo en que las vistas seran mostradas, en este caso sera primero el <tree>, <form>, <calendar> ,y de ultimo las graficas <graph>.
      -->
      <record model="ir.actions.act_window" id="project_list_action">

        <field name="name">Proyectos</field>
        <field name="res_model">agili.project</field>
        <field name="view_type">form</field>
        <field name="view_mode">tree,form,calendar,graph</field>
        <field name="context" eval="{'search_default_my_activities': 1}"/>

      </record>
```

## Menus 

Ok now we have to add the menus that link to your module

First add the top menu:

```xml
      <!-- Añadimos el menu de la barra top -->
      <menuitem id="main_agili_menu" name="Gestion de Cooperativas"/>
```

Add the left side parent menu:

```xml
      <!-- Añadimos el menu del panel izquierdo -->
      <menuitem id="agili_menu" 
                name="Gestion de Cooperativas"
                parent="main_agili_menu"/>
```

And to finish with the view, we add the submenu that takes us to the actions of our module:

```xml
      <!-- Añadimos un submenu al menu anterior creado, el cual nos lleva a las views de nuestro modelo -->
      <menuitem id="project_menu" name="Proyecto" 
            parent="agili_menu"
            action="project_list_action"/>
 </data>
</odoo>

```

## View Activity

Create the file agili/views/```activity.xml``` with the following content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
  <data>

    <!-- Data file form 

    @ function: Crear y modificar registros 
    @ Descrip: Este data file define como sera el formulario, que datos seran registrados por el usuario etc
    -->
    <record model="ir.ui.view" id="activity_form_view">

      <field name="name">activity.form</field>
      <field name="model">agili.activity</field>
      <field name="arch" type="xml">

        <form string="activity Form">
          <!-- State

            @Description: Añadimos la logica y funcionamiento para trabajar con el estado de una actividad. Con los siguientes botones controlamos el estado.
          -->
          <header>

            <button name="action_process" type="object"
            string="En Proceso"
            states="stopped,done"/>
            <button name="action_stopped" type="object"
            string="Detenida" states="process,done"
            class="oe_highlight"/>
            <button name="action_done" type="object"
            string="Terminada" states="stopped,process"
            class="oe_highlight"/>

            <field name="ac_state" widget="statusbar"/>

          </header>

          <sheet>
            <!-- Agrupamos los campos generales de una actividad -->
            <group string="General">
              <field name="name"/>
              <field name="objetive"/>
              <field name="description"/>
              <field name="ac_responsible_id"/>
            </group>

            <!-- Agrupamos los campos que generan la toma de decisiones-->
            <group string="Control">
              <field name="project_id"/>
              <field name="ac_start_date"/>
              <field name="ac_end_date"/>
              <field name="ac_hour_man"/>
              <field name="result"/>
            </group>

          </sheet>
        </form>

      </field>

    </record>


    <!-- Record search 
      @Function: Para realizar la busqueda de los registros
      
      @Description: Con el record search definimos de que manera seran buscado los registros, definiendo por cuales campos se haran las busquedas, añadiendo domain, entre otros.
    -->
    <record model="ir.ui.view" id="activity_search_view">

      <field name="name">activity.search</field>
      <field name="model">agili.activity</field>

      <field name="arch" type="xml">
        <search>
          <field name="name"/>
          <field name="hour_man"/>
          <field name="description"/>
          <field name="ac_state"/>

          <!-- Filter
          
            @Function: Añadir condiciones a las busuqedes

            @Description: En este caso añadimos un filter para que solo sean mostrados las actividades del usuario logueado.
          -->
          <filter name="my_activities" 
                  string="Mis Actividades"
                  domain="[('ac_responsible_id', '=', uid)]"/>

          <!-- Invocamos al filter creado anteriormente -->
          <group string="Group By">
            <filter name="by_responsible" 
                    string="Responsable" 
                  context="{'group_by': 'ac_responsible_id'}"
            />
          </group>
        </search>

      </field>

    </record>

    <!-- Record tree

      @Function: Listar la información en una tabla

      @Description: Record para mostrar la información en una tabla, donde cada field es una columna.
    -->
    <record model="ir.ui.view" id="activity_tree_view">
      <field name="name">activity.tree</field>
      <field name="model">agili.activity</field>

      <field name="arch" type="xml">
        <tree string="activity Tree">
          <field name="project_id"/>
          <field name="name"/>
          <field name="ac_start_date"/>
          <field name="ac_end_date"/>
          <field name="ac_responsible_id"/>
          <field name="ac_hour_man"/>
        </tree>
      </field>

    </record>

    <!-- Record Calendar

       @Function: Mostrar mediante un calendario las fechas de inicio y fin de los proyectos
    -->
    <record model="ir.ui.view" id="activity_calendar_view">
      <field name="name">activity.calendar</field>
      <field name="model">agili.activity</field>
      <field name="arch" type="xml">
        
        <calendar string="activity Calendar" 
                  date_start="start_date" 
                  date_stop="end_date"
                  color="ac_responsible_id">

          <field name="name"/>

        </calendar>

      </field>
    </record>

      <!-- Tag actions.act_window 
      
        @Function: Este tag o record tiene como funcion contralar el flujo de los views a las acciones de los mismos

        @Descripcion: Una de las cosa que ahce este record es definir el modo en que las vistas seran mostradas, en este caso sera primero el <tree>, <form>, <calendar> ,y de ultimo las graficas <graph>.
      -->
      <record model="ir.actions.act_window" id="activity_list_action">

        <field name="name">Actividades</field>
        <field name="res_model">agili.activity</field>
        <field name="view_type">form</field>
        <field name="view_mode">tree,form,calendar</field>
        <field name="context" eval="{'search_default_my_activities': 1}"/>

      </record>

      
      <!-- Añadimos un submenu al menu de gestion de proyectos -->
      <menuitem id="activity_menu" name="Actividad" 
            parent="agili_menu"
            action="activity_list_action"/>

  </data>
</odoo>
```

Add the view project and activity to file agili/__manifest__.py:

```python
  'data': [
        # 'security/ir.model.access.csv',
        'views/project.xml',
        'views/activity.xml',
    ],
```



