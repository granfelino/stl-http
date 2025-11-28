✅ Micro-project: Re-create a Mini REST API Using the Standard Library
### Goal:
* Gain intuition for how request routing, status codes, verbs, and response formatting work.
* Use http.server and a custom handler.

### Endpoints:
* GET /items → returns JSON list
* POST /items → parses JSON body and appends to list
* GET /items/<id> → returns single item or 404

### Add:
* Returning proper Content-Type: application/json
* Different status codes (200, 201, 400, 404)
* Parsing request paths into segments
* Reading POST body (self.rfile.read())

### Expected Learning Outcomes:
* path parsing
* method matching (GET vs POST)
* handling body vs headers
* JSON serialization
* where and why status codes are sent
* how an API is structured internally
