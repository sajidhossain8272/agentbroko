import hashlib
import hmac
import struct

# Pure Python Bech32 implementation
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

def bech32_polymod(values):
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for p in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ p
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk

def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

def bech32_create_checksum(hrp, data, spec=1):
    values = bech32_hrp_expand(hrp) + data
    const = 1 if spec == 1 else 0x2bc830a3
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ const
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data, spec=1):
    combined = data + bech32_create_checksum(hrp, data, spec)
    return hrp + '1' + ''.join([CHARSET[d] for d in combined])

def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

# Base58Check encoding for Legacy/SegWit
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58_encode(raw):
    n = int.from_bytes(raw, 'big')
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(BASE58_ALPHABET[r])
    pad = 0
    for byte in raw:
        if byte == 0:
            pad += 1
        else:
            break
    return (BASE58_ALPHABET[0] * pad) + ''.join(reversed(res))

def base58_check_encode(prefix, payload):
    data = prefix + payload
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    return base58_encode(data + checksum)

def mnemonic_to_seed(mnemonic, passphrase=""):
    salt = ("mnemonic" + passphrase).encode('utf-8')
    return hashlib.pbkdf2_hmac('sha512', mnemonic.encode('utf-8'), salt, 2048)

def derive_master_key(seed):
    h = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return h[:32], h[32:]

def derive_child_key(parent_key, parent_chain, index):
    # Hardened index check
    if index >= 0x80000000:
        data = b'\x00' + parent_key + struct.pack('>I', index)
    else:
        # Simplification for public key derivation
        data = b'\x00' + parent_key + struct.pack('>I', index)
    h = hmac.new(parent_chain, data, hashlib.sha512).digest()
    return h[:32], h[32:]

def pubkey_hash_to_addresses(pubkey_bytes):
    # SHA256 + RIPEMD160
    sha = hashlib.sha256(pubkey_bytes).digest()
    h = hashlib.new('ripemd160', sha).digest()
    
    # 1. Native SegWit (bc1q...)
    words = [0] + convertbits(h, 8, 5)
    native_segwit = bech32_encode("bc", words)
    
    # 2. Legacy (1...)
    legacy = base58_check_encode(b'\x00', h)
    
    # 3. Nested SegWit (3...)
    redeem_script = b'\x00\x14' + h
    script_hash = hashlib.new('ripemd160', hashlib.sha256(redeem_script).digest()).digest()
    nested_segwit = base58_check_encode(b'\x05', script_hash)
    
    return {
        'native_segwit': native_segwit,
        'nested_segwit': nested_segwit,
        'legacy': legacy
    }
