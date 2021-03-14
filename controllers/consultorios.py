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

#/tareafinal/consultorios/lista
def lista():
    'devuelve una lista con todos los consultorios'
    consultorio=db(db.consultorio).select(db.consultorio.ALL)
    return dict(consultorio=consultorio)

#/tareafinal/consultorios/lista_centro/01
def lista_centro():
    'devuelve una lista con todos los consultorios de un centro dado'
    #capturo el argumento pasado
    centro_id_arg=request.args(0) or redirect(URL("lista"))
    #hago la consulta a la base de datos para que me devuelva los consultorios 
    #de la base de datos db, la tabla consultorio
    consultorios = db.consultorio
    centros=db.centro
    #la columna centro
    centro_id = consultorios.centro
    #donde el valor de dicha columna sea igual al argumento 
    query = centro_id == centro_id_arg
    #defino la consulta
    conjunto = db(query)
    #la ejecuto
    rows = conjunto.select()
    #consulta del nombre del centro
    rows2=db(db.centro.id==centro_id_arg).select()
    centro_nombre=rows2[0].nombre
      

    return dict(consultorio=rows,centro_nombre=centro_nombre)

#/tareafinal/consultorio/nuevo
def nuevo():
    'crea un consultorio nuevo'
    form=SQLFORM(db.consultorio).process(next=URL("lista"))
    return dict(form=form)

#/tareafinal/consultorio/ver/01
def ver():
    'muestra la informacion de un consultorio'
    consultorio_id=request.args(0) or redirect(URL("lista"))
    consultorio=db.consultorio[consultorio_id]
    #centros=db(db.centro.id==centro_id).select()
    form=SQLFORM(db.consultorio,consultorio,readonly=True, showid=False)
    return dict(consultorio=consultorio,form=form)

#/tareafinal/consultorio/editar/01
def editar():
    'modifica la informacion de un consultorio'
    consultorio_id=request.args(0,cast=int)
    consultorio=db.consultorio[consultorio_id]
    form=SQLFORM(db.consultorio,consultorio,readonly=False, showid=False).process(next=URL('ver',args=consultorio.id))
    return dict(form=form)


#/tareafinal/consultorio/borrar/01
def borrar():
    'borra la informacion de un consultorio'
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
