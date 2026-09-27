from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATED_SUCCESS="file_validated successfully"
    FILE_TYPE_NOT_SUPPORTED="file type not supported"
    FILE_SIZE_EXCEEDED="file size exceeded"
    FIILE_UPLOAD_FAILED="file upload failed"
    