# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import UserError
import logging
import ast

_logger = logging.getLogger(__name__)


class MailActivitySchedule(models.TransientModel):
    _inherit = 'mail.activity.schedule'

    def action_schedule_activities(self):
        self.ensure_one()

        # === GET ACTIVITY TYPE ===
        activity_type = self.activity_type_id

        # === COMPARE USING env.ref() ===
        target_xmlid = 'my_crm_activity.activity_open_survey_form'
        try:
            target_id = self.env.ref(target_xmlid).id
        except ValueError:
            _logger.error("XML ID %s not found!", target_xmlid)
            return super().action_schedule_activities()

        if not activity_type or activity_type.id != target_id:
            return super().action_schedule_activities()

        # === PARSE res_ids ===
        res_ids_str = self.res_ids or '[]'
        try:
            res_ids = ast.literal_eval(res_ids_str)
            if not isinstance(res_ids, list):
                res_ids = [res_ids]
        except (ValueError, SyntaxError):
            raise UserError("Invalid res_ids format.")

        if not res_ids:
            raise UserError("No record selected.")

        res_id = res_ids[0]

        # === GET MODEL & RECORD ===
        res_model = self.res_model
        if not res_model:
            raise UserError("No model selected.")

        record = self.env[res_model].browse(res_id)
        if not record.exists():
            raise UserError("Record not found.")

        # === CREATE ACTIVITY USING res_model_id (Many2one) ===
        self.env['mail.activity'].create({
            'activity_type_id': activity_type.id,
            'summary': self.summary or activity_type.name,
            'res_model_id': self.env['ir.model']._get(res_model).id,  # CORRECT
            'res_id': res_id,
            'user_id': self.activity_user_id.id or self.env.uid,
            'date_deadline': self.date_deadline,
            'note': self.note,
        })

        # === LOG ===
        _logger.warning("OPENING SITE SURVEY FOR %s %s", res_model, res_id)

        # === RETURN WINDOW ACTION ===
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'site.survey',  # CHANGE TO YOUR MODEL
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_opportunity_id': record.id,
                'default_partner_id': record.partner_id.id,
                'default_team_id': record.team_id.id,
            },
        }
