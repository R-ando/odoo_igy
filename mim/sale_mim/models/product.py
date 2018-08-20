# -*- coding: utf-8 -*-

from odoo import fields, api, models


class ArticleCategorie(models.Model):
    _name = "article.categorie"
    _description = "Categorie d'article"
    
    name = fields.Char('Catégorie', size=64, required=True)
    
    _sql_constraints = [
        ('name', 'unique(name)', 'The name of the category must be unique')]


class MimArticle(models.Model):
    _name = 'mim.article'
    
    name = fields.Char('Article', size=64, required=True)
    price = fields.Float('Prix', required=True)
    category_id = fields.Many2one('article.categorie', string='Catégorie', required=True)
        
    _sql_constraints = [
        ('name', 'unique(name)', 'The name of the idea must be unique')
    ]