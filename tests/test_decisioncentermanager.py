# Copyright contributors to the IBM ODM MCP Server project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from unittest.mock import Mock
from decisioncenter_mcp_server.DecisionCenterManager import DecisionCenterManager
from http.server import BaseHTTPRequestHandler, HTTPServer
from decisioncenter_mcp_server.Credentials import Credentials
import json
import threading
import os

class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/decisioncenter-api/v1/endpoint':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(mock_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_mock_server(server_class=HTTPServer, handler_class=MockServerRequestHandler, port=8885):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

@pytest.fixture(scope='module', autouse=True)
def mock_server():
    # Start the mock server in a separate thread
    mock_server_thread = threading.Thread(target=run_mock_server)
    mock_server_thread.daemon = True
    mock_server_thread.start()
    yield
    # Cleanup code can be added here if needed

class Parameter:
    def __init__(self, name:str, type:str, location:str, required:bool, description:str=None, enum:list[str]=None, format:str=None):
        self.name = name
        self.type = type
        self.location = location
        self.required = required
        self.enum = enum
        self.format = format
        self.description = description

def test_generate_tools_format():

    def get_file_path(filename):
        # Locate the folder where the script is stored
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Combine folder path with the target file name
        return os.path.join(base_dir, filename)

    odm_url = 'http://localhost:8885/decisioncenter-api'

    manager = DecisionCenterManager(credentials=Credentials(
        odm_url=odm_url,
        username=os.environ.get('TEST_USERNAME', 'mock_user'),
        password=os.environ.get('TEST_PASSWORD', 'mock_password_placeholder')))

    endpoints  = manager._fetch_endpoints(get_file_path('openapi-9501.json'))
    # endpoints  = manager._fetch_endpoints(get_file_path('test.json'))
    repository = manager.generate_tools_format(endpoints)

    # verify all tools were generated
    assert len(repository) == 133

    def check_endpoint(tool_name:str, method:str, url:str, summary:str, parameters:list[Parameter]):
        endpoint = repository[tool_name]
        assert endpoint
        assert endpoint.method  == method
        assert endpoint.url     == odm_url + url
        assert len(endpoint.parameters) == len(parameters), print(repr(endpoint.parameters))

        assert endpoint.tool
        assert endpoint.tool.name  == tool_name
        assert endpoint.tool.title == summary
        assert len(endpoint.tool.inputSchema['properties']) == len(parameters), print(repr(endpoint.tool.inputSchema['properties']))

        for expected_param in parameters:
            actual_parameter = endpoint.parameters.get(expected_param.name)
            assert actual_parameter,                                        print(actual_parameter, expected_param.name, repr(endpoint.parameters))
            assert actual_parameter['in'] == expected_param.location,       print(repr(endpoint.parameters.get(expected_param.name)))
            assert actual_parameter.get('format') == expected_param.format, print(repr(endpoint.parameters.get(expected_param.name)))

            actual_prop = endpoint.tool.inputSchema['properties'][expected_param.name]
            assert actual_prop
            assert actual_prop['type'] == expected_param.type,                      print(expected_param.name, repr(actual_prop))
            assert actual_prop.get('enum') == expected_param.enum,                  print(expected_param.name, repr(actual_prop))
            assert actual_prop.get('description') == expected_param.description,    print(expected_param.name, repr(actual_prop))
            assert (expected_param.name in endpoint.tool.inputSchema['required']) == expected_param.required

    # check a representative subset of tools
    check_endpoint('registerWebhook', 
                   'PUT',
                   '/v1/webhook/notify',
                   'Register a webhook to notify other applications of events that are coming from Decision Center',
                   [
                       Parameter('url',        'string', 'query',      True, "The URL of the server to send notifications"),
                       Parameter('datasource', 'string', 'query',     False, "The JNDI name of the Decision Center data source. If not specified, it defaults to jdbc/ilogDataSource"),
                       Parameter('body',       'string', 'body/json', False, "The authentication token of the remote server"),
                    ]
                   )
    check_endpoint('rejectRelease', 
                   'POST',
                   '/v1/releases/{releaseId}/reject',
                   'Reject the open release of a decision service',
                   [
                       Parameter('releaseId',  'string', 'path',        True, None),
                       Parameter('userName',   'string', 'query',      False, "the name of the user on behalf of whom rejecting the release."),
                       Parameter('datasource', 'string', 'query',      False, "The JNDI name of the Decision Center data source. If not specified, it defaults to jdbc/ilogDataSource"),
                       Parameter('body',       'string', 'body/plain', False, "the rejection comment."),
                    ]
                   )
    check_endpoint('updateServer', 
                   'POST',
                   '/v1/servers/{serverId}',
                   'Update a target server to use for deployments, simulations, and tests',
                   [
                       Parameter('serverId',              'string', 'path',       True, "The ID of the server"),
                       Parameter('datasource',            'string', 'query',     False, "The JNDI name of the Decision Center data source. If not specified, it defaults to jdbc/ilogDataSource"),
                       Parameter('createdBy',             'string', 'body/json', False),
                       Parameter('createdOn',             'string', 'body/json', False, format="date-time"),
                       Parameter('lastchangedBy',         'string', 'body/json', False),
                       Parameter('lastChangedOn',         'string', 'body/json', False, format="date-time"),
                       Parameter('url',                   'string', 'body/json', False, "The URL of the server"),
                       Parameter('description',           'string', 'body/json', False, "The description of the server"),
                       Parameter('loginServer',           'string', 'body/json', False, "The name of the user allowed to access the server"),
                       Parameter('loginPassword',         'string', 'body/json', False, "The password of the user allowed to access the server"),
                       Parameter('authenticationKind',    'string', 'body/json', False, enum=['BASIC_AUTH', 'OAUTH'], description="The type of authentication used by the server"),
                       Parameter('authenticationProvider','string', 'body/json', False, "The name of the authentication provider to use (for OAUTH authentication kind)"),
                       Parameter('groups',                'array',  'body/json', False, "A list of groups allowed to use this server. A list with the single element * means all groups are allowed to use this server"),
                    ]
                   )