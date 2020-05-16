status = [1, 2, 3, 4, 5, 6, 7]

db.define_table('entry',
                Field('name'),
                Field('parent', 'integer', requires=IS_EMPTY_OR (IS_IN_DB(db, 'entry.id', '%(name)s'))),
                Field('status', 'integer', requires=IS_IN_SET(status), default=1))

db.define_table('journal',
                Field('parent', 'integer', requires=IS_IN_DB(db, db.entry.id)),
                Field('body', 'text'),
                Field('created_on', 'datetime', default=request.now, requires=IS_NOT_EMPTY()))

db.define_table('notes',
                Field('parent', 'integer', requires=IS_IN_DB(db, db.entry.id)),
                Field('body', 'text'),
                Field('created_on', 'datetime', default=request.now, requires=IS_NOT_EMPTY()),
                Field('modified_on', 'datetime'),
                Field('title', 'string'))
