# IBM ODM Authoring MCP Server Documentation

## Overview

The IBM ODM Authoring MCP Server bridges IBM ODM Decision Center with modern AI assistants and orchestration platforms.
It enables you to:
- Expose Decision Center REST API endpoints as tools for AI assistants
- Integrate easily with Watson Orchestrate, Claude Desktop, and Cursor AI

## Features

- **Tool Integration:** Expose ODM Decision Center REST API endpoints as tools
- **Authentication:** Zen API Key, Basic Auth, and OpenID Connect
- **Multi-Platform:** Works with Watson Orchestrate, Claude Desktop, and Cursor AI

## Quickstart: Claude Desktop Integration

For detailed instructions on setting up and using Claude Desktop with the Decision MCP Server, see the [Claude Desktop Integration Guide](/docs/Claude-desktop-integration-guide.md).

### Demo Video

## Prerequisites & Installation

### Prerequisites

### Running the Server

## Configuration

### Configuration Parameters Table

| CLI Argument      | Environment Variable | Description                                                                                            | Default                                 |
|-------------------|---------------------|---------------------------------------------------------------------------------------------------------|-----------------------------------------|
| `--url`           | `ODM_URL`           | URL of the Decision Center REST API                      | `http://localhost:9060/decisioncenter-api`             |
| `--username`      | `ODM_USERNAME`      | Username for Basic Auth or Zen authentication                                                           | `odmAdmin`                              |
| `--password`      | `ODM_PASSWORD`      | Password for Basic Auth                                                                                 | `odmAdmin`                              |
| `--zenapikey`     | `ZENAPIKEY`         | Zen API Key for authentication with Cloud Pak for Business Automation                                   |                                         |
| `--client-id`     | `CLIENT_ID`         | OpenID Connect client ID for authentication                                                             |                                         |
| `--client-secret` | `CLIENT_SECRET`     | OpenID Connect client secret for authentication                                                         |                                         |
| `--pkjwt-cert-path` | `PKJWT_CERT_PATH` | Path to the certificate for PKJWT authentication (mandatory for PKJWT)                                  |                                         |
| `--pkjwt-key-path` | `PKJWT_KEY_PATH`   | Path to the private key certificate for PKJWT authentication (mandatory for PKJWT)                      |                                         |
| `--pkjwt-key-password` | `PKJWT_KEY_PASSWORD` | Password to decrypt the private key for PKJWT authentication. Only needed if the key is password-protected. |                               |
| `--token-url`     | `TOKEN_URL`         | OpenID Connect token endpoint URL for authentication                                                    |                                         |
| `--scope`         | `SCOPE`             | OpenID Connect scope used when requesting an access token using Client Credentials for authentication   | `openid`                                |
| `--verifyssl`     | `VERIFY_SSL`        | Whether to verify SSL certificates (`True` or `False`)                                                  | `True`                                  |
| `--ssl-cert-path` | `SSL_CERT_PATH`     | Path to the SSL certificate file. If not provided, defaults to system certificates.                     |                                         |
| `--mtls-cert-path`| `MTLS_CERT_PATH`    | Path to the SSL certificate file of the client for mutual TLS authentication (mandatory for mTLS)       |                                         |
| `--mtls-key-path` | `MTLS_KEY_PATH`     | Path to the SSL private key file of the client for mutual TLS authentication (mandatory for mTLS)       |                                         |
| `--mtls-key-password` | `MTLS_KEY_PASSWORD` | Password to decrypt the private key of the client for mutual TLS authentication. Only needed if the key is password-protected. |              |
| `--log-level`     | `LOG_LEVEL`         | Set the logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)                                 | `INFO`                                  |

> Parameters specific to Decision Center REST API
>| CLI Argument | Environment Variable | Description | Default |
>|--------------|----------------------|-------------|---------|
>| `--tags`     | `TAGS`               | List of tags (eg. About Explore Build). Useful to keep only the tools whose tag is in the list. If this option is not specified, all the tools are published by the MCP server. | |
>| `--tools`    | `TOOLS`              | List of tools to publish (eg. decisionServices releases createRelease). This option can be used along with --tags but it takes precedence over the option --no-tools | |
>| `--no-tools` | `NO_TOOLS`           | List of tools to ignore  (eg. launchCleanup wipe executeSqlScript). This option can be used along with --tags but is ignored if the option --tools is specified. | |

> Parameters to start the MCP server in remote mode (allowing connections from remote MCP clients) 
>| CLI Argument | Environment Variable | Description | Default |
>|--------------|----------------------|-------------|---------|
>| `--transport`| `TRANSPORT`          | `stdio`, `streamable-http` or `sse` : Means of communication of the Decision MCP server: local (`stdio`) or remote (`streamable-http` or `sse`)) | `stdio` |
>| `--host`     | `HOST`               | IP or hostname that the MCP server listens to in remote mode. | `0.0.0.0` |
>| `--port`     | `PORT`               | Port that the MCP server listens to in remote mode. | `3000` |
>| `--mount-path`| `MOUNT_PATH`        | Path that the MCP server listens to in remote mode. | `/mcp` |

### Decision MCP Server Configuration File          
