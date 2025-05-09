import datetime
from odoo import http
from odoo.http import request
from odoo.addons.arkana_rest.utils.auth import token_auth_required, json_response
import logging

_logger = logging.getLogger(__name__)


class MyApi(http.Controller):

    @http.route(
        "/api/v1/partners/list",
        type="http",
        auth="none",
        methods=["GET"],
        csrf=False
    )
    @token_auth_required
    def get_partners(self, user_id=None, **kwargs):
        try:
            # Use the user_id passed from the decorator
            partners = request.env["res.partner"].with_user(user_id).search([], limit=10)
            data = [
                {
                    "id": p.id,
                    "name": p.name,
                    "email": p.email,
                    "phone": p.phone,
                }
                for p in partners
            ]
            return json_response(data)
        except Exception as e:
            _logger.exception("Error in get_partners")
            return json_response({"error": str(e)}, 500)

    @http.route(
        "/api/v1/partners/detail/<int:partner_id>",
        type="http",
        auth="none",
        methods=["GET"],
        csrf=False
    )
    @token_auth_required
    def get_partner_detail(self, partner_id, user_id=None, **kwargs):
        try:
            # Use the user_id passed from the decorator
            partner = request.env["res.partner"].with_user(user_id).browse(partner_id)
            if not partner.exists():
                return json_response({"error": "Partner not found"}, 404)

            data = {
                "id": partner.id,
                "name": partner.name,
                "email": partner.email,
                "phone": partner.phone,
                "street": partner.street,
                "city": partner.city,
                "country": partner.country_id.name if partner.country_id else None,
            }
            return json_response(data)
        except Exception as e:
            _logger.exception("Error in get_partner_detail")
            return json_response({"error": str(e)}, 500)

    @http.route(
        "/api/v1/partners/update/<int:partner_id>",
        type="http",
        auth="none",
        methods=["POST"],
        csrf=False
    )
    @token_auth_required
    def update_partner(self, partner_id, user_id=None, **kwargs):
        try:
            # Use the user_id passed from the decorator
            partner = request.env["res.partner"].with_user(user_id).browse(partner_id)
            if not partner.exists():
                return json_response({"error": "Partner not found"}, 404)

            # Update partner details with the provided data
            if request.httprequest.content_type == 'application/json':
                payload_data = request.get_json_data()
            else:
                return json_response({"error": "Invalid content type, expected application/json"}, 400)
            partner.write(payload_data)

            # Return only the updated fields in the response
            updated_fields = {
                "id": partner.id,
                "name": partner.name,
                "email": partner.email,
                "phone": partner.phone,
                "changed_fields": {field: getattr(partner, field, None) for field in payload_data.keys()}
            }
            return json_response(updated_fields)
        except Exception as e:
            _logger.exception("Error in update_partner")
            return json_response({"error": str(e)}, 500)

    @http.route(
        "/api/v1/partners/delete/<int:partner_id>",
        type="http",
        auth="none",
        methods=["DELETE"],
        csrf=False
    )
    @token_auth_required
    def delete_partner(self, partner_id, user_id=None, **kwargs):
        try:
            # Use the user_id passed from the decorator
            partner = request.env["res.partner"].with_user(user_id).browse(partner_id)
            if not partner.exists():
                return json_response({"error": "Partner not found"}, 404)

            partner_data = partner.read([
                'id',
                'name',
                'email',
                'phone',
            ])

            # Delete the partner
            partner.unlink()
            return json_response({
                "message": "Partner deleted successfully",
                "old_data": partner_data,
                "delete_date": str(datetime.datetime.now()),
                "deleted_uid": request.env.user.id or None,
            })
        except Exception as e:
            _logger.exception("Error in delete_partner")
            return json_response({"error": str(e)}, 500)
