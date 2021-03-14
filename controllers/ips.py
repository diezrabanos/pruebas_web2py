# -*- coding: utf-8 -*-


# Creación, consulta, edición y borrado de todas las tablas
# Todas las acciones serán estarán disponibles únicamente para los usuarios del servicio de informática
# Búsqueda de centros por codigo_cias, codigo_gap, nombre, teléfonos
# Búsqueda de consultorios por codigo_cias, codigo_gap, nombre, teléfonos
# Busqueda de rangos por nombre y descripción
# Búsqueda de ip
# Búsqueda de ips libres de un centro/consultorio
# Búsqueda de puestos por ip, nombre, teléfono, profesional

#celtro1
# centro2
# centro3

#/tareafinal/ips/lista
def lista():
    'devuelve una lista con todas las ips'
    ip=db(db.ip).select(db.ip.ALL)
    return dict(ip=ip)

#/tareafinal/puestos/lista_centro/01
def lista_centro():
    'devuelve una lista con todos los puestos de un centro dado'
    #tengo que hacer el filtro aqui por centro
    #hago la consulta a la base de datos para que me devuelva los consultorios 
    #capturo el argumento pasado
    centro_id_arg=request.args(0) or redirect(URL("lista"))
    #de la base de datos db, la tabla consultorio
    puestos = db.puesto
    #la columna centro
    centro_id = puestos.centro
    #donde el valor de dicha columna sea igual al argumento 
    query = centro_id == centro_id_arg
    #defino la consulta
    conjunto = db(query)
    #la ejecuto
    rows = conjunto.select()
    return dict(puesto=rows)

#/tareafinal/puestos/lista_consulorio/01
def lista_consultorio():
    'devuelve una lista con todos los puestos de un consultorio dado'
    #tengo que hacer el filtro aqui por centro
    #hago la consulta a la base de datos para que me devuelva los consultorios 
    #capturo el argumento pasado
    consultorio_id_arg=request.args(0) or redirect(URL("lista"))
    #de la base de datos db, la tabla consultorio
    puestos = db.puesto
    #la columna centro
    consultorio_id = puestos.consultorio
    #donde el valor de dicha columna sea igual al argumento 
    query = consultorio_id == consultorio_id_arg
    #defino la consulta
    conjunto = db(query)
    #la ejecuto
    rows = conjunto.select()
    return dict(puesto=rows)

#/tareafinal/puestos/lista_rango/01
def lista_rango():
    'devuelve una lista con todos los puestos de un rango dado'
    #tengo que hacer el filtro aqui por centro
    #hago la consulta a la base de datos para que me devuelva los consultorios 
    #capturo el argumento pasado
    rango_id_arg=request.args(0) or redirect(URL("lista"))
    #de la base de datos db, la tabla consultorio
    puestos = db.puesto
    #la columna centro
    rango_id = puestos.rango
    #donde el valor de dicha columna sea igual al argumento 
    query = rango_id == rango_id_arg
    #defino la consulta
    conjunto = db(query)
    #la ejecuto
    rows = conjunto.select()
    return dict(puesto=rows)


#/tareafinal/ip/nuevo
def nuevo():
    'crea una ip nueva'
    form=SQLFORM(db.ip).process(next=URL("lista"))
    return dict(form=form)

#/tareafinal/ip/ver/01
def ver():
    'muestra la informacion de una ip'
    ip_id=request.args(0) or redirect(URL("lista"))
    ip=db.ip[ip_id]
    #centros=db(db.centro.id==centro_id).select()
    form=SQLFORM(db.ip,ip,readonly=True, showid=False)
    return dict(ip=ip,form=form)

#/tareafinal/ip/editar/01
def editar():
    'modifica la informacion de una ip'
    ip_id=request.args(0,cast=int)
    ip=db.ip[ip_id]
    #centros=db(db.centro.id==centro_id).select()
    form=SQLFORM(db.ip,ip,readonly=False, showid=False).process(next=URL("lista"))
    return dict(form=form)


#/tareafinal/ip/borrar/01
def borrar():
    'borra la informacion de una ip'
    ip_id=request.args(0) or redirect(URL("lista"))
    ip=db.ip[ip_id]
    db(db.ip.id == ip_id).delete()
    redirect(URL("lista"))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
