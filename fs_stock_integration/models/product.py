from odoo import models, fields, api
import requests
import logging
import base64

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def import_products_from_api(self):
        """Import products from a public API with duplicate prevention"""
        try:
            # get from ir.config_parameter
            api_url = self.env['ir.config_parameter'].sudo().get_param(
                'fakestoreapi.product.url'
            )
            if not api_url:
                # hardcoded URL for testing
                api_url = "https://fakestoreapi.com/products"
            _logger.info(f"Fetching products from {api_url}")

            response = requests.get(api_url)
            response.raise_for_status()
            products = response.json()
            _logger.info(f"Successfully fetched {len(products)} products from API")

            created_count = 0
            updated_count = 0
            skipped_count = 0

            for product_data in products:
                api_ref = f"FS-{product_data['id']}"
                _logger.info(f"Processing product with API reference: {api_ref}")

                existing_product = self.search([('default_code', '=', api_ref)], limit=1)

                image_data = None
                if product_data['image']:
                    try:
                        image_response = requests.get(product_data['image'])
                        image_response.raise_for_status()
                        image_data = base64.b64encode(image_response.content).decode('utf-8')
                        _logger.info(f"Successfully fetched image for product {api_ref}")
                    except Exception as img_error:
                        _logger.warning(
                            "Failed to fetch image for product %s: %s", api_ref, img_error
                        )

                vals = {
                    'name': product_data['title'],
                    'default_code': api_ref,
                    'list_price': product_data['price'],
                    'description': product_data['description'],
                    'type': 'product',
                    'image_1920': image_data,
                }

                category_id = self.env['product.category']._get_or_create_category(product_data['category'])
                if category_id:
                    vals['categ_id'] = category_id.id

                if existing_product:
                    existing_product.write(vals)
                    updated_count += 1
                    _logger.info(f"Updated existing product: {api_ref}")
                else:
                    self.create(vals)
                    created_count += 1
                    _logger.info(f"Created new product: {api_ref}")

            message = f'Imported {created_count} products'
            if updated_count:
                message += f', updated {updated_count} products'
            if skipped_count:
                message += f', skipped {skipped_count} existing products'

            _logger.info(message)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': message,
                    'sticky': False,
                }
            }
        except Exception as e:
            _logger.error(f"Product import error: {e}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': str(e),
                    'sticky': True,
                    'type': 'danger',
                }
            }


class ProductCategory(models.Model):
    _inherit = 'product.category'

    fs_code = fields.Char('FakeStoreAPI Code')

    def _get_or_create_category(self, name):
        """Get or create a product category by name and assign relevant fs_code"""
        _logger.info(f"Searching for category with fs_code: {name}")
        category_id = self.search([('fs_code', '=', name)], limit=1)
        if not category_id:
            _logger.info(f"Category with fs_code {name} not found, creating a new one")
            all_parent = self.search([('name', '=', 'All')], limit=1)
            category_id = self.create({
                'name': name.capitalize(),
                'fs_code': name,
                'parent_id': all_parent.id if all_parent else False
            })
            _logger.info(f"Created new category: {category_id.name} with fs_code: {name}")
        else:
            _logger.info(f"Found existing category: {category_id.name} with fs_code: {name}")
        return category_id
