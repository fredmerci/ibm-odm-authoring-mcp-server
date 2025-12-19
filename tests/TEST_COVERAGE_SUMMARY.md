# Test Coverage Summary for invokeDecisionCenterApi

## Overview
Added comprehensive test suite for the `invokeDecisionCenterApi` function in [`DecisionCenterManager.py`](../src/decisioncenter_mcp_server/DecisionCenterManager.py:364).

## Test Class: TestInvokeDecisionCenterApi

### Test Cases Added (14 tests)

#### 1. **test_invoke_with_path_parameter**
- Tests URL path parameter replacement
- Verifies that `{testId}` in URL is replaced with actual value
- Validates successful JSON response handling

#### 2. **test_invoke_with_missing_required_path_parameter**
- Tests error handling for missing required path parameters
- Expects `ValueError` with message "Missing argument testId"

#### 3. **test_invoke_with_query_parameters**
- Tests query parameter handling
- Verifies multiple query params (datasource, filter) are passed correctly
- Validates they appear in the `params` argument of the request

#### 4. **test_invoke_with_json_body_parameters**
- Tests JSON body parameter handling
- Verifies parameters marked as `body/json` are sent in request body
- Validates proper JSON serialization

#### 5. **test_invoke_with_plain_text_body**
- Tests plain text body handling
- Verifies parameters marked as `body/plain` are sent as raw data
- Tests the `data` parameter of the request

#### 6. **test_invoke_with_file_upload**
- Tests file upload functionality
- Creates temporary file and verifies it's opened and passed correctly
- Tests parameters marked as `body/form` with `format: binary`

#### 7. **test_invoke_response_json**
- Tests JSON response parsing
- Verifies `application/json` content-type handling
- Validates response is properly deserialized

#### 8. **test_invoke_response_text**
- Tests plain text response handling
- Verifies non-JSON responses return as text
- Tests `text/plain` content-type

#### 9. **test_invoke_response_binary_run_locally**
- Tests binary file download when `run_locally=True`
- Verifies file is saved to local filesystem
- Validates response contains `filename` and `url` (file://) fields
- Tests `application/octet-stream` content-type

#### 10. **test_invoke_response_binary_run_remotely**
- Tests binary file handling when `run_locally=False`
- Verifies file content is base64 encoded
- Validates response contains `mimeType`, `filename`, and `data` fields
- Tests proper base64 encoding/decoding

#### 11. **test_invoke_error_response**
- Tests error handling for non-200 status codes
- Verifies exceptions are raised with error message
- Tests 404 response handling

#### 12. **test_invoke_with_mixed_parameters**
- Tests combination of different parameter types
- Verifies path, query, and body parameters work together
- Validates proper routing of each parameter type

#### 13. **test_invoke_cleanup_called**
- Tests that credentials cleanup is called after API invocation
- Verifies proper resource management
- Uses mock to verify `cleanup()` is called once

#### 14. **test_invoke_with_empty_arguments**
- Tests handling of optional parameters
- Verifies empty arguments dict works for endpoints with no required params
- Validates request is made with empty parameter dictionaries

## Test Fixtures

### mock_credentials
- Creates mock [`Credentials`](../src/decisioncenter_mcp_server/Credentials.py:42) object
- Provides mock session with headers
- Includes cleanup mock

### manager
- Creates [`DecisionCenterManager`](../src/decisioncenter_mcp_server/DecisionCenterManager.py:26) instance
- Uses mock_credentials fixture

### sample_endpoint
- Creates sample [`DecisionCenterEndpoint`](../src/decisioncenter_mcp_server/DecisionCenterEndpoint.py:16) for testing
- Includes all parameter types: path, query, body/json, body/form, body/plain
- Provides realistic test scenario

## Coverage Areas

### Parameter Handling
- ✅ Path parameters with URL replacement
- ✅ Query parameters
- ✅ JSON body parameters
- ✅ Plain text body parameters
- ✅ File upload (multipart/form-data)
- ✅ Mixed parameter types
- ✅ Empty/optional parameters

### Response Handling
- ✅ JSON responses
- ✅ Plain text responses
- ✅ Binary file downloads (local mode)
- ✅ Binary file downloads (remote mode with base64)
- ✅ Error responses (non-200 status)

### Edge Cases
- ✅ Missing required parameters
- ✅ Resource cleanup
- ✅ Content-Type detection
- ✅ File handling and cleanup

## Test Execution

Run all tests:
```bash
uv run pytest tests/test_decisioncentermanager.py -v
```

Run only invokeDecisionCenterApi tests:
```bash
uv run pytest tests/test_decisioncentermanager.py::TestInvokeDecisionCenterApi -v
```

## Results
All 14 tests pass successfully ✅