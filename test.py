from gevent import pywsgi
from gevent.ssl import SSLContext
from verdebooks.py import app  # Replace with your actual application import

# HTTPS server setup
ssl_context = SSLContext()
ssl_context.load_cert_chain(certfile='/var/www/verdebooks/newcert.pem', keyfile='/var/www/verdebooks/new_privkey.pem')

# HTTPS server
https_server = pywsgi.WSGIServer(('0.0.0.0', 7900), app, ssl_context=ssl_context)
# HTTP server (optional, for testing without SSL)
http_server = pywsgi.WSGIServer(('0.0.0.0', 8000), app)

print("HTTPS server is running on 7900")
print("HTTP server is running on 8000")

https_server.start()
http_server.start()

try:
    https_server.serve_forever()
    http_server.serve_forever()
except KeyboardInterrupt:
    https_server.stop()
    http_server.stop()
