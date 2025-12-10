# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EventTypeTicket(models.Model):
    """
    Extend the event.type.ticket model (event template tickets) to automatically
    set ticket name from product name when a product is selected.
    """
    _inherit = 'event.type.ticket'

    def _get_product_ticket_name(self, product, lang=None):
        """
        Get the appropriate ticket name from a product.
        For variants: use the attribute values (e.g., "Blue, Large")
        For regular products: use the product name
        Respects the specified language context for translations.

        :param product: product.product recordset
        :param lang: language code (e.g., 'en_US', 'nl_NL'). If None, uses current context.
        :return: translated ticket name string
        """
        if not product:
            return False

        # Use specified language or fallback to context/user language
        if lang is None:
            lang = self._context.get('lang') or self.env.user.lang
        product = product.with_context(lang=lang)

        # Check if product is a variant (has attribute values)
        if product.product_template_attribute_value_ids:
            # Get translated attribute value names
            attribute_values = product.product_template_attribute_value_ids.with_context(lang=lang)
            return ', '.join(attribute_values.mapped('name'))
        return product.name

    def _write_translated_ticket_name(self, product):
        """
        Write the ticket name translations for all installed languages.
        This ensures the name field (which is translatable) has proper
        translations in all active languages.

        :param product: product.product recordset
        """
        if not product:
            return

        # Get all installed languages
        installed_langs = self.env['res.lang'].search([]).mapped('code')

        # Write the name for each language
        for lang_code in installed_langs:
            translated_name = self._get_product_ticket_name(product, lang=lang_code)
            if translated_name:
                # Write to this specific language context
                self.with_context(lang=lang_code).write({'name': translated_name})

    @api.onchange('product_id')
    def _onchange_product_id_set_name(self):
        """
        Automatically set the ticket name to match the product name
        when a product is selected in event templates.
        For variants, uses the attribute values only.
        Note: onchange only sets the current language, actual write happens on save.
        """
        if self.product_id:
            self.name = self._get_product_ticket_name(self.product_id)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to ensure product name is used as ticket name
        when creating new template tickets if name is not explicitly provided.
        Writes translations for all installed languages.
        """
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('name'):
                product = self.env['product.product'].browse(vals['product_id'])
                # Use default language for initial creation
                name = self._get_product_ticket_name(product)
                if name:
                    vals['name'] = name

        records = super(EventTypeTicket, self).create(vals_list)

        # After creation, write translations for all languages
        for record in records:
            if record.product_id:
                record._write_translated_ticket_name(record.product_id)

        return records

    def write(self, vals):
        """
        Override write method to automatically update ticket name when
        product is changed in templates, unless name is explicitly provided.
        Writes translations for all installed languages.
        """
        if 'product_id' in vals and 'name' not in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            # Use default language for initial write
            name = self._get_product_ticket_name(product)
            if name:
                vals['name'] = name

        result = super(EventTypeTicket, self).write(vals)

        # After write, update translations for all languages if product changed
        if 'product_id' in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            for record in self:
                record._write_translated_ticket_name(product)

        return result


class EventEventTicket(models.Model):
    """
    Extend the event.event.ticket model to automatically set ticket name
    from product name when a product is selected.
    """
    _inherit = 'event.event.ticket'

    def _get_product_ticket_name(self, product, lang=None):
        """
        Get the appropriate ticket name from a product.
        For variants: use the attribute values (e.g., "Blue, Large")
        For regular products: use the product name
        Respects the specified language context for translations.

        :param product: product.product recordset
        :param lang: language code (e.g., 'en_US', 'nl_NL'). If None, uses current context.
        :return: translated ticket name string
        """
        if not product:
            return False

        # Use specified language or fallback to context/user language
        if lang is None:
            lang = self._context.get('lang') or self.env.user.lang
        product = product.with_context(lang=lang)

        # Check if product is a variant (has attribute values)
        if product.product_template_attribute_value_ids:
            # Get translated attribute value names
            attribute_values = product.product_template_attribute_value_ids.with_context(lang=lang)
            return ', '.join(attribute_values.mapped('name'))
        return product.name

    def _write_translated_ticket_name(self, product):
        """
        Write the ticket name translations for all installed languages.
        This ensures the name field (which is translatable) has proper
        translations in all active languages.

        :param product: product.product recordset
        """
        if not product:
            return

        # Get all installed languages
        installed_langs = self.env['res.lang'].search([]).mapped('code')

        # Write the name for each language
        for lang_code in installed_langs:
            translated_name = self._get_product_ticket_name(product, lang=lang_code)
            if translated_name:
                # Write to this specific language context
                self.with_context(lang=lang_code).write({'name': translated_name})

    @api.onchange('product_id')
    def _onchange_product_id_set_name(self):
        """
        Automatically set the ticket name to match the product name
        when a product is selected.
        For variants, uses the attribute values only.
        Note: onchange only sets the current language, actual write happens on save.
        """
        if self.product_id:
            self.name = self._get_product_ticket_name(self.product_id)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to ensure product name is used as ticket name
        when creating new tickets if name is not explicitly provided.
        Writes translations for all installed languages.
        """
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('name'):
                product = self.env['product.product'].browse(vals['product_id'])
                # Use default language for initial creation
                name = self._get_product_ticket_name(product)
                if name:
                    vals['name'] = name

        records = super(EventEventTicket, self).create(vals_list)

        # After creation, write translations for all languages
        for record in records:
            if record.product_id:
                record._write_translated_ticket_name(record.product_id)

        return records

    def write(self, vals):
        """
        Override write method to automatically update ticket name when
        product is changed, unless name is explicitly provided in the update.
        Writes translations for all installed languages.
        """
        if 'product_id' in vals and 'name' not in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            # Use default language for initial write
            name = self._get_product_ticket_name(product)
            if name:
                vals['name'] = name

        result = super(EventEventTicket, self).write(vals)

        # After write, update translations for all languages if product changed
        if 'product_id' in vals and vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            for record in self:
                record._write_translated_ticket_name(product)

        return result