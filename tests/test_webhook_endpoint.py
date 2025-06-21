import pytest
from unittest.mock import MagicMock, patch

# We'll need to patch FastAPI and the whatsapp_response module
# Since webhook_endpoint.py directly imports these at the top level,
# we need to ensure our mocks are in place *before* webhook_endpoint.py is imported.

@pytest.fixture
def mock_fastapi_and_router():
    with patch('fastapi.FastAPI') as mock_fastapi_class,
         patch('whatsapp_response.whatsapp_router') as mock_whatsapp_router:
        
        # Create a mock instance for FastAPI
        mock_app_instance = MagicMock()
        mock_fastape_class.return_value = mock_app_instance

        # Import webhook_endpoint.py *after* patching
        # This ensures that when webhook_endpoint.py runs, it uses our mocks
        import webhook_endpoint

        yield mock_app_instance, mock_whatsapp_router, webhook_endpoint


def test_fastapi_app_initialization(mock_fastapi_and_router):
    mock_app_instance, _, _ = mock_fastapi_and_router
    mock_app_instance.assert_called_once() # Verify FastAPI() was called

def test_whatsapp_router_included(mock_fastapi_and_router):
    mock_app_instance, mock_whatsapp_router, _ = mock_fastapi_and_router
    mock_app_instance.include_router.assert_called_once_with(mock_whatsapp_router)

# Optional: Test for direct app object exposure if it's used elsewhere
def test_app_object_exists(mock_fastapi_and_router):
    mock_app_instance, _, webhook_endpoint = mock_fastapi_and_router
    assert webhook_endpoint.app is mock_app_instance