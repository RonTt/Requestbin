import json
import operator

from flask import session, make_response, request, render_template

from .web import app

@app.endpoint('api.bins')
def bins():
    private = request.form.get('private') == 'true'
    bin = app.config['service'].create_bin(private)
    if bin.private:
        session[bin.name] = bin.secret_key
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, bin.json()), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        resp = make_response(bin.json(), 200)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.endpoint('api.bin')
def bin(name):
    jsonp = request.args.get('jsonp')
    if name:
        try:
            bin = app.config['service'].lookup_bin(name);
        except KeyError:
            return json.dumps(dict(errors=['Bin Not Found'])), 404

        try:
            if jsonp:
                resp = make_response('%s(%s)' % (jsonp, bin.json()), 200)
                resp.headers['Content-Type'] = 'text/javascript'
            else:
                resp = make_response(bin.json(), 200)
                resp.headers['Content-Type'] = 'application/json'
                resp.headers['Access-Control-Allow-Origin'] = '*'
        except KeyError:
            return json.dumps(dict(errors=[keyerror])), 200
    else:
        return json.dumps(dict(errors=['No Bin Name Supplied'])), 404
    return resp

@app.endpoint('api.binrequest')
def bin(name, requestid):
    jsonp = request.args.get('jsonp')
    if name:
        if requestid:
            try:
                bin = app.config['service'].lookup_bin(name);
            except KeyError:
                return json.dumps(dict(errors=['Bin Not Found'])), 404

            try:
                requestid = int(requestid);
                binrequest = bin.requests[requestid];
            except IndexError:
                return json.dumps(dict(errors=['Request Not Found in Bin'])), 404
            except TypeError:
                return json.dumps(dict(errors=['Request Not Found in Bin'])), 404
            except KeyError:
                return json.dumps(dict(errors=['Request Not Found in Bin'])), 404

            try:
                if jsonp:
                    resp = make_response('%s(%s)' % (jsonp, binrequest.json()), 200)
                    resp.headers['Content-Type'] = 'text/javascript'
                else:
                    resp = make_response(binrequest.json(), 200)
                    resp.headers['Content-Type'] = 'application/json'
                    resp.headers['Access-Control-Allow-Origin'] = '*'
            except KeyError:
                return json.dumps(dict(errors=[keyerror])), 200
        else:
            return json.dumps(dict(errors=['No Requets ID Supplied'])), 404
    else:
        return json.dumps(dict(errors=['No Bin Name Supplied'])), 404
    return resp        

@app.endpoint('api.stats')
def stats():
    service = app.config['service']
    stats = {
        'bin_count': service.storage.count_bins(),
        'request_count': service.storage.count_requests(),
        'avg_req_size_kb': service.storage.avg_req_size(), }
    resp = make_response(json.dumps(stats), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp
