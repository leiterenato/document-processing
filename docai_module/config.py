# General imports
from IPython.display import IFrame
import os
import requests
import datetime
import re

# Import Google Cloud client libraries
from google.cloud import firestore
from google.cloud import firestore_admin_v1
from google.cloud import storage
from google.cloud import documentai_v1beta3 as documentai
from google.cloud import dlp_v2
from google.cloud import language_v1

# Instantiate the clients
DLP_CLIENT = dlp_v2.DlpServiceClient()
FIRESTORE_CLIENT = firestore.Client()
FIRESTORE_ADMIN = firestore_admin_v1.FirestoreAdminClient()
DOCAI_CLIENT = documentai.DocumentProcessorServiceClient()
STORAGE_CLIENT = storage.Client.from_service_account_json('/home/jupyter/key.json')
NLP_CLIENT = language_v1.LanguageServiceClient()

# Global variables
DOCAI_LOCATION = 'us'
MIME_TYPE = 'application/pdf'
REGION_NAME = 'us-east1'
COLLECTION_ID = 'documents'

# Dynamically generated variables
SERVICE_ACCOUNT_ID = 'sa-geral'
FULL_SERVICE_ACCOUNT_ID = 'sa-geral@cool-ml-demos.iam.gserviceaccount.com'
PROJECT_ID = 'cool-ml-demos'
TEST_BUCKET = 'cool-ml-demos-test'
ORIGINAL_BUCKET = 'cool-ml-demos-original'
DOCAI_BUCKET = 'cool-ml-demos-docai'
DLP_BUCKET = 'cool-ml-demos-dlp'
PROCESSOR_ID = 'ff4bad3352769404'
