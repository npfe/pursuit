# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import json
from datetime import datetime
from pprint import pprint

status = {1:'not_started', 2:'hold', 3:'track', 4:'done'}

# ---- example index page ----
def index():
    level = 1
    archive = list()
    # top entries selection
    entries_list = db(db.entry.parent == None).select().as_list()
    for entry in entries_list:
        # sets the level of the top entry
        entry['level'] = 0
        #  adds the qty of children
        entry['children'] = db(db.entry.parent == entry['id']).count()
        # adds the quantity of each subitems category for progress bar
        entry['not_started'], entry['hold'], entry['track'], entry['done'], entry['sum_w'] = get_w_progress(entry['name'], entry)
    # creates entry list containing ids of each entry
    entries_id = [entry['id'] for entry in entries_list]
    next_id = list()            # placeholder for ids to be pushed into the loop
    # recursively populates the list
    for i, id in enumerate(entries_id):
        children = db(db.entry.parent == id).select().as_list()
        for child in children:
            # finds index in entries_list where to insert the children
            index = next((index for (index, d) in enumerate(entries_list) if d['id']==child['parent']), None)
            # position index to 1 after position of the parent
            index+=1
            # append id of current child in the loop
            next_id.append(child['id'])
            # sets the entry
            child['level'] = level
            child['children'] = db(db.entry.parent == child['id']).count()
            log = db(db.journal.parent == child['id']).select().last()
            child['log'] = log.body[:75]+'...' if log != None else ''
            if log != None:
                last = get_status(log.created_on)
                child['last'] = last
            # skips items that are done or insert them in the final structure
            if child['status'] != 4:
                entries_list.insert(index,child)
            else:
                archive.append(child)
        if i == len(entries_id)-1:
            for item in next_id:
                entries_id.append(item)
            next_id = []
            level+=1

    pprint(archive)

    return dict(data=entries_list, status=status, archive=archive)

def get_w_progress(name, id):
    # entry status count dictionnary
    entry_status = {1:0, 2:0, 3:0, 4:0}
    entries_list = [id]
    entries_id = [id['id']]
    next_id = list()
    level=1
    # recursively populates the list
    for i, id in enumerate(entries_id):
        children = db(db.entry.parent == id).select().as_list()
        for child in children:
            # finds index in entries_list where to insert the children
            index = next((index for (index, d) in enumerate(entries_list) if d['id']==child['parent']), None)
            # position index to 1 after position of the parent
            index = index+1 if index!=None else index
            next_id.append(child['id'])
            # counts tasks status
            entry_status[child['status']]+=1
        if i == len(entries_id)-1:
            for item in next_id:
                entries_id.append(item)
            next_id = []
            level+=1
    total = sum(entry_status.values())
    return entry_status[1], entry_status[2], entry_status[3], entry_status[4], total

def get_status(status):
    wrapper_class = 'badge badge-pill '
    class_type = {2:'badge-success', 3:'badge-warning', 5:'badge-danger'}
    # creates a list of the class_type dict keys
    list_type = list(class_type.keys())
    # finds out the duration since last log was entered
    now = datetime.now()
    delta = (now-status).days
    if delta < 1:
        delta = int((now-status).seconds/3600)
        value = '%s hour%s' % (str(delta), 's' if delta>1 else '')
        wrapper_class = wrapper_class+class_type[list_type[0]]
    else:
        value = '%s day%s' % (str(delta), 's' if delta>1 else '')
        if delta > list_type[2]:
            wrapper_class = wrapper_class+class_type[list_type[2]]
        elif delta >= list_type[1]:
            wrapper_class = wrapper_class+class_type[list_type[1]]
        else:
            wrapper_class = wrapper_class+class_type[list_type[0]]
    # creates the span html to be displayed
    delta = SPAN(value, _class=wrapper_class)
    return delta


def children(parent):
    children_list = list()
    db_children = db(db.entry.parent == parent['id']).select()
    if len(db_children) > 0:
        for db_child in db_children:
            child_data = {'name': db_child.name, 'id': db_child.id, 'children':{}}
            child_data['children'] = children(db_child)
            children_list.append(child_data)
    return children_list

def children_list(parent):
    c_list = list()
    children = db(db.entry.parent == parent).select()
    for child in children:
        c_count = db(db.entry.parent == child.id).count()
        c_list.append({'name': child.name, 'id': child.id, 'children': c_count})
    return c_list

def item():
    item = request.args(0)
    status = {1:'not_started', 2:'hold', 3:'track', 4:'done'}
    record = db.entry[item]
    return locals()

def new_item():
    parent = request.args(0)
    db.entry.parent.default = parent
    form = SQLFORM(db.entry)
    if form.process(session=None, formname='_newitem').accepted:
        response.js =  "location.reload();"
        response.flash=('Log inserted')

    return locals()

def edit_item():
    entry = request.args(0)
    redirection = request.args(1).replace('_', '/')
    db.entry.id.readable = db.entry.id.writable = False
    db.entry.parent.readable = db.entry.parent.writable = False
    db.entry.status.readable = db.entry.status.writable = False
    form = SQLFORM(db.entry, entry)
    if form.process().accepted:
        print(URL(redirection))
        redirect(URL( redirection))
    return locals()

def delete_item():
    entry = request.args(0)
    form = FORM.confirm('Yes', {'Back':URL('index')})
    if form.accepted:
        print('deleted')
    return locals()

def set_status():
    record = request.args(0)
    status = request.args(1)
    db(db.entry.id == record).update(status=status)
    session.flash = '%s status updated' % (db.entry[record].name)
    redirect(URL('default', 'item', args=record))

def log_form():
    record = request.args(0)
    db.journal.parent.readable = db.journal.parent.writable = False
    db.journal.parent.default = record
    db.journal.created_on.default = request.now
    form = SQLFORM(db.journal)
    form.vars.created_on = request.now

    if form.process(session=None, formname='_newlog').accepted:
        response.js =  "jQuery('#%s').get(0).reload()" % request.vars.reload_div
        response.flash=('Log inserted')
    return locals()

def log_journal():
    record = request.args(0)
    logs = db(db.journal.parent == record).select(orderby=~db.journal.id)
    return dict(logs=logs)

def log_delete():
    record = request.args(0)
    db(db.journal.id == record).delete()
    response.js = "jQuery('#%s').get(0).reload()" % request.args(1)
    response.flash=('Log deleted')

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
