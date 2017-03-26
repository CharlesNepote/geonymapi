#!/usr/bin/python3

import falcon
import json
import requests

import geonym

class HeaderMiddleware:

    def process_response(self, req, resp, resource):
        resp.set_header('X-Powered-By', 'GeonymAPI')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        resp.set_header('Access-Control-Allow-Methods','GET')

class GeonymResource(object):
    def getGeonym(self, req, resp, query=None):
        resp.status = falcon.HTTP_200
        if 'lat' in req.params and 'lon' in req.params:
            query = geonym.ll2geonym(float(req.params['lat']), float(req.params['lon']))
        elif 'geonym' in req.params:
            query = req.params['geonym']

        if query is not None and geonym.checkGeonym(query):
            data = geonym.geonym2ll(query)
            geojson = {"type":"Feature",
                "properties":data,
                "params":geonym.getParams(),
                "geometry":{"type":"Point","coordinates":[data['lon'],data['lat']]}}
            resp.body = json.dumps(geojson, sort_keys=True)
        else:
            resp.status = falcon.HTTP_400

    def on_get(self, req, resp, query=None):
        self.getGeonym(req, resp, query);


# Falcon.API instances are callable WSGI apps.
app = falcon.API(middleware=[HeaderMiddleware()])

# Resources are represented by long-lived class instances
g = GeonymResource()

# things will handle all requests to the matching URL path
app.add_route('/geonym', g)
app.add_route('/{query}', g)