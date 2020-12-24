
from os import write
import struct
import binascii
from PIL import Image
import argparse
def CreateMyChank(text,isText):
    add_chank = b""

    if isText:
        emb_text = text.encode()
    else:
        emb_text = text

    length = len(emb_text).to_bytes(4,"big") # data length 4bytes
    type = b"MOMO" # Any ctype_name 4bytes

    add_chank += length+type+emb_text
    add_chank += binascii.crc32(add_chank).to_bytes(4,"big") #crc 4bytes
    return add_chank

def EmbeddingTextToImage_ChankSeperate(data,text, output_name,isText):
    png_bainary = b""
    #add header
    png_bainary = struct.unpack_from(">8s", data, 0)[0] # header 8bytes

    offset = 8 
    #
    png_bainary += struct.unpack_from(f">25s", data, offset)[0] # IHDR chank 25bytes

    offset += 25

    # IDAT chank separerate
    while 1:

        ctype = struct.unpack_from(">4s", data, offset + 4) #ctype 4byte
        if ctype[0] == b"IEND": 
            break

        length = struct.unpack_from(">I", data, offset) # data length is 4bytes

        png_bainary += struct.unpack_from(f">{length[0]+12}s", data, offset)[0] #add IDAT chank 12bytes + data length
        offset += length[0]+12 

    png_bainary += CreateMyChank(text,isText) #add mychank
    png_bainary += struct.unpack_from(">12s", data, offset)[0] # add IEND chank  12bytes


    with open(f"{output_name}","wb") as f: #save
        f.write(png_bainary)
    print("embbeding message was successfully!!")


def EmbeddingTextToImage_Simply(data,text,output_name,isText):
    png_bainary = data[:-12] # until IEND chank
    png_bainary += CreateMyChank(text,isText) #add my chank
    png_bainary += data[-12:] # add IEND chank

    with open(f"{output_name}","wb") as f:
        f.write(png_bainary)
    print("embbeding message was successfully!!")

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("-t", action='store_true')
    arg.add_argument("-in","--input_image",default = "image.png")
    arg.add_argument("-on", "--output_image",default= "embed_text_image.png")
    args = arg.parse_args()

    if args.t:
        input_text = "test"
    else:
        input_text = open("input.zip","rb").read()

    data = open(args.input_image, "rb").read()
    EmbeddingTextToImage_Simply(data,input_text,args.output_image,args.t)   
if __name__ == "__main__":
    main()