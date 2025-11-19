{
    'name': 'Skylimit Automatic Event Product Name',
    'version': '18.0.1.0.0',
    'category': 'Event',
    'summary': 'Automatically use product name as ticket name in events',
    'description': """
        Skylimit Automatic Event Product Name
        ======================================

        This module automatically sets the ticket name to match the product name
        when adding ticket lines to events and event templates. This eliminates
        the need to manually enter the same information twice and ensures
        consistency between product and ticket names.

        Features:
        ---------
        * Automatically populate ticket name from product name
        * Supports product variants - ticket name includes variant attributes
        * Works when creating new event tickets
        * Works when creating new event template tickets
        * Maintains data consistency between products and tickets
        * Follows Odoo best practices for model extension
    """,
    'author': 'iSensio',
    'website': 'https://isensio.com',
    'depends': [
        'base',
        'event',
        'event_product',
        'product',
    ],
    'data': [
        # No views needed for this functionality
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}