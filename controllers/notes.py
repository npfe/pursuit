# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import datetime


def overview():
    rows = db(db.notes.id > 0).select(db.notes.id, db.notes.title, db.notes.modified_on)
    return locals()

def new():
    note_id = db.notes.insert(
                    title='new-note',
                    body='',
                    parent=request.vars.parent,
                    created_on=datetime.datetime.now())
    redirect(URL('notes', 'editor', vars={'note_id': note_id}))


def editor():
    note_id = request.vars.note_id
    body = db.notes[note_id].body
    title = db.notes[note_id].title

    return locals()

def update():
    note_id = request.vars.note_id
    db(db.notes.id == note_id).update(body=request.vars['body'], modified_on=datetime.datetime.now())
    return 'ok'

def update_title():
    note_id = request.vars['note_id']
    new_title = request.vars['title']
    db(db.notes.id == note_id).update(title=new_title)

def preview():
    note_id = request.vars['note_id']
    return db.notes[note_id].body
