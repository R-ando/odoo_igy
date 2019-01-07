# - * - coding: utf-8 - * -
from odoo.exceptions import UserError
import base64
from odoo import api, fields, models, _, tools
from odoo import modules
import odoo.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLineAdvance(models.TransientModel):
    _name = 'sale.order.line.advance'
    _description = 'Product configuration'

#   Add_image
    image = fields.Binary(
        string="Image")
    order_id = fields.Many2one(
        string="Order Line",
        comodel_name="sale.order.line")

    sujet = fields.Char(
        string="Sujet",
        readonly=True)
    select_type = fields.Many2one(
        string="Type",
        comodel_name="product.product",
        domain=[('categ_id', '=', 3)],
        change_default=True)
    largeur = fields.Float(
        string="Largeur",
        default=1.0)
    hauteur = fields.Float(
        string="Hauteur",
        default=1.0)
    dimension = fields.Float(
        string="Dimension")
    pu_ttc = fields.Float(
        string="PU TTC")
    quantity = fields.Integer(
        string="Quantité",
        default=1)
    vitre = fields.Many2one(
        string="Vitre",
        comodel_name="mim.article",
        domain=[('category_id', '=', 'Vitrage')])
    type_vitre = fields.Selection(
        string="",
        selection=[('simple', 'Simple'), ('double', 'Double')])
    decoratif = fields.Many2one(
        string="Décoratif",
        comodel_name="mim.article",
        domain=[('category_id', '=', 'Decoratif')])
    poigne = fields.Many2one(
        string="Poignée",
        comodel_name="mim.article",
        domain=[('category_id', '=', 'Poignee')])
    nb_poigne = fields.Integer(
        string="Nombre",
        default=1.0)
    serr = fields.Many2one(
        string="Serrure",
        comodel_name="mim.article",
        domain=[('category_id.name', '=', 'Serrure')])
    nb_serr = fields.Integer(
        string="Nombre",
        default=1.0)
    oscillo_battant = fields.Boolean(
        string="Oscillo - battant")
    va_et_vient = fields.Boolean(
        string="Va et vient")
    butoir = fields.Boolean(
        string="Butoir")
    remplissage_vitre = fields.Selection(
        string='Remplissage vitre',
        selection=[
            ('standard', 'Standard'),
            ('pleine_2_3', '2/3 pleine'),
            ('pleine_1_2', '1/2 pleine'),
            ('pleine_1_3', '1/3 pleine'),
            ('pleine_bardage', 'Pleine/bardage')
        ]
    )
    type_fixe = fields.Selection(
        string="Type Fixe",
        selection=[
            ('imposte', 'Imposte'),
            ('soubassement', 'Soubassement'),
            ('lateral', u'Latéral')
        ]
    )
    inegalite = fields.Selection(
        string=u"Inégalité",
        selection=[
            ('egaux', 'Egaux'),
            ('inegaux', u'Inégaux')
        ]
    )
    type_poteau = fields.Selection(
        string="Poteau Rect / Angle / Tendeur",
        selection=[
            ('poteau_rect', 'Poteau rectangle'),
            ('poteau_angle', 'Poteau d\'angle'),
            ('tendeur', 'Tendeur')
        ]
    )
    cintre = fields.Boolean(
        string="Cintré")
    triangle = fields.Boolean(
        string="Triangle")
    division = fields.Boolean(
        string="Division")
    nb_division = fields.Integer(
        string="Nombre division",
        default=1.0)
    laque = fields.Boolean(
        string="Laqué")
    moustiquaire = fields.Boolean(
        string="Moustiquaire")
    tms = fields.Float(
        string="TMS")
    type_moustiquaire = fields.Selection(
        string="Type de moustiquaire",
        selection=[
            ('fixe', 'Fixe'),
            ('coulissante', 'Coulissante'),
        ]
    )
    total = fields.Float(
        string="Total",
        readonly=True,
        digits=dp.get_precision('Account'),
        compute='_compute_total',)
    totalcacher = fields.Float(
        string="Total",
        digits=dp.get_precision('Account'),
        compute='_compute_total',)
    hidder_autre_option = fields.Boolean(
        string="Cacher les autres options")
    cacher = fields.Boolean(
        String="Cacher",
        default=False)
    intermediaire = fields.Selection(
        string=u"Intermédiaire",
        selection=[
            ('sans', u'Sans intermédiaire'),
            ('avec', u'Avec intermédiaire'),
        ]
    )

