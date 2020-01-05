import pickle

from django.shortcuts import render, redirect
from django.http import HttpResponse
from PIL import Image

from script.HuffmanTree import HuffmanTree
from script.helper_functions import get_key, read_and_get_from_file
from . import forms


def create_tree_and_save_files(huffman_tree_obj):
    huffman_tree_obj.create_tree()
    key = get_key()
    compressed_file_data = huffman_tree_obj.get_compressed_file(key=key)
    meta_data = compressed_file_data[0]
    bit_array = compressed_file_data[1]

    with open(f'C:\\Users\\areeb\\Documents\\Programming\\Pycharm '
              f'Projects\\django_pied_piper\\media\\metadata\\'
              f'{key}.dat', 'wb') as fp:
        pickle.dump(meta_data, fp)

    with open(f'C:\\Users\\areeb\\Documents\\Programming\\Pycharm '
              f'Projects\\django_pied_piper\\media\\compressed'
              f'\\{key}.bin', 'wb') as fp:
        fp.write(bit_array)
    return f'{key}.bin'


def home_view(request):
    return render(request, 'huffman_coding/home.html')


def download_compressed_file_view(request, file_name):
    with open(f'C:\\Users\\areeb\\Documents\\Programming\\Pycharm '
              f'Projects\\django_pied_piper\\media\\compressed'
              f'\\{file_name}', 'rb') as fp:
        response = HttpResponse(fp.read(),
                                content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment;filename=compressed.bin'
        return response


def download_text_file_view(request, file_name):
    with open(f'C:\\Users\\areeb\\Documents\\Programming\\Pycharm '
              f'Projects\\django_pied_piper\\media\\temp'
              f'\\{file_name}', 'rb') as fp:
        response = HttpResponse(fp.read(), content_type='text/rtf')
        response['Content-Disposition'] = 'attachment;filename=decompressed.txt'
        return response


def download_image_file_view(request, file_name):
    with open(f'C:\\Users\\areeb\\Documents\\Programming\\Pycharm '
              f'Projects\\django_pied_piper\\media\\temp'
              f'\\{file_name}', 'rb') as fp:
        response = HttpResponse(fp.read(), content_type='image/bmp')
        response['Content-Disposition'] = 'attachment;filename=decompressed.bmp'
        return response


def text_compress_view(request):
    if request.method == 'POST':
        form = forms.TextFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = request.FILES['text_file']
            text = fp.read()
            text = str(text, 'utf-8')

            huffman_tree = HuffmanTree(data=text)
            file_name = create_tree_and_save_files(huffman_tree)
            return redirect('download-compressed-file', file_name)
    else:
        form = forms.TextFileForm()
    return render(request, 'huffman_coding/form.html', {'form': form})


def image_compress_view(request):
    if request.method == 'POST':
        form = forms.ImageFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = request.FILES['image_file']
            with open(
                    r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp.bmp',
                    'wb') as temp_fp:
                temp_fp.write(fp.read())
            huffman_tree = HuffmanTree(
                file_path=r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp.bmp',
                is_image=True)
            file_name = create_tree_and_save_files(huffman_tree)

            return redirect('download-compressed-file', file_name)

    else:
        form = forms.ImageFileForm()
    return render(request, 'huffman_coding/form.html', {'form': form})


def text_decompress_view(request):
    if request.method == 'POST':
        form = forms.BinaryFileForm(request.POST, request.FILES)
        if form.is_valid():
            fh = request.FILES['binary_file']
            with open(
                    r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp_b.bin',
                    'wb') as temp_fp:
                temp_fp.write(fh.read())
            compressed_file_data = read_and_get_from_file(file_path=r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp_b.bin')
            key = compressed_file_data['key']
            encoded_data = compressed_file_data['encoded_data']
            meta_data_file_name = f'{key}.dat'
            with open(f'C:\\Users\\areeb\\Documents\\Programming\\Pycharm '
                      f'Projects\\django_pied_piper\\media\\metadata'
                      f'\\{meta_data_file_name}', 'rb') as fp:
                meta_data = pickle.load(fp)

            huffman_tree = HuffmanTree(elements_dict=meta_data, is_decompression=True)
            huffman_tree.decompress(encoded_file_data=encoded_data)
            decoded_data = huffman_tree.decoded_data
            with open(
                    r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp_t.txt',
                    'w') as temp_fp:
                temp_fp.write(decoded_data)
            return redirect('download-text-file', 'temp_t.txt')

    else:
        form = forms.BinaryFileForm()
    return render(request, 'huffman_coding/form.html', {'form': form})


def image_decompress_view(request):
    if request.method == 'POST':
        form = forms.BinaryFileForm(request.POST, request.FILES)
        if form.is_valid():
            fh = request.FILES['binary_file']
            with open(
                    r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp_b.bin',
                    'wb') as temp_fp:
                temp_fp.write(fh.read())
            compressed_file_data = read_and_get_from_file(
                file_path=r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp_b.bin')
            key = compressed_file_data['key']
            encoded_data = compressed_file_data['encoded_data']
            meta_data_file_name = f'{key}.dat'
            with open(f'C:\\Users\\areeb\\Documents\\Programming\\Pycharm '
                      f'Projects\\django_pied_piper\\media\\metadata'
                      f'\\{meta_data_file_name}', 'rb') as fp:
                meta_data = pickle.load(fp)

            huffman_tree = HuffmanTree(elements_dict=meta_data,
                                       is_decompression=True,
                                       is_image=True)
            huffman_tree.decompress(encoded_file_data=encoded_data)
            decoded_image_data = huffman_tree.decoded_data
            image_size = huffman_tree.image_size

            new_image = Image.new('RGB', size=image_size)
            new_image.putdata(decoded_image_data)
            image_path = r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp_i.bmp'
            new_image.save(image_path)

            return redirect('download-image-file', 'temp_i.bmp')

    else:
        form = forms.BinaryFileForm()

    return render(request, 'huffman_coding/form.html', {'form': form})

