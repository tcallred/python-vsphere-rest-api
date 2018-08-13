"""
  Written by Taylor Allred (taylor.allred@microfocus.com)
  Rest API middle-man to get cpu and memory usage of a virtual machine running on an ESXi host
"""

from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS
from vm_perf import specific_vm_perf
import traceback
import sys

app = Flask(__name__)
CORS(app)
api = Api(app)

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
REST_IP = sys.argv[3]


class VirtualMachine(Resource):
    """
      Usage: <rest-server-ip-or-dns>:<port>/vm?host=<host>&name=<vm-name>
            eg 151.155.216.36:5000/vm?host=151.155.216.208&name=eDir-st8123

      Returns: JSON with cpu and memory usage as % (divide by 100) and disk space as percentage (no divide)
            eg 'mem':'266' -> using 2.66% of memory, 'disk': '58' -> using 58% of disk

    """
    def get(self):
        try:
            args = request.args
            if len(request.args) < 2:
                return "Not enough params", 400
            res = specific_vm_perf(args['host'], USERNAME, PASSWORD, args['name'])
            return res, 200
        except Exception as e:
            traceback.print_exc()
            return str(e), 400


api.add_resource(VirtualMachine, "/vm")
app.run(host=REST_IP)