#   Changement automatique du total en fonction des autres champs
    @api.depends(
        'total', 'largeur', 'hauteur', 'dimension', 'pu_ttc', 'quantity',
        'select_type', 'vitre', 'type_vitre', 'decoratif', 'poigne',
        'serr', 'nb_poigne', 'nb_serr', 'oscillo_battant', 'va_et_vient',
        'butoir', 'remplissage_vitre', 'cintre', 'triangle', 'division',
        'nb_division', 'laque', 'moustiquaire', 'type_moustiquaire', 'tms',
        'intermediaire')
    def _compute_total(self):
        select_type = self.select_type
        vitre = self.vitre
        type_vitre = self.type_vitre
        decoratif = self.decoratif
        serr = self.serr
        poigne = self.poigne
        nb_poigne = self.nb_poigne
        nb_serr = self.nb_serr
        oscillo_battant = self.oscillo_battant
        va_et_vient = self.va_et_vient
        butoir = self.butoir
        remplissage_vitre = self.remplissage_vitre
        cintre = self.cintre
        triangle = self.triangle
        division = self.division
        nb_division = self.nb_division
        laque = self.laque
        moustiquaire = self.moustiquaire
        type_moustiquaire = self.type_moustiquaire
        tms = self.tms
        largeur = self.largeur
        hauteur = self.hauteur
        intermediaire = self.intermediaire
        dimension = self.dimension
        pu_ttc = self.pu_ttc
        quantity = self.quantity

        val_total = 0.0
        val_vitre = 0.0
        val_type_vitre = 1
        val_autre_vitrage = 0.0
        val_decoratif = 0.0
        val_poigne = 0.0
        val_serr = 0.0
        val_oscillo_battant = 0.0
        val_va_et_vient = 0.0
        val_butoir = 0.0
        val_remplissage_vitre = 1
        val_cintre = 1
        val_triangle = 1
        val_laque = 1
        val_moustiquaire = 0.0
        cacher = False
        hidder_autre_option = False
        types = ""

        if vitre:
            val_vitre = self.vitre.price

        if type_vitre == 'double':
            if vitre:
                val_type_vitre = 2
            else:
                val_vitre = 55000

        if decoratif:
            categ = self.decoratif
            if categ.category_id.id:
                val_decoratif = categ.price

        if poigne:
            categ = self.poigne
            if categ.category_id.id:
                val_poigne = categ.price * nb_poigne

        if serr:
            categ = self.serr
            if categ.category_id.id:
                val_serr = categ.price * nb_serr

        if oscillo_battant:
            val_oscillo_battant = 150000

        if va_et_vient:
            if select_type == 'porte_ouvrante2vtx':
                val_va_et_vient = 480000
            else:
                val_va_et_vient = 240000

        if butoir:
            val_butoir = 21000

        if remplissage_vitre is not None:
            if remplissage_vitre == 'standard':
                val_remplissage_vitre = 1
            if remplissage_vitre == 'pleine_2_3':
                val_remplissage_vitre = 1.14
            if remplissage_vitre == 'pleine_1_2':
                val_remplissage_vitre = 1.1
            if remplissage_vitre == 'pleine_1_3':
                val_remplissage_vitre = 1.07
            if remplissage_vitre == 'pleine_bardage':
                val_remplissage_vitre = 1.2

        if cintre:
            val_cintre = 2

        if triangle:
            val_triangle = 1.50

        if laque:
            val_laque = 1.15

        if select_type:
            types = self.select_type.name

        if types == 'Coulissante 2VTX':
            if moustiquaire:
                val_moustiquaire = (((largeur / 2 * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = ((((((largeur * hauteur) / 1000000 * (170000 + val_vitre * val_type_vitre + val_decoratif) * (1 + (tms / 100)) * val_remplissage_vitre) + 29700 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 0.95 * 1.1 * 1.08 * val_cintre * val_triangle) + val_moustiquaire) * val_laque) * 1.10

        if types == 'Coulissante 1VTL':
            if moustiquaire:
                val_moustiquaire = (((largeur / 2 * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = (((((((largeur * 2) * hauteur) / 1000000 * (170000 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100)) * val_remplissage_vitre) + 29700 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 0.95 * 1.1 * 1.08 * val_cintre / 2) * val_laque) + val_moustiquaire) * 1.10

        if types == 'Coulissante 3VTX':
            if moustiquaire:
                val_moustiquaire = (((largeur / 3 * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = (((((largeur * hauteur) / 1000000 * (180000 * (1 + (tms / 100)) + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) + val_remplissage_vitre) + 29700 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.025 * 1.08 * val_cintre + val_moustiquaire) * val_laque) * 1.10

        if types == 'Coulissante 4VTX':
            if moustiquaire:
                val_moustiquaire = (((largeur / 2 * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = ((((largeur * hauteur) / 1000000 * (180000 / 2 * (1 + (tms / 100)) * val_remplissage_vitre + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * 2 + 29700 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.05 * 1.025 * 1.08 * val_cintre * val_laque) + val_moustiquaire) * 1.10

        if types == 'Porte ouvrante 2VTX':
            if moustiquaire:
                val_moustiquaire = (((largeur / hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = (((largeur * hauteur) / 1000000 * ((210222 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100))) * val_remplissage_vitre + 92884 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.15 * 1.08 * val_cintre * val_laque) + val_moustiquaire

        if types == 'Porte ouvrante 1VTL':
            if moustiquaire:
                val_moustiquaire = (((largeur / 2 * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = ((((largeur * hauteur) / 1000000 * (210000 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100)) * val_remplissage_vitre) + 58652 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.15 * 1.08 * val_cintre + val_moustiquaire) * val_laque

        if types == u'Fenêtre ouvrante 1VTL':
            if moustiquaire:
                val_moustiquaire = (((largeur / 2 * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = ((((largeur * hauteur) / 1000000 * (210000 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100)) * val_remplissage_vitre) + 58652 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.15 * 1.08 * val_cintre + val_moustiquaire) * val_laque

        if types == u'Fenêtre ouvrante 2VTX':
            if moustiquaire:
                val_moustiquaire = (((largeur / hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = ((((largeur * hauteur) / 1000000 * (210222 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100))) * val_remplissage_vitre + 92884 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir + 40000) * 1.15 * 1.08 * val_cintre * val_laque) + val_moustiquaire

        if types == 'A soufflet':
            if division:
                val_total = (((((largeur / nb_division) * hauteur) / 1000000 * (163000 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100))) * val_remplissage_vitre + 58500 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.1 * 1.05 * 1.25 * 1.08 * val_cintre) * nb_division
            else:
                if moustiquaire:
                    val_moustiquaire = ((((largeur * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4))
            val_total = ((((largeur * hauteur) / 1000000 * (163000 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100)) * val_remplissage_vitre + 58500 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.1 * 1.05 * 1.25 * 1.08 * val_cintre) * val_laque) + val_moustiquaire
        if types == 'Projetant':
            if division:
                val_total = (((((largeur / nb_division) * hauteur) / 1000000 * (163000 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100))) * val_remplissage_vitre + 58500 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.1 * 1.05 * 1.25 * 1.08 * val_cintre) * nb_division
            else:
                if moustiquaire:
                    val_moustiquaire = ((((largeur * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4))
            val_total = ((((largeur * hauteur) / 1000000 * (163000 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * (1 + (tms / 100)) * val_remplissage_vitre + 58500 + val_poigne + val_serr + val_oscillo_battant + val_va_et_vient + val_butoir) * 1.1 * 1.05 * 1.25 * 1.08 * val_cintre) * val_laque) + val_moustiquaire

        if types == 'Fixe':
            if moustiquaire:
                val_moustiquaire = (((largeur / 2 * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4)
            val_total = ((largeur * hauteur) / 1000000 * (150000 + val_vitre * val_type_vitre + val_decoratif + val_autre_vitrage) * val_remplissage_vitre * 1.15 * 1.08 * val_cintre * val_triangle * val_laque) + val_moustiquaire

        if types == 'Moustiquaire':
            cacher = True
            if type_moustiquaire == 'fixe':
                val_total = ((((largeur / nb_division) * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4) * nb_division
            if type_moustiquaire == 'coulissante':
                val_total = ((((largeur / nb_division) * hauteur) / 1000000 * 81000) * 1.2 * 1.08) * nb_division

        if types == 'Naco':
            if moustiquaire:
                val_moustiquaire = ((((largeur * hauteur) / 1000000 * 13500) * 1.2 * 1.08 * 1.4))
            if division:

                val_total = (((largeur / nb_division) * hauteur) / 1000000 * (150000 + val_decoratif + val_autre_vitrage + (3000 * (hauteur / 100)))) * 1.15 * 1.08 * val_cintre * val_laque * nb_division
            else:

                val_total = ((((largeur * hauteur) / 1000000 * (150000 + val_vitre * val_type_vitre + val_autre_vitrage + (3000 * (hauteur / 100)))) * 1.15 * 1.08 * val_cintre * val_laque)) + val_moustiquaire

        if types == 'Poteau rectangle':
            cacher = True
            if laque is True:
                val_total = ((dimension / 1000) * pu_ttc) * val_laque
            if laque is False:
                val_total = ((dimension / 1000) * pu_ttc) * 1

        if types == 'Poteau d\'angle':
            cacher = True
            if laque is True:
                val_total = ((dimension / 1000) * pu_ttc) * val_laque
            if laque is False:
                val_total = ((dimension / 1000) * pu_ttc) * 1

        if types == 'Tendeur':
            cacher = True
            if laque is True:
                val_total = ((dimension / 1000) * pu_ttc) * val_laque
            if laque is not False:
                val_total = ((dimension / 1000) * pu_ttc) * 1

        if types == 'Bardage PVC':
            cacher = True
            hidder_autre_option = True
            val_total = ((largeur * hauteur) / 1000000) * 45000 / 1.2

        order_obj = self.env['sale.order']
        maj1 = order_obj.partner_id.major1 / 100
        maj2 = order_obj.user_id.major2 / 100
        maj_globale = 0.0
        if order_obj.company_id:
            maj_globale = order_obj.company_id.maj_globale / 100

#   Erreur si certains champs ne sont pas correctement remplis
        if largeur is False or largeur == 0:
            msg = _(u'Le champ Largeur ne peut pas être vide ou égal à 0')
            raise UserError(msg)

        if hauteur is False or hauteur == 0:
            msg = _(u'Le champ Hauteur ne peut pas être vide ou égal à 0')
            raise UserError(msg)

        self.total = ((val_total * quantity * 1.10) * (1 + maj1 + maj2)) * (1 + maj_globale)
        self.totalcacher = ((val_total * quantity * 1.10) * (1 + maj1 + maj2)) * (1 + maj_globale)
        self.cacher = cacher
        self.hidder_autre_option = hidder_autre_option

#   modification de l'image selon le type
        image_name = 'image0.png'
        if types == 'A soufflet':
            image_name = 'image1.png'
            if nb_division == 2:
                image_name = 'image3.png'

        if types == 'Projetant':
            image_name = 'image2.png'
            if nb_division == 2:
                image_name = 'image4.png'

        if types == u'Fenêtre ouvrante 1VTL':
            image_name = 'image11.png'
            if remplissage_vitre == 'pleine_bardage':
                image_name = 'image12.png'

        if types == u'Fenêtre ouvrante 2VTX':
            image_name = 'image13.png'
            if remplissage_vitre:
                if remplissage_vitre == 'pleine_bardage':
                    image_name = 'image14.png'

        if types == 'Fixe':
            image_name = 'image17.png'
            if nb_division == 2:
                image_name = 'image18.png'
            if nb_division == 3:
                image_name = 'image19.png'

        if types == 'Porte ouvrante 1VTL':
            image_name = 'image26.png'
            if (remplissage_vitre and remplissage_vitre != 'standard'):
                if remplissage_vitre == u'pleine_bardage':
                    if intermediaire == 'avec':
                        image_name = 'image21.png'
                    else:
                        image_name = 'image20.png'
                if remplissage_vitre == u'pleine_2_3':
                    image_name = 'image22.png'
                if remplissage_vitre == u'pleine_1_2':
                    image_name = 'image23.png'
                if remplissage_vitre == u'pleine_1_3':
                    image_name = 'image24.png'
            elif intermediaire == 'avec':
                    image_name = 'image25.png'

        if types == 'Porte ouvrante 2VTX':
            image_name = 'image33.png'
            if (remplissage_vitre and remplissage_vitre != 'standard'):
                if remplissage_vitre == u'pleine_bardage':
                    if intermediaire == 'avec':
                        image_name = 'image28.png'
                    else:
                        image_name = 'image27.png'
                if remplissage_vitre == u'pleine_2_3':
                    image_name = 'image29.png'
                if remplissage_vitre == u'pleine_1_2':
                    image_name = 'image30.png'
                if remplissage_vitre == u'pleine_1_3':
                    image_name = 'image31.png'
            elif intermediaire == 'avec':
                    image_name = 'image32.png'

        if tms == 0.0:
            if types == 'Coulissante 2VTX':
                image_name = 'image34.png'
            if types == 'Coulissante 3VTX':
                image_name = 'image36.png'
            if types == 'Coulissante 4VTX':
                image_name = 'image35.png'
        else:
            if types == 'Coulissante 1VTL':
                image_name = 'image42.png'
            if types == 'Coulissante 2VTX':
                image_name = 'image43.png'
                if (remplissage_vitre and remplissage_vitre != 'standard'):
                    if remplissage_vitre == u'pleine_bardage':
                        if intermediaire == 'avec':
                            image_name = 'image38.png'
                        else:
                            image_name = 'image0.png'
                    if remplissage_vitre == u'pleine_2_3':
                        image_name = 'image0.png'
                    if remplissage_vitre == u'pleine_1_2':
                        image_name = 'image39.png'
                    if remplissage_vitre == u'pleine_1_3':
                        image_name = 'image40.png'
                elif intermediaire == 'avec':
                    image_name = 'image41.png'

            if types == 'Coulissante 3VTX':
                image_name = 'image44.png'
            if types == 'Coulissante 4VTX':
                image_name = 'image45.png'

        with open(modules.get_module_resource('sale_mim', 'static/src/img', (image_name)), 'rb') as f:
            image = base64.b64encode(f.read())
        resized_image = tools.image_resize_image_medium(image, size=(128, 64))

        self.image = resized_image

#   Créer une ligne de commande à partir du pop-up
    def order_line_create(self, vals):
        order_id = self.order_id.id
        select_type = self.select_type
        type_fix = self.type_fixe
        inegalite = self.inegalite
        vitrage = self.vitre
        type_vitre = self.type_vitre
        decoratif = self.decoratif
        serr = self.serr
        nb_serr = self.nb_serr
        poigne = self.poigne
        nb_poigne = self.nb_poigne
        oscillo_battant = self.oscillo_battant
        va_et_vient = self.va_et_vient
        butoir = self.butoir
        remplissage_vitre = self.remplissage_vitre
        cintre = self.cintre
        triangle = self.triangle
        division = self.division
        nb_division = self.nb_division
        laque = self.laque
        moustiquaire = self.moustiquaire
        type_moustiquaire = self.type_moustiquaire
        tms = self.tms
        rec_largeur = self.largeur
        rec_hauteur = self.hauteur
        intermediaire = self.intermediaire
        rec_dimension = self.dimension
        rec_pu_ttc = self.pu_ttc
        rec_qty = self.quantity
        image = self.image
        total = self.total
        _logger.info("\n*****select_type = %s*****\n" % self)
        types = select_type.name
        vitre = ''
        poignee = ''
        btr = ''
        oscillo = ''
        v_et_v = ''
        rempli = ''
        ctr = ''
        lq = ''
        trgl = ''
        mstqr = ''
        dvs = ''
        tmss = ''
        simple_double = ''
        deco = ''
        intermdr = ''
        inegalit = ''

        if type_vitre:
            if type_vitre == 'double':
                simple_double = ' double,'

        dec = decoratif.name
        if ((decoratif.name is not None) and(decoratif.name is not False)):
            if dec == u'Compliqué':
                deco = u' compliqué,'

        if intermediaire:
            if intermediaire == 'sans':
                intermdr = ''
            if intermediaire == 'avec':
                intermdr = u' avec intermédiaire, '

        if inegalite:
            if inegalite == 'egaux':
                inegalit = ''
            if inegalite == u'inegaux':
                inegalit = u'inégaux,'

        if ((vitrage.name is False) or (vitrage.name is None)):
            vitre = '\n - Vitrage : standard, '
        else:
            vitre = u"\n - Vitrage : " + vitrage.name + ", "

        if ((poigne.name is not None) and (poigne.name is not False)):
            poignee = u'' + poigne.name + ''

        if butoir:
            btr = " avec butoir, "

        if va_et_vient:
            v_et_v = " avec va et vient,"

        if oscillo_battant:
            oscillo = " oscillo battant, "

        if remplissage_vitre:
            if remplissage_vitre == 'standard':
                remplissage_vitre = ''
            if remplissage_vitre == u'pleine_2_3':
                remplissage_vitre = u'2/3 pleine'
            if remplissage_vitre == u'pleine_1_2':
                remplissage_vitre = u'1/2 pleine'
            if remplissage_vitre == u'pleine_1_3':
                remplissage_vitre = u'1/3 pleine'
            if remplissage_vitre == u'pleine_bardage':
                remplissage_vitre = u'Pleine/bardage'
            rempli = " " + str(remplissage_vitre) + ", "

        if cintre:
            ctr = u" cintré, "

        if laque:
            lq = u" laqué, "

        if triangle:
            trgl = u" Triangle, "

        if moustiquaire:
            mstqr = "  avec moustiquaire "

        if division:
            if(nb_division > 1):
                dvs = " " + str(nb_division) + " divisions, "
            else:
                dvs = " " + str(nb_division) + " division, "

        if tms != 0.0:
            tmss = " TMS, "

        type_porte = u'Fenêtre'
        if types == 'Coulissante 2VTX':
            if tms != 0.0:
                type_porte = 'Porte'
            serrure = ''
            if serr.name is not None:
                if moustiquaire:
                    serrure = u' 2 serrures encastrées 2 points '
                else:
                    serrure = u' 1 poignee 4 points à  clef'
            else:
                if moustiquaire:
                    serrure = u' 2 serrures encastrées 2 points'
                else:
                    serrure = u' 1 poignee et 1 serrures encastrées 2 points'
            types = u" " + type_porte + " Coulissante 2VTX " + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " " + serrure + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == 'Coulissante 1VTL':
            serrure = ''
            if serr.name is not None:
                if moustiquaire:
                    serrure = u' 2 serrures encastrées 2 points'
                else:
                    serrure = u' 1 poignée 4 points à  clef'
            else:
                if moustiquaire:
                    serrure = u' 2 serrures encastrées 2 points'
                else:
                    serrure = u' 1 poignée 2 points'
            types = u"Porte Coulissante 1VTL " + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " " + serrure + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == 'Glandage':
            types = "Glandage" + "\n"

        if types == 'Coulissante 3VTX':
            if tms != 0.0:
                type_porte = 'Porte'
            serrure = ''
            if serr.name is not None:
                if moustiquaire:
                    serrure = u' 2 serrures encastrées 2 points'
                else:
                    serrure = u' 1 poignée 4 points à  clef et 1 serrure encastrée 2 point'
            else:
                if moustiquaire:
                    serrure = u' 2 serrures encastrées 2 points'
                else:
                    serrure = u' 1 poignée et 1 serrures encastrées 2 points'
            types = u" " + type_porte + " Coulissante 3VTX " + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " " + serrure + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == 'Coulissante 4VTX':
            if tms != 0.0:
                type_porte = 'Porte'
            serrure = ''
            if serr.name is not None:
                if moustiquaire:
                    serrure = u' 3 serrures encastrées 2 points'
                else:
                    serrure = u' 1 poignée 4 points à  clef'
            else:
                if moustiquaire:
                    serrure = u' 3 serrures encastrées 2 points'
                else:
                    serrure = u' 1 poignée et 2 serrures encastrées 2 points'
            types = u" " + type_porte + " Coulissante 4VTX " + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " " + serrure + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == 'Porte ouvrante 1VTL':
            types = u" Porte ouvrante 1VTL " + "\n - Accessoires :" + " ".join((tmss + " " + intermdr + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == u'Fenêtre ouvrante 1VTL':
            types = u" Fenêtre ouvrante 1VTL  " + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == 'Porte ouvrante 2VTX':
            types = u" Porte ouvrante 2VTX  " + "\n - Accessoires :" + " ".join((inegalit + " " + tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == u'Fenêtre ouvrante 2VTX':
            types = u" Fenêtre ouvrante 2VTX  " + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == 'A soufflet':
            types = u" A soufflet  " + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == 'Fixe':
            if type_fix:
                if type_fix == 'imposte':
                    types = "Imposte Fixe" + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"
                if type_fix == 'soubassement':
                    types = "Soubassement Fixe" + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"
                if type_fix == 'lateral':
                    types = u"Latéral Fixe" + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"
            else:
                types = u"Fixe" + "\n"

        if types == 'Moustiquaire':
            types = u"Moustiquaire indépendant" + "\n"

        if types == 'Naco':
            types = u"Naco" + "\n - Accessoires :" + " ".join((tmss + " " + dvs + " " + btr + " " + oscillo + " " + v_et_v + " " + ctr + " " + lq + " " + trgl + " ").split()) + vitre + " ".join((simple_double + deco + " " + rempli + " " + mstqr).split()) + " \n"

        if types == 'Poteau rectangle' or 'Poteau d\'angle' or 'Tendeur':
            if types == 'Poteau rectangle':
                types = "Poteau rectangle" + "\n"
            if types == 'Poteau d\'angle':
                types = "Poteau d'angle" + "\n"
            if types == "Tendeur":
                types = "Tendeur" + "\n"

        if types == 'Bardage PVC':
            types = "Bardage PVC" + "\n"

        if types == 'Projetant':
            types = "Projetant" + "\n"

        lxh = types
        if types == 'Poteau rectangle':
            if (rec_dimension and rec_pu_ttc):
                lxh = lxh + " \n\t - Dimension : %d x %d \n" % (rec_dimension, rec_pu_ttc,)
        else:
            if(rec_largeur and rec_hauteur):
                lxh = lxh + "- Dimension : %d x %d HT \n" % (rec_largeur, rec_hauteur,)

        name = lxh
        resized_image = tools.image_resize_image_medium(image, size=(96, 64))

        order_line_vals = {
            'product_id': select_type.id,
            'name': name,
            'image': resized_image,
            'order_id': order_id,
            'product_uom_qty': rec_qty,
            'price_subtotal': total,
            'price_unit': rec_qty and (total / rec_qty),
            'largeur': rec_largeur,
            'hauteur': rec_hauteur,
            'dimension': rec_dimension,
            'vitre': vitrage.id,
            'type_vitre': type_vitre,
            'decoratif': decoratif.id,
            'poigne': poigne.id,
            'nb_poigne': nb_poigne,
            'serr': serr.id,
            'nb_serr': nb_serr,
            'oscillo_battant': oscillo_battant,
            'va_et_vient': va_et_vient,
            'butoir': butoir,
            'remplissage_vitre': remplissage_vitre,
            'type_fixe': type_fix,
            'inegalite': inegalite,
            'cintre': cintre,
            'triangle': triangle,
            'division': division,
            'nb_division': nb_division,
            'laque': laque,
            'moustiquaire': moustiquaire,
            'tms': tms,
            'type_moustiquaire': type_moustiquaire,
            'intermediaire': intermediaire
        }
        _logger.info("\n*****order_line_vals = %s*****\n" % order_line_vals)
        self.env['sale.order.line'].create(order_line_vals)

        return True
