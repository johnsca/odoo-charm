Odoo charm
==========

# Overview

Odoo is a comprehensive open source management system. It has a large, active
community, which has developed modules to handle all facets of company
management.

These include, amongst others: Sales Management, CRM, e-commerce,
Manufacturing, Stock, Accounting, Human Resources, Project Management,
Logistics, Productivity and Document Management.

Odoo allows you to start easily with one module to fit a specific need then
add additional modules as and when you need them enabling you to have a
powerful feature rich Enterprise Resource Planner.

# Usage

To deploy and use this charm, you want to relate it to the db-admin PostgreSQL
endpoint:

juju deploy odoo
juju add-relation odoo postgresql:db-admin

The charm provides the http relation as well that you can point your other
frontends to, or you can expose the charm and point your browser at the unit.

Make sure you change the management password after you have created your
database.

# Configuration

If you want to install a different Odoo version, all you need to do is set
the `install_sources` configuration parameter to point to a different repository
and possibly also change `install_keys` to set the relevant signing key as well.

## Known Limitations and Issues

This charm does not support scale-out yet.

# Contact Information

## Authors
  - Ondřej Kuzník <ondrej.kuznik@credativ.co.uk>

## Odoo

  - Website: https://odoo.com
  - Bug tracker: https://github.com/odoo/issues
  - Community mailing lists: https://www.odoo.com/groups

## credativ

  - Website: https://credativ.co.uk
  - Contact email: info@credativ.co.uk
