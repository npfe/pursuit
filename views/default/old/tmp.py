def index():
    data = list()
    entries = db(db.entry.parent == None).select()
    # entries with no parents - heads or non classified ones
    for item in entries:
        item_data = {'name': item.name, 'id': item.id, 'children':[]}
        data.append(item_data)

    # recursively gets children
    for i in range(0, len(data)):
        data[i]['children'] = children(data[i])

    # pretty print (comment out)
    print(json.dumps(data, indent=4, sort_keys=True))
    return dict(data=data)

def children(parent):
    children_list = list()
    db_children = db(db.entry.parent == parent['id']).select()
    if len(db_children) > 0:
        for db_child in db_children:
            child_data = {'name': db_child.name, 'id': db_child.id, 'children':{}}
            child_data['children'] = children(db_child)
            children_list.append(child_data)
    return children_list
