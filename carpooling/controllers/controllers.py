from odoo import http
from odoo.http import request


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

    @http.route('/available-rides', type='http', auth="public", website=True)
    def get_available_rides(self):
        rides_obj = request.env['car.pooling'].sudo().search([('status', 'in', ('available', 'full'))])
        values = {}
        rides_list = []
        for rides in rides_obj:
            rides_list.append({
                'id': rides.id,
                'driver': rides.driver.name,
                'available_seat': rides.available_seat,
                'departure_date': rides.departure_date,
                'source_city': rides.source_city,
                'destination_city': rides.destination_city,
                'is_round_trip': 'Yes' if rides.is_round_trip else 'No',
                'return_date': rides.return_date
            })

        values.update({
            'rides': rides_list
        })

        return http.request.render('carpooling.available_rides', values)

    @http.route('/my_controller/route', type='http', auth="public", website=True)
    def ride_booking(self, **post):
        user = request.env.user
        print(user.id)
        source_city = post.get('source_city')
        destination_city = post.get('destination_city')
        departure_date = post.get('departure_date')
        capacity = post.get('capacity')
        # 'driver': user,
        result = request.env['car.pooling'].sudo().create(
            {'driver': user.id, 'source_city': source_city, 'destination_city': destination_city,
             'departure_date': departure_date, 'capacity': capacity})
        return request.render('carpooling.enquiry_thanks')

    @http.route('/book-ride', type='http', auth="public", website=True)
    def book_a_ride(self):
        rides_obj = request.env['car.pooling'].sudo().search([('status', 'in', ('available', 'full'))])
        for rides in rides_obj:
            result = request.env['car.pooling.passenger'].sudo().create({'trip_id': rides.id})
        return http.request.render('carpooling.enquiry_thanks')
