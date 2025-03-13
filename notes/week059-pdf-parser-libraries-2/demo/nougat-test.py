# pip install nougat-ocr
# https://github.com/facebookresearch/nougat

# nougat ./pdfs/4.pdf -o ./output
# nougat ./pdfs/3-img.pdf -o ./output

# 
# /usr/local/lib/python3.13/site-packages/nougat/transforms.py:158: UserWarning: 1 validation error for InitSchema
# compression_type
#   Input should be 'jpeg' or 'webp' [type=literal_error, input_value=95, input_type=int]
#     For further information visit https://errors.pydantic.dev/2.10/v/literal_error
#   alb.ImageCompression(95, p=0.07),
# Traceback (most recent call last):
#   File "/usr/local/bin/nougat", line 5, in <module>
#     from predict import main
#   File "/usr/local/lib/python3.13/site-packages/predict.py", line 18, in <module>
#     from nougat import NougatModel
#   File "/usr/local/lib/python3.13/site-packages/nougat/__init__.py", line 7, in <module>
#     from .model import NougatConfig, NougatModel
#   File "/usr/local/lib/python3.13/site-packages/nougat/model.py", line 34, in <module>
#     from nougat.transforms import train_transform, test_transform
#   File "/usr/local/lib/python3.13/site-packages/nougat/transforms.py", line 158, in <module>
#     alb.ImageCompression(95, p=0.07),
#     ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
#   File "/usr/local/lib/python3.13/site-packages/albumentations/core/validation.py", line 48, in custom_init
#     config = dct["InitSchema"]()
#   File "/usr/local/lib/python3.13/site-packages/pydantic/main.py", line 214, in __init__
#     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
# pydantic_core._pydantic_core.ValidationError: 3 validation errors for InitSchema
#
# pip install albumentations==1.0
#

#
# TypeError: BARTDecoder.prepare_inputs_for_inference() got an unexpected keyword argument 'cache_position'
#
# pip install transformers==4.38.2
#