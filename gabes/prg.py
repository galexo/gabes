from Crypto.Cipher import AES
from Crypto.Util import Counter

class SeedPRG:
    """AES-CTR PRG that returns as many bytes as you ask for, replayable from seed."""
    def __init__(self, seed: bytes):
        assert len(seed) in (16, 24, 32)   # 128/192/256-bit AES keys
        self._cipher = AES.new(seed, AES.MODE_CTR,
                               counter=Counter.new(128, initial_value=0))
    def randbytes(self, n: int) -> bytes:
        return self._cipher.encrypt(b'\x00' * n)   # encrypting zeros yields the keystream
    def randint(self, bits: int) -> int:
        length = (bits + 7) // 8
        return int.from_bytes(self.randbytes(length), 'big') & ((1 << bits) - 1)
    
    def choice(self, seq):
        """Return a random element from the non-empty sequence seq."""
        if not seq:
            raise IndexError("Cannot choose from an empty sequence")
        idx = self.randint(seq.__len__().bit_length())
        idx = idx % len(seq)
        return seq[idx]