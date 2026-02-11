class ChunkReader:
    def __init__(self, arr: bytes):
        self.arr=arr
        self.offset=0

    def read_int(self):
        num=0
        v= self.arr[self.offset]
        self.offset+=1
        while v >= 0x80:
            num = (num << 7) + (v & 0x7F)
            v = self.arr[self.offset]
            self.offset+=1
        num = (num << 7) + v
        if num>2**31:
            num=num-2**32
        return num
    
    def read_str(self):
        len=self.read_int()
        if len<0:
            return None
        val= self.arr[self.offset : (self.offset + len)].decode("utf-8")
        self.offset+=len
        return val
