from . import config

# Create a document in the collection with doc_values
def create_document_firestore(
    collection: str,
    doc_values: dict
):
    config.FIRESTORE_CLIENT.collection(collection).add(doc_values)

def create_firestore_index(
    collection_id: str,    
):
    parent = f'projects/{config.PROJECT_ID}/databases/(default)/collectionGroups/{collection_id}'
    index = {
        'name':'documents',
        'fields': [
            {'name':'blob_name'},{'name':'bucket_name'} 
        ]
    }
    return config.FIRESTORE_ADMIN.create_index(parent, index)
    
# Query all documents from collection, with filter
def get_all_documents_firebase(
    collection: str,
    field_name: str,
    filter_value: str,
    limit: int = 1
) -> dict:
    docs = config.FIRESTORE_CLIENT.collection(collection).where(
        field_name, u'==', filter_value).order_by(
            'creation_time').limit(limit).stream()
    response = {}

    for doc in docs:
        response[doc.id] = doc.to_dict()

    return response

# Get document content with blob_name
def get_document_firebase(
    collection: str,
    blob_name: str
) -> dict:
    doc = config.FIRESTORE_CLIENT.collection(collection).where(
            'blob_name', '==', blob_name).limit(1).get()
    
    return doc[0].to_dict() if doc else doc

# Get specific field from document in collection
def get_field_from_doc_firebase(
    collection: str,
    blob_name: str,
    field_name: str
) -> dict:
    doc_field = config.FIRESTORE_CLIENT.collection(collection).where(
            'blob_name', '==', blob_name).limit(1).get()

    return doc_field[0].get(field_name) if doc_field else doc_field

# Update a specific document field
def update_document_field_firebase(
    collection: str,
    blob_name: str,
    field_name: str,
    value: str
) -> bool:
    doc_id = config.FIRESTORE_CLIENT.collection(collection).where(
        'blob_name', '==', blob_name).limit(1).get()

    if doc_id:
        doc_ref = config.FIRESTORE_CLIENT.collection(
            'documents').document(doc_id[0].id)
        doc_ref.update({field_name:value})
        return True
    else:
        return False