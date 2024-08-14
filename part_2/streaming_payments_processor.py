import tempfile
import os

def get_payments_storage():
    """
    @returns an instance of io.BufferedWriter using a temporary file.
    """
    temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False)
    return temp_file

class ChecksumStorage:
    def __init__(self, storage):
        self.storage = storage
        self.checksum = 0

    def write(self, data):
        self.checksum += sum(data)
        self.storage.write(data)

    def flush(self):
        self.storage.flush()

    def close(self):
        self.storage.close()
        os.remove(self.storage.name)

def stream_payments_to_storage(storage):
    """
    Simulates streaming payments to the given storage.
    This function will write some example data to the storage.
    """
    for i in range(10):
        storage.write(bytes([1, 2, 3, 4, 5]))

def process_payments():
    temp_storage = get_payments_storage()
    checksum_storage = ChecksumStorage(temp_storage)

    stream_payments_to_storage(checksum_storage)

    print(checksum_storage.checksum)

    checksum_storage.close()

process_payments()
