# Document Processing with Google Cloud machine learning APIs

## Abstract
Many customers have to deal with a lot of unstructured data like PDFs, scanned documents, photos, etc., and it is difficult to understand and get insights from the content of these documents. This design doc proposes an architecture to process these documents at scale using machine learning APIs in Google Cloud. Three versions of this architecture are provided to give more flexibility for customers to implement it.

## Business Objectives and Impact
Capturing unstructured data from PDFs, photos, emails, etc., has been an expensive, time-consuming and error-prone process requiring manual data entry. Today, AI and machine learning have made great advances towards automating this process, enabling businesses to derive insights from, and take advantage of, this data that had been previously untapped. Google Cloud ready-to-use APIs, like Document AI and DLP, uses advanced machine learning techniques to extract data and insights from these files. 
By implementing this architecture, many enterprises can optimize their processes by reducing the errors associated with manual data collection, reducing the time to process these documents (from days to seconds) and making these data available to extract insights.

## Customer Journey - High level overview
The flow starts with an end user or a system uploading a document (PDF for example) to a bucket in Cloud Storage. The document will be processed by three different Google Cloud APIs: Document AI (extract all the information in a structured way from the document), Data Loss Prevention (anonymize all sensitive information) and Natural Language API (extract entities and information from the document). These Google Cloud APIs will work asynchronously and the management API will store the status of its execution in the Firestore database. The requests are handled by a management API which acts as a hub for the services.
As soon as the API finishes processing the document, the results are stored in Cloud Storage for future reference. Additionally, a second layer of processing is implemented to process the results in order to visualize the data. The user, or a system, can query the results of this processing flow at any time by invoking the management API.

## Business Requirements
The following are business requirements:
 - Extract text, forms, tables and key/value pair from documents (PDF and TIFF).
 - Extract information from the document by classifying  the documents according to its content and identifying entities.
 - Identify and redact any sensitive information (PII) like passport number, social security number, address, etc.
 - Store this information for a long period of time for audit purposes
 - Dashboard with important information from the results of these documents.
 
