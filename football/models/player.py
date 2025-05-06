# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Player(models.Model):
    _name = 'football.player'
    _description = 'Player Model'

    name = fields.Char(string='Name', required=True)
    day_of_birth = fields.Date(string='Day of Birth')
    country = fields.Char(string='Country')
    team = fields.Char(string='Team')
    position = fields.Char(string='Position')
    height = fields.Float(string='Height of the player')
    weight = fields.Float(string='Weight of the player')



