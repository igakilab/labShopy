import nfc
from binascii import hexlify

__nfctag = ""

def check_services(tag, start, n):
    services = [nfc.tag.tt3.ServiceCode(i >> 6, i & 0x3f)
                for i in xrange(start, start+n)]
    versions = tag.request_service(services)
    for i in xrange(n):
        if versions[i] == 0xffff: continue
        print services[i], versions[i]


def on_connect(tag):
    idm, pmm = tag.polling(system_code=0xFE00)
    tag.idm, tag.pmm, tag.sys = idm, pmm, 0xFE00
    print tag
#    global __nfctag
#    __nfctag = "hoge"
#    n = 32
#    check_services(tag, 0x1A8B, n)
    sc = nfc.tag.tt3.ServiceCode(106, 0x0b)  # 174B
    bc = nfc.tag.tt3.BlockCode(1, service=0)
    data = tag.read_without_encryption([sc], [bc])
    print 'str:', data.decode("shift-jis")
    print 'hex:', hexlify(data)

def nfcCheck():
    with nfc.ContactlessFrontend('usb') as clf:
        clf.connect(rdwr={'on-connect': on_connect})
    global __nfctag
    return __nfctag


if __name__ == '__main__':
    print nfcCheck()
