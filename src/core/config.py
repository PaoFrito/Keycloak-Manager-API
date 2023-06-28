import os

KEYCLOAK_URL = os.getenv('KEYCLOAK_URL', 'http://localhost:8080')
REALM_NAME = os.getenv('KEYCLOAK_REALM_NAME', 'realm') 
CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID', 'client_id') 
CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET', 'client_secret') 
ADMIN_CLIENT_ID = os.getenv('KEYCLOAK_ADMIN_CLIENT_ID', 'admin_client_id') 
ADMIN_CLIENT_SECRET = os.getenv('KEYCLOAK_ADM_CLIENT_SECRET', 'admin_client_secret')
API_URL = os.getenv('API_URL', 'http://localhost:8085') 
PROJECT_VERSION = os.getenv('PROJECT_VERSION', '0.0.1') 