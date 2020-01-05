from os import listdir

from bitarray import bitarray


def get_key():
    """Get key based on file names in meta_data folder"""
    files_list = listdir(r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\metadata')

    for i in range(0, 255):
        name = f'{i}.dat'

        if not files_list.__contains__(name):
            return i


def read_and_get_from_file(file_path):
    """Reads data from file and returns the dict with encoded_data $ key"""
    bit_array = bitarray()
    with open(file_path, 'rb') as fp:
        # noinspection PyArgumentList
        bit_array.fromfile(fp)
    key = bit_array[:8]
    key = int(key.to01(), 2)  # Converting key from bitarray to int
    binary_presentation = bit_array[8:]
    binary_presentation_length = len(binary_presentation)
    binary_presentation.tobytes()
    byte_presentation_int = int.from_bytes(binary_presentation,
                                           byteorder='big',
                                           signed=False)
    encoded_data = bin(byte_presentation_int)[2:]
    significant_bits_length = binary_presentation_length - len(
        encoded_data)
    significant_bits = '0' * significant_bits_length
    encoded_data = significant_bits + encoded_data
    return {'key': key, 'encoded_data': encoded_data}
