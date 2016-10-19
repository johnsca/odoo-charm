import os
import os.path
import shutil

from charmhelpers.core.hookenv import config, log, open_port, status_set
from charmhelpers.core.host import (
        service_available,
        service_pause,
        service_restart,
        service_resume,
        service_running,
)
from charmhelpers.core.templating import render
from charms.reactive import (
        hook,
        remove_state,
        set_state,
        when,
        when_not,
)

from charms.layer.nginx import configure_site


@when('apt.installed.odoo')
@when_not('odoo.installed')
def install_odoo():
    for path in ['/opt/odoo', '/opt/odoo/data', '/opt/odoo/addons']:
        if not os.path.exists(path):
            os.mkdir(path, mode=0o755)
            shutil.chown(path, 'odoo')
    render(source='odoo.unit',
           target='/etc/systemd/system/odoo.service',
           context={
                'conf': config(),
           })
    service_pause('odoo')
    set_state('odoo.installed')

@when('odoo.installed')
@when_not('db.master.available')
def blocked():
    status_set('blocked', 'Please link to a PostgreSQL service')

@when('db.connected')
def request_db(pgsql):
    pgsql.set_database(config('dbname'))

@when('odoo.installed', 'db.master.available')
@when_not('odoo.configured')
def update_conf(psql):
    render(source='odoo.conf',
           target='/etc/odoo/openerp-server.conf',
           owner='odoo',
           perms=0o400,
           context={
               'db': psql.master,
               'conf': config(),
           })
    service_resume('odoo')
    service_restart('odoo')
    set_state('odoo.configured')

@when('nginx.available', 'odoo.configured')
@when_not('odoo.ready')
def configure_webapp():
    log('Exposing Odoo on port %d' % config('port'), 'DEBUG')
    configure_site('odoo', 'odoo-site.conf')
    open_port(config('port'))
    set_state('odoo.ready')

@when('website.available', 'odoo.ready')
@when_not('odoo.website.configured')
def configure_website(website):
    website.configure(port=config('port'))
    set_state('odoo.website.configured')

#@hook('update-status')
@when('odoo.ready')
def update_status():
    if service_running('odoo'):
        status_set('active', 'Odoo is running')
    else:
        status_set('blocked', 'Odoo has stopped')
