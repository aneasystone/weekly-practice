from pdf2zh.doclayout import OnnxModel

from pdf2zh import translate, translate_stream

params = {
    'lang_in': 'en',
    'lang_out': 'zh',
    'service': 'google',
    'thread': 4,
    'model': OnnxModel.load_available()
}

filepath = '/Users/aneasystone/Downloads/2504.08748v1/2504.08748v1.pdf'

# (file_mono, file_dual) = translate(files=[filepath], **params)[0]
# print(file_mono, file_dual)

with open(filepath, 'rb') as f:
    (stream_mono, stream_dual) = translate_stream(stream=f.read(), **params)
    with open('./dual.pdf', 'wb') as dual:
        dual.write(stream_dual)
