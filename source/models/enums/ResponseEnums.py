from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATED_SUCCESS="file validated successfully"
    FILE_TYPE_NOT_SUPPORTED="file type not supported"
    FILE_SIZE_EXCEEDED="file size exceeded"
    FIILE_UPLOAD_FAILED="file upload failed"
    PROCESSING_SUCCESS="processs success"
    PROCESSING_FAILED="processs failed"