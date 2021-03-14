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

#/tareafinal/rangos/lista
def lista():
    'devuelve una lista con todos los rangos'
    rango=db(db.rango).select(db.rango.ALL)
    return dict(rango=rango)

#/tareafinal/rangos/lista_centro/01
def lista_centro():
    'devuelve una lista con todos los rangos de red de un centro dado'
    #hago la consulta a la base de datos para que me devuelva los consultorios 
    #capturo el argumento pasado
    centro_id_arg=request.args(0) or redirect(URL("lista"))
    #de la base de datos db, la tabla consultorio
    rangos = db.rango
    #la columna centro
    centro_id = rangos.centro
    #donde el valor de dicha columna sea igual al argumento 
    query = centro_id == centro_id_arg
    #defino la consulta
    conjunto = db(query)
    #la ejecuto
    rows = conjunto.select()

    #consulta del nombre del centro
    rows2=db(db.centro.id==centro_id_arg).select()
    centro_nombre=rows2[0].nombre

    return dict(rango=rows,centro_nombre=centro_nombre)
    

#/tareafinal/rangos/lista_consultorio/01
def lista_consultorio():
    'devuelve una lista con todos los rangos de red de un consultorio dado'
    #hago la consulta a la base de datos para que me devuelva los consultorios 
    #capturo el argumento pasado
    consultorio_id_arg=request.args(0) or redirect(URL("lista"))
    #de la base de datos db, la tabla consultorio
    rangos = db.rango
    #la columna centro
    consultorio_id = rangos.consultorio
    #donde el valor de dicha columna sea igual al argumento 
    query = consultorio_id == consultorio_id_arg
    #defino la consulta
    conjunto = db(query)
    #la ejecuto
    rows = conjunto.select()
    return dict(rango=rows)

#/tareafinal/rangos/nuevo
def nuevo():
    'crea un rango de red nuevo'
    form=SQLFORM(db.rango).process(next=URL("lista"))
    return dict(form=form)

#/tareafinal/rangosde/ver/01
def ver():
    'muestra la informacion de un rango de red'
    rango_id=request.args(0) or redirect(URL("lista"))
    rango=db.rango[rango_id]
    #centros=db(db.centro.id==centro_id).select()
    form=SQLFORM(db.rango,rango,readonly=True, showid=False)
    return dict(rango=rango,form=form)

#/tareafinal/rangos/editar/01
def editar():
    'modifica la informacion de un rango de red'
    rango_id=request.args(0,cast=int)
    rango=db.rango[rango_id]
    #centros=db(db.centro.id==centro_id).select()
    form=SQLFORM(db.rango,rango,readonly=False, showid=False).process(next=URL("lista"))
    return dict(form=form)


#/tareafinal/rangos/borrar/01
def borrar():
    'borra la informacion de un rango de red'
    centro_id=request.args(0) or redirect(URL("lista"))
    centro=db.centro[centro_id]
    db(db.centro.id == centro_id).delete()
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
