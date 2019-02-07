# -*- coding: utf-8 -*-
from odoo import models, fields, api
from collections import defaultdict
import logging
_logger = logging.getLogger(__name__)


class MigrateFields(models.TransientModel):
    _name = 'migrate.fields'

    model_ids = fields.Many2many(
        string="Model",
        comodel_name="ir.model")

    @api.model
    def _custom_setup_fields(self, model_name):
        """Setup the fields, except for recomputation triggers."""
        model_obj = self.env[model_name]
        cls = type(model_obj)
        _logger.info("\n*****self = %s*****\n" % dir(self))
        _logger.info("\n*****cls = %s*****\n" % cls)

        # set up fields
        bad_fields = []
        for name, field in cls._fields.items():
            try:
                field.setup_full(self)
            except Exception:
                if not self.pool.loaded and field.base_field.manual:
                    # Something goes wrong when setup a manual field.
                    # This can happen with related fields using another manual many2one field
                    # that hasn't been loaded because the comodel does not exist yet.
                    # This can also be a manual function field depending on not loaded fields yet.
                    bad_fields.append(name)
                    continue
                raise

        for name in bad_fields:
            del cls._fields[name]
            delattr(cls, name)

        # map each field to the fields computed with the same method
        groups = defaultdict(list)
        for field in cls._fields.values():
            if field.compute:
                cls._field_computed[field] = group = groups[field.compute]
                group.append(field)
        _logger.info("\n*****groups = %s*****\n" % groups)
        return groups

    def excecute(self):
        for model in self.model_ids:
            model_name = model.model
            groups = self._custom_setup_fields(model_name)
            records = self.env[model_name].search([('order_id', '>', 1)], limit=300)
            # key = function_name
            # vals = field name
            for key, vals in groups.items():
                for modified_field in vals:
                    modified_field_split = str(modified_field).split('.')
                    field_name = modified_field_split[len(modified_field_split) - 1]
                    for record in records:
                        if isinstance(key, str):
                            getattr(record, str(key))()
            _logger.info("\n*****records = %s*****\n" % records)
