class ChunkWriter:
    def __init__(self):
        self.buffer_list = []
        self.offset_list = []
        self.length_list = []

    def write_int(self, num: int):
        v = num & 0xFFFFFFFF

        buf = bytearray(10) 
        offset = 9 
        length = 0

        while v >= 0x80:
            if length == 0:
                buf[offset] = (v & 0x7F).to_bytes(1, byteorder='big')[0] 
            else:
                buf[offset] = ((v & 0x7F) | 0x80).to_bytes(1, byteorder='big')[0]
            v >>= 7
            length += 1
            offset -= 1

        if length == 0:
            buf[9] = v.to_bytes(1, byteorder='big')[0] 
        else:
            buf[9 - length] = (v | 0x80).to_bytes(1, byteorder='big')[0]

        length += 1
        self.buffer_list.append(buf)
        self.offset_list.append(offset)
        self.length_list.append(length)

    def write_str(self, val: str):
        s = val.encode()
        self.write_int(len(s))
        self.buffer_list.append(s)
        self.offset_list.append(0)
        self.length_list.append(len(s))

    def close(self) -> bytes:
        total = sum(self.length_list)
        out = bytearray(total)
        pos = 0

        for buf, off, length in zip(self.buffer_list, self.offset_list, self.length_list):
            out[pos:pos+length] = buf[off:off+length]
            pos += length

        return bytes(out)
