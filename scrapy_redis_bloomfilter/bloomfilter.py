class Hash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed
    
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, server, key, blockNum=1):
        self.size = 1 << 31
        self.seeds = [5, 7, 11, 13, 31]
        self.server = server
        self.key = key
        self.blockNum = blockNum
        self.hashes = []
        for seed in self.seeds:
            self.hashes.append(Hash(self.size, seed))
    
    def contains(self, value):
        if not value:
            return False
        ret = True
        
        name = self.key + str(int(value[0:2], 16) % self.blockNum)
        for f in self.hashes:
            loc = f.hash(value)
            ret = ret & self.server.getbit(name, loc)
        return ret
    
    def insert(self, value):
        name = self.key + str(int(value[0:2], 16) % self.blockNum)
        for f in self.hashes:
            loc = f.hash(value)
            self.server.setbit(name, loc, 1)


from redis import StrictRedis

server = StrictRedis(host='localhost', port=6379, db=1, password='foobared')
key = 'baidu'
filter = BloomFilter(server=server, key=key)
filter.insert('1')
result = filter.contains('1')
print(result)
