import pickle

from django.shortcuts import render, redirect
from PIL import Image

from script.HuffmanTree import HuffmanTree
from script.helper_functions import get_key
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


def home_view(request):
    return render(request, 'huffman_coding/home.html')


def text_compress_view(request):
    if request.method == 'POST':
        form = forms.TextFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = request.FILES['text_file']
            text = fp.read()
            text = str(text, 'utf-8')

            huffman_tree = HuffmanTree(data=text)
            create_tree_and_save_files(huffman_tree)

            # TODO: redirect to file download page
            return redirect('home')
    else:
        form = forms.TextFileForm()
    return render(request, 'huffman_coding/compress.html', {'form': form})


def image_compress_view(request):
    if request.method == 'POST':
        form = forms.ImageFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = request.FILES['image_file']
            with open(r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp.bmp', 'wb') as temp_fp:
                temp_fp.write(fp.read())
            huffman_tree = HuffmanTree(file_path=r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\temp\temp.bmp', is_image=True)
            create_tree_and_save_files(huffman_tree)

            # TODO: redirect to file download page
            return redirect('home')
    else:
        form = forms.ImageFileForm()
    return render(request, 'huffman_coding/compress.html', {'form': form})
