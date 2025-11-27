# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EventTypeTicket(models.Model):
    """
    Extend the event.type.ticket model (event template tickets) to automatically
    set ticket name from product name when a product is selected.
    """
    _inherit = 'event.type.ticket'

    def _get_product_ticket_name(self, product):
        """
        Get the appropriate ticket name from a product.
        For variants: use the attribute values (e.g., "Blue, Large")
        For regular products: use the product name
        """
        if not product:
            return False
        # Check if product is a variant (has attribute values)
        if product.product_template_attribute_value_ids:
            return ', '.join(product.product_template_attribute_value_ids.mapped('name'))
        return product.name

    @api.onchange('product_id')
    def _onchange_product_id_set_name(self):
        """
        Automatically set the ticket name to match the product name
        when a product is selected in event templates.
        For variants, uses the attribute values only.
        """
        if self.product_id:
            self.name = self._get_product_ticket_name(self.product_id)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to ensure product name is used as ticket name
        when creating new template tickets if name is not explicitly provided.
        """
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('name'):
                product = self.env['product.product'].browse(vals['product_id'])
                name = self._get_product_ticket_name(product)
                if name:
                    vals['name'] = name

        return super(EventTypeTicket, self).create(vals_list)

    def write(self, vals):
        """
        Override write method to automatically update ticket name when
        product is changed in templates, unless name is explicitly provided.
        """
        if 'product_id' in vals and 'name' not in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            name = self._get_product_ticket_name(product)
            if name:
                vals['name'] = name

        return super(EventTypeTicket, self).write(vals)


class EventEventTicket(models.Model):
    """
    Extend the event.event.ticket model to automatically set ticket name
    from product name when a product is selected.
    """
    _inherit = 'event.event.ticket'

    def _get_product_ticket_name(self, product):
        """
        Get the appropriate ticket name from a product.
        For variants: use the attribute values (e.g., "Blue, Large")
        For regular products: use the product name
        """
        if not product:
            return False
        # Check if product is a variant (has attribute values)
        if product.product_template_attribute_value_ids:
            return ', '.join(product.product_template_attribute_value_ids.mapped('name'))
        return product.name

    @api.onchange('product_id')
    def _onchange_product_id_set_name(self):
        """
        Automatically set the ticket name to match the product name
        when a product is selected.
        For variants, uses the attribute values only.
        """
        if self.product_id:
            self.name = self._get_product_ticket_name(self.product_id)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to ensure product name is used as ticket name
        when creating new tickets if name is not explicitly provided.
        """
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('name'):
                product = self.env['product.product'].browse(vals['product_id'])
                name = self._get_product_ticket_name(product)
                if name:
                    vals['name'] = name

        return super(EventEventTicket, self).create(vals_list)

    def write(self, vals):
        """
        Override write method to automatically update ticket name when
        product is changed, unless name is explicitly provided in the update.
        """
        if 'product_id' in vals and 'name' not in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            name = self._get_product_ticket_name(product)
            if name:
                vals['name'] = name

        return super(EventEventTicket, self).write(vals)