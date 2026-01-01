from enum import Enum


class ResponseSignal(Enum):

    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    MAX_FILE_SIZE_EXCEEDED = "max_file_size_exceeded"
    FILE_UPLOADED_SUCCESSFULLY = "file_uploaded_successfully"
    FILE_VALIDATED_SUCCESSFULLY = "file_validated_successfully"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    FILE_PROCESSING_FAILED = "file_processing_failed"
    FILE_PROCESSED_SUCCESSFULLY = "file_processed_successfully"