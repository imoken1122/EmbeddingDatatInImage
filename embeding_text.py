
from os import write
import struct
import binascii
from PIL import Image
import argparse


def CreateMyChank(text):
    add_chank = b""
    length = len(text.encode()).to_bytes(4,"big")
    type = b"MOMO" # Any name
    emb_text = text.encode()
    add_chank += length+type+emb_text
    add_chank += binascii.crc32(add_chank).to_bytes(4,"big")
    return add_chank

def EmbeddingTextToImage(data,text):
    png_bainary = b""
    #add header
    png_bainary = struct.unpack_from(">8s", data, 0)[0]

    offset = 8
    #
    png_bainary += struct.unpack_from(f">25s", data, offset)[0]

    offset += 25

    while 1:

        ctype = struct.unpack_from(">4s", data, offset + 4)
        if ctype[0] == b"IEND": 
            break

        length = struct.unpack_from(">I", data, offset)

        png_bainary += struct.unpack_from(f">{length[0]+12}s", data, offset)[0]
        offset += length[0]+12

    png_bainary += CreateMyChank(text)
    png_bainary += struct.unpack_from(">12s", data, offset)[0]

    with open("image_from_str2.png","wb") as f:
        f.write(png_bainary)
    print("embbeding message was successfully!!")

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("-t","--input_text",default = "テスト")
    arg.add_argument("-img","--input_image",default = "image.png")
    arg.add_argument("-n","--output_name",default= "embed_text_image.png")
    args = arg.parse_args()
    print(args)

    data = open(args.input_image, "rb").read()
    EmbeddingTextToImage(data,args.input_text,args.output_name)   
if __name__ == "__main__":
    main()