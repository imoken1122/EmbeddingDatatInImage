import argparse
import struct
def SearchChank(data,isText):
    offset = 33
    while 1:
        length = struct.unpack_from(">I", data, offset) 
        ctype = struct.unpack_from(">4s", data, offset + 4)
        if ctype[0] == b"MOMO":
            length = struct.unpack_from(">I", data, offset) 
            if isText:
                EmbedingTextExtractor(data,length,offset)       
            else:
                EmbeddingFileExtractor( data, length, offset)

        elif ctype[0] == b"IEND": 
            print("find IEND tag")
            break
       
        offset += length[0]+12

def EmbedingTextExtractor(data,length, offset):

    print("A secret message was found !! ")
    print(struct.unpack_from(f">{length[0]}s", data, offset+8)[0].decode())

     
def EmbeddingFileExtractor(data,length,offset):
    print("zipfile was found !!")
    zip_binary = struct.unpack_from(f">{length[0]}s", data, offset+8)[0] 
    with open("output.zip", "wb") as f:
        f.write(zip_binary)

def ImageInfoAnalyser(data):
    signature = struct.unpack_from(">8c", data, 0)
    offset = 8

    while 1:

        length = struct.unpack_from(">I", data, offset) 
        ctype = struct.unpack_from(">4s", data, offset + 4)

        if ctype[0] == b"IEND": 
            print("find IEND tag")
            break
        
        image_info_dic[ctype] = [length]


        if ctype[0] == b"IHDR":
            #Data = struct.unpack_from(">13c",offset+8)
            width = struct.unpack_from(">I", data, offset + 8)
            height = struct.unpack_from(">I", data, offset + 12)
            bitDepth = struct.unpack_from(">B", data, offset +16)
            crc = struct.unpack_from(">I", data, offset + 21)

            offset += 25
        else:

            offset += length[0]+12

        print(f"\n[{ctype[0]}] \n length:{length[0]}\n offset:{offset}")

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("-t", action='store_true')
    arg.add_argument("-in","--input_image",default = "image.png")
    args = arg.parse_args()

    data = open(args.input_image, "rb").read()
    SearchChank(data,args.t)
if __name__ == "__main__":
    main()