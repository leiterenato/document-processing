from . import config

def online_process_document(file_path: str, mime_type: str):
    # The full resource name of the processor
    name = f"projects/{config.PROJECT_ID}/locations/{config.DOCAI_LOCATION}/processors/{config.PROCESSOR_ID}"

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Read the file into memory and configure the process request
    document = {"content": image_content, "mime_type": mime_type}
    request = {"name": name, "document": document}

    # Recognizes text entities in the PDF document
    return config.DOCAI_CLIENT.process_document(request=request)

# Print the result from document ai api call
def print_doc_result(document: config.documentai.types.document.Document):
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = _get_text(form_field.field_name, document)
            field_value = _get_text(form_field.field_value, document)
            print("Extracted key value pair:")
            print(f"\t{field_name} {field_value}")
        for paragraph in document.pages:
            paragraph_text = _get_text(paragraph.layout, document)
            print(f"Paragraph text:\n{paragraph_text}")

# Extract shards from the text field
def _get_text(doc_element: dict, document: dict):
    """
    Document AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response

# Process a document async
def async_process_document(
    gcs_input_uri: str,
    gcs_output_uri: str,
    gcs_output_uri_prefix: str,
    mime_type: str
) -> str:
    # 'mime_type' can be 'application/pdf', 'image/tiff',
    # and 'image/gif', or 'application/json'
    service = config.documentai.types.document_processor_service
    input_config = service.BatchProcessRequest.BatchInputConfig(
        gcs_source=gcs_input_uri, mime_type=mime_type
    )

    # Where to write results
    destination_uri = f'{gcs_output_uri}/{gcs_output_uri_prefix}/'
    output_config = service.BatchProcessRequest.BatchOutputConfig(
        gcs_destination=destination_uri
    )

    # Call Processor to process document
    name = f"projects/{config.PROJECT_ID}/locations/{config.DOCAI_LOCATION}/processors/{config.PROCESSOR_ID}"
    request = service.BatchProcessRequest(
        name=name,
        input_configs=[input_config],
        output_config=output_config,
    )
    operation = config.DOCAI_CLIENT.batch_process_documents(request)

    return operation

# def _convert_pdf_image(blob_name: str):
#     # storage_client.download_as_bytes(
#     # convert_from_bytes

#     try:
#         # Download original file from bucket
#         pdf_bytes = cloud_storage_methods._download_blob_bytes(
#             config.BUCKET_SIGNED_URL_ORIGINAL,
#             'original/' + blob_name
#         )
#     except NotFound as e:
#         return str(e), 400
#     else:
#         # Convert PDF to image JPEG
#         images = convert_from_bytes(pdf_bytes)
        
#         files_data = {}

#         # If there are converted images
#         if len(file_images):
#             # Copy first image and generate a thumbnail
#             thumbnail = file_images[0].copy()
#             thumbnail.thumbnail(thumbnail_size)
#             thumbnail_name = f'thumbnail-{blob_name}.jpeg'

#             with BytesIO() as output:
#                 thumbnail.save(output, 'JPEG')
#                 files_data[thumbnail_name] = output.getvalue()

#             # Save all images as JPEG
#             for i, image in enumerate(images):
#                 filename = f'{blob_name}-{i}.jpeg'
#                 with BytesIO() as output:
#                     image.save(output, 'JPEG')
#                     files_data[filename] = output.getvalue()

#             # Upload files to cloud storage
#             for key, value in files_data.itens():
#                 cloud_storage_methods._upload_blob_bytes(
#                     config.BUCKET_SIGNED_URL_DOC_IMAGE,
#                     value,
#                     f'images/{blob_name}/{key}',
#                     'image/jpeg'
#                 )

#             # Update metadata to Firestore
#             firestore_methods._update_document_field_firebase(
#                 config.COLLECTION_DOCUMENTS,
#                 blob_name,
#                 'images',
#                 [f'/images/{blob_name}/{key}' for key in files_data.keys()]
#             )

#             firestore_methods._update_document_field_firebase(
#                 config.COLLECTION_DOCUMENTS,
#                 blob_name,
#                 'images_bucket',
#                 config.BUCKET_SIGNED_URL_DOC_IMAGE
#             )
#             return 'Document convertion finished', 200
#         else:
#             return 'No images to be processed', 200