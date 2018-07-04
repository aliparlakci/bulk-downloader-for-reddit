class FileAlreadyExistsError(Exception):
    pass

class NotADownloadableLinkError(Exception):
    pass

class AlbumNotDownloadedCompletely(Exception):
    pass

class FileNameTooLong(Exception):
    pass