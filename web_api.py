#coding=utf-8
from bottle import route, run, default_app, Bottle
from pyrack import RackConnect, RackObjects
from configparser import ConfigParser
import json

if __name__ != '__main__':
    from sys import path as syspath
    from os import path, chdir
    syspath.append(path.dirname(__file__))
    chdir(path.dirname(__file__))


rackdb = ConfigParser()
rackdb.readfp(open('rackdb.conf'))
db_host = rackdb.get('mysql', 'hostname')
db_user = rackdb.get('mysql', 'user')
db_pass = rackdb.get('mysql', 'password')
db_name = rackdb.get('mysql', 'dbname')
object_type_ids = json.loads(rackdb.get('racktables', 'object_type_ids'))

rackdoc = RackConnect(
    mysql_host=db_host,
    user=db_user,
    password=db_pass,
    database=db_name
)
rackobjects = RackObjects(rackdoc)
app = Bottle()


@route('/facts/:obj_id')
def fact(obj_id=None):
    obj_id = int(obj_id)
    return rackobjects.obj_attr(obj_id)

@route('/facts')
def facts():
    return rackobjects.list(object_type_ids)


@route('/name/:name')
def by_name(name=None):
    obj_id = int(rackobjects.get_id(from_type='name', value=name))
    return {'RackObj': rackobjects.obj_attr(obj_id)}


@route('/fqdn/:fqdn')
def by_fqdn(fqdn=None):
    obj_id = int(rackobjects.get_id(from_type='FQDN', value=fqdn))
    return rackobjects.obj_attr(obj_id)


@route('/withrole/:env/:role_id')
def with_role(role_id=None, env=None):
#    try:
        return rackobjects.with_role(role_id=role_id, environment=env)
#    except Exception as e:
#        return {"error": e.message}
#if __name__ == '__main__':
@route('/withtag/:tagString')
def with_tag(tagString):
    print (tagString)
    resp = rackobjects.with_tag(tagString)
    print (resp)
    return {'matches': resp}

run(host='127.0.0.1', port=8282)
#if __name__ != '__main__':
#    application = default_app()
