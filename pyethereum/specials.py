import utils
import bitcoin


def proc_ecrecover(block, tx, msg):
    if msg.gas < 500:
        return 0, 0, []
    indata = msg.data + '\x00' * 128
    h = indata[:32]
    v = utils.big_endian_to_int(indata[32:64])
    r = utils.big_endian_to_int(indata[64:96])
    s = utils.big_endian_to_int(indata[96:128])
    pub = bitcoin.encode_pubkey(bitcoin.ecdsa_raw_recover(h, (v, r, s)), 'bin')
    o = [0] * 12 + [ord(x) for x in utils.sha3(pub[1:])[-20:]]
    return 1, msg.gas - 500, o


def proc_sha256(block, tx, msg):
    if msg.gas < 100:
        return 0, 0, []
    o = [ord(x) for x in bitcoin.bin_sha256(msg.data)]
    return 1, msg.gas - 100, o


def proc_ripemd160(block, tx, msg):
    if msg.gas < 100:
        return 0, 0, []
    o = [0] * 12 + [ord(x) for x in bitcoin.bin_ripemd160(msg.data)]
    return 1, msg.gas - 100, o

specials = {
    '0000000000000000000000000000000000000001': proc_ecrecover,
    '0000000000000000000000000000000000000002': proc_sha256,
    '0000000000000000000000000000000000000003': proc_ripemd160,
}