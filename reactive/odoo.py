import os
import os.path

from charmhelpers.core.hookenv import config, log, status_set
from charmhelpers.core.host import (
        service_available,
        service_pause,
        service_restart,
        service_resume,
)
from charmhelpers.core.templating import render
from charms.reactive import remove_state, set_state, when, when_not


@when('db.master.available')
def update_conf(psql):
    log('Running update_conf', 'DEBUG')
    conf = config()
    render(source='odoo.conf',
           target='/etc/odoo/openerp-server.conf',
           owner='odoo',
           perms=0o400,
           context={
               'db': psql.master,
               'conf': conf,
           })
    service_resume('odoo')
    service_restart('odoo')
    status_set('active', 'Ready')

@when('odoo.installed')
@when_not('db.master.available')
def blocked():
    log('Running blocked', 'DEBUG')
    status_set('blocked', 'Please link to a PostgreSQL service')

@when('db.connected')
def request_db(pgsql):
    log('Running request_db', 'DEBUG')
    conf = config()
    pgsql.set_database(conf['dbname'])

@when('apt.installed.odoo')
@when_not('odoo.installed')
def install_odoo():
    for path in ['/opt/odoo', '/opt/odoo/data', '/opt/odoo/addons']:
        if not os.path.exists(path):
            os.mkdir(path) #, mode=0755)
    render(source='odoo.unit',
           target='/etc/systemd/system/odoo.service',
           context={
                'conf': config(),
           })
    service_pause('odoo')
    set_state('odoo.installed')
