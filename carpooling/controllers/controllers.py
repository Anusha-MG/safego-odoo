from odoo import http


class CarPooling(http.Controller):
    @http.route('/car_pooling/car_pooling', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/car_pooling/car_pooling/objects', auth='public')
    def list(self, **kw):
        return http.request.render('car_pooling.listing', {
            'root': '/car_pooling/car_pooling',
            'objects': http.request.env['car_pooling.car_pooling'].search([]),
        })

    @http.route('/car_pooling/car_pooling/objects/<model("car_pooling.car_pooling"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('car_pooling.object', {
            'object': obj
        })


    @http.route('/home/bookride', type='http', auth="public", website=True)
    def create_ticket_records(self):
        values = {}
        values.update({
        })
        return http.request.render('carpooling.website_helpdesk_form_ticket_submit_form_new', values)
