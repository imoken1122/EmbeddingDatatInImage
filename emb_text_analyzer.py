import argparse
import struct
def EmbedingTextAnalyser(data):

    offset = 33
    while 1:
        length = struct.unpack_from(">I", data, offset) 
        ctype = struct.unpack_from(">4s", data, offset + 4)

        if ctype[0] == b"MOMO":
            length = struct.unpack_from(">I", data, offset) 
            print("A secret message was found !! ")
            print(struct.unpack_from(f">{length[0]}s", data, offset+8)[0].decode())
            break
        elif ctype[0] == b"IEND": 
            print("find IEND tag")
            break
       

        offset += length[0]+12

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
    arg.add_argument("-img","--input_image",default = "image.png")
    args = arg.parse_args()

    data = open(args.input_image, "rb").read()
    EmbedingTextAnalyser(data)
if __name__ == "__main__":
    main()