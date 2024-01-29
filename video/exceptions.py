class InvalidFilenameException(Exception):
    """Raised when an invalid filename is passed"""

    def __init__(self, message="Invalid filename"):
        self.message = message
        super().__init__(self.message)


class NotConnectedToNasException(Exception):
    """Raised when server is not connected to NAS"""

    def __init__(self, message="Failed to mount NAS drive"):
        self.message = message
        super().__init__(self.message)


class FileCouldNotBeOpened(Exception):
    """Raised when a possibly damaged or corrupt file could not be opened"""

    def __init__(self, message="Could not read the video, file might be damaged or corrupted"):
        self.message = message
        super().__init__(self.message)
