# -*- coding: utf-8 -*-


# Creación, consulta, edición y borrado de todas las tablas
# Todas las acciones serán estarán disponibles únicamente para los usuarios del servicio de informática
# Búsqueda de centros por codigo_cias, codigo_gap, nombre, teléfonos
# Búsqueda de consultorios por codigo_cias, codigo_gap, nombre, teléfonos
# Busqueda de rangos por nombre y descripción
# Búsqueda de ip
# Búsqueda de ips libres de un centro/consultorio
# Búsqueda de puestos por ip, nombre, teléfono, profesional

#centro1
# centro2
# centro3

#/tareafinal/default/lista
def lista():
    'devuelve una lista con todos los centros'
    centro=db(db.centro).select(db.centro.ALL)
    return dict(centro=centro)
    

#/tareafinal/default/nuevo
def nuevo():
    'crea un centro nuevo'
    form=SQLFORM(db.centro).process(next=URL("lista"))
    return dict(form=form)

#/tareafinal/default/nuevo/01
def vista():
    'muestra la informacion de un centro'
    centro_id=request.args(0) or redirect(URL("lista"))
    centro=db.centro[centro_id]
    #centros=db(db.centro.id==centro_id).select()
    form=SQLFORM(db.centro,centro,readonly=True, showid=False)
    return dict(centro=centro,form=form)

def editar():
    'modifica la informacion de un centro'
    centro_id=request.args(0,cast=int)
    centro=db.centro[centro_id]
    #centros=db(db.centro.id==centro_id).select()
    form=SQLFORM(db.centro,centro,readonly=False, showid=False).process(next=URL("lista"))
    return dict(form=form)


#/tareafinal/default/nuevo/01
def borrar():
    'borra la informacion de un centro'
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
