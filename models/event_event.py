# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EventTypeTicket(models.Model):
    """
    Extend the event.type.ticket model (event template tickets) to automatically
    set ticket name from product name when a product is selected.
    """
    _inherit = 'event.type.ticket'

    @api.onchange('product_id')
    def _onchange_product_id_set_name(self):
        """
        Automatically set the ticket name to match the product name
        when a product is selected in event templates.
        Uses display_name to include variant attributes if applicable.
        """
        if self.product_id and self.product_id.display_name:
            self.name = self.product_id.display_name

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to ensure product name is used as ticket name
        when creating new template tickets if name is not explicitly provided.
        Uses display_name to include variant attributes if applicable.
        """
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('name'):
                product = self.env['product.product'].browse(vals['product_id'])
                if product and product.display_name:
                    vals['name'] = product.display_name

        return super(EventTypeTicket, self).create(vals_list)

    def write(self, vals):
        """
        Override write method to automatically update ticket name when
        product is changed in templates, unless name is explicitly provided.
        Uses display_name to include variant attributes if applicable.
        """
        if 'product_id' in vals and 'name' not in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            if product and product.display_name:
                vals['name'] = product.display_name

        return super(EventTypeTicket, self).write(vals)


class EventEventTicket(models.Model):
    """
    Extend the event.event.ticket model to automatically set ticket name
    from product name when a product is selected.
    """
    _inherit = 'event.event.ticket'

    @api.onchange('product_id')
    def _onchange_product_id_set_name(self):
        """
        Automatically set the ticket name to match the product name
        when a product is selected.

        This method is triggered when the product_id field changes,
        ensuring that the ticket name stays synchronized with the
        product name without requiring manual input.
        Uses display_name to include variant attributes if applicable.
        """
        if self.product_id and self.product_id.display_name:
            self.name = self.product_id.display_name

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to ensure product name is used as ticket name
        when creating new tickets if name is not explicitly provided.
        Uses display_name to include variant attributes if applicable.
        """
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('name'):
                product = self.env['product.product'].browse(vals['product_id'])
                if product and product.display_name:
                    vals['name'] = product.display_name

        return super(EventEventTicket, self).create(vals_list)

    def write(self, vals):
        """
        Override write method to automatically update ticket name when
        product is changed, unless name is explicitly provided in the update.
        Uses display_name to include variant attributes if applicable.
        """
        if 'product_id' in vals and 'name' not in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            if product and product.display_name:
                vals['name'] = product.display_name

        return super(EventEventTicket, self).write(vals)