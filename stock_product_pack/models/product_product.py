# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models
import math


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_quantities(self):
        packs = self._context.get('include_pack') and self.filtered('pack_ok') or self.browse([])
        for product in packs.with_context(prefetch_fields=False):
            pack_qty_available = []
            pack_virtual_available = []
            pack_free_qty = []
            subproducts = product.pack_line_ids.filtered(
                lambda p: p.product_id.type == 'product')
            for subproduct in subproducts:
                subproduct_stock = subproduct.product_id
                sub_qty = subproduct.quantity
                if sub_qty:
                    pack_qty_available.append(math.floor(
                        subproduct_stock.qty_available / sub_qty))
                    pack_virtual_available.append(math.floor(
                        subproduct_stock.virtual_available / sub_qty))
                    pack_free_qty.append(math.floor(
                        subproduct_stock.free_qty / sub_qty))
            product.qty_available = pack_qty_available and min(pack_qty_available) or False
            product.incoming_qty = 0
            product.outgoing_qty = 0
            product.virtual_available = pack_virtual_available and min(pack_virtual_available) or False
            product.free_qty = pack_free_qty and min(pack_free_qty) or False
        super(ProductProduct, self - packs)._compute_quantities()
