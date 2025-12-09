#!/usr/bin/env python3
"""
lfsr.py - small CLI LFSR simulator for degree-4 LFSRs

Conventions:
 - State is (s3, s2, s1, s0) with s3 MSB, s0 LSB
 - taps are (p3, p2, p1, p0) for polynomial x^4 + p3*x^3 + p2*x^2 + p1*x + p0
 - feedback f = p3*s3 XOR p2*s2 XOR p1*s1 XOR p0*s0
 - update: (s3,s2,s1,s0) -> (f, s3, s2, s1)
 - default reported output bit is s0 (rightmost) before shifting
"""

import argparse
import sys
from typing import Tuple, List

def step(state: Tuple[int,int,int,int], taps: Tuple[int,int,int,int]) -> Tuple[int,int,int,int]:
    s3, s2, s1, s0 = state
    f = (s3 & taps[0]) ^ (s2 & taps[1]) ^ (s1 & taps[2]) ^ (s0 & taps[3])
    return (f, s3, s2, s1)

def lfsr_stream_bits(taps: Tuple[int,int,int,int], init: Tuple[int,int,int,int], N: int) -> List[int]:
    s = list(init)
    out = []
    for _ in range(N):
        out.append(s[3])  # output = s0
        s = list(step(tuple(s), taps))
    return out

def lfsr_stream_bytes(taps: Tuple[int,int,int,int], init: Tuple[int,int,int,int], nbytes: int) -> bytes:
    bits = lfsr_stream_bits(taps, init, nbytes*8)
    b_arr = bytearray()
    for i in range(nbytes):
        byte = 0
        for j in range(8):
            bit = bits[i*8 + j]
            byte = (byte << 1) | (bit & 1)
        b_arr.append(byte)
    return bytes(b_arr)

def state_to_int(state: Tuple[int,int,int,int]) -> int:
    s3,s2,s1,s0 = state
    return (s3<<3) | (s2<<2) | (s1<<1) | s0

def int_to_state(x: int) -> Tuple[int,int,int,int]:
    return ((x>>3)&1, (x>>2)&1, (x>>1)&1, x&1)

def find_cycles(taps: Tuple[int,int,int,int]):
    deg = 4
    seen_canon = {}
    cycles = []
    for i in range(1, 2**deg):  # skip all-zero
        init = int_to_state(i)
        seq = []
        seen = {}
        state = init
        idx = 0
        while state not in seen:
            seen[state] = idx
            seq.append(state)
            state = step(state, taps)
            idx += 1
        start = seen[state]
        cycle = seq[start:]
        # canonical rotation (smallest lexicographic rotation)
        rotations = []
        n = len(cycle)
        for k in range(n):
            rot = tuple(cycle[k:]+cycle[:k])
            rotations.append(rot)
        canon = min(rotations)
        if canon not in seen_canon:
            seen_canon[canon] = True
            cycles.append(list(cycle))
    # sort cycles by length
    cycles.sort(key=lambda c: (len(c), [state_to_int(s) for s in c]))
    return cycles

def parse_state(s: str) -> Tuple[int,int,int,int]:
    s = s.strip().lower()
    if s.startswith('0x'):
        v = int(s, 16)
    elif s.startswith('0b'):
        v = int(s, 2)
    else:
        v = int(s, 0)
    if not (0 <= v <= 0xF):
        raise ValueError("Initial state must be between 0x0 and 0xF")
    return int_to_state(v)

def parse_taps(s: str) -> Tuple[int,int,int,int]:
    parts = [p.strip() for p in s.split(',')]
    if len(parts) != 4:
        raise ValueError("Taps must be 4 comma-separated bits, e.g. 0,0,1,1")
    bits = tuple(int(x) & 1 for x in parts)
    return bits

def main(argv):
    parser = argparse.ArgumentParser(description="Degree-4 LFSR CLI simulator")
    parser.add_argument("--poly", choices=['a','b','c','custom'], default='a',
                        help="Choose polynomial: a (x^4+x+1), b (x^4+x^2+1), c (x^4+x^3+x^2+x+1), or custom")
    parser.add_argument("--taps", help="Custom taps p3,p2,p1,p0 (comma separated), e.g. 0,1,0,1")
    parser.add_argument("--init", default="0x1", help="Initial state (hex like 0x8 or binary 0b1011 or decimal 9). Default 0x1")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bits", type=int, help="Number of output bits to print")
    group.add_argument("--bytes", type=int, help="Number of output bytes to print (packed MSB first per byte)")
    parser.add_argument("--show-cycles", action="store_true", help="List all nonzero cycles (states and s0 output)")
    parser.add_argument("--outbit", choices=['s0','s1','s2','s3'], default='s0', help="Which state bit to treat as output (default s0)")
    args = parser.parse_args(argv)

    if args.poly == 'a':
        taps = (0,0,1,1)  # x^4 + x + 1
    elif args.poly == 'b':
        taps = (0,1,0,1)  # x^4 + x^2 + 1
    elif args.poly == 'c':
        taps = (1,1,1,1)  # x^4 + x^3 + x^2 + x + 1
    else:
        if not args.taps:
            parser.error("--poly custom requires --taps p3,p2,p1,p0")
        taps = parse_taps(args.taps)

    try:
        init_state = parse_state(args.init)
    except Exception as e:
        parser.error("Bad --init: " + str(e))

    # optionally print cycles
    if args.show_cycles:
        cycles = find_cycles(taps)
        print(f"Polynomial taps (p3,p2,p1,p0) = {taps}")
        print(f"Found {len(cycles)} nonzero cycle(s), total nonzero states = {sum(len(c) for c in cycles)} (should be 15)\n")
        for idx, cyc in enumerate(cycles, 1):
            hex_states = [f"0x{state_to_int(s):X}" for s in cyc]
            outs = "".join(str(s[3]) for s in cyc)  # s0 outputs
            print(f"Cycle {idx}: length {len(cyc)}")
            print(" States (hex):", ", ".join(hex_states))
            print(" Output s0 sequence:", outs)
            print("-"*40)
        # if only showing cycles, exit
        if not (args.bits or args.bytes):
            return

    # produce output bits/bytes
    if args.bits:
        # produce bits but allow selecting a different output bit
        bits = []
        s = list(init_state)
        out_index = {'s0':3, 's1':2, 's2':1, 's3':0}[args.outbit]
        for _ in range(args.bits):
            bits.append(str(s[out_index]))
            s = list(step(tuple(s), taps))
        print("".join(bits))
        return

    if args.bytes:
        data = lfsr_stream_bytes(taps, init_state, args.bytes)
        # print bytes in hex and also raw if printable
        print("Hex bytes:", data.hex())
        try:
            text = data.decode('ascii', errors='replace')
            print("ASCII (with replacements):", text)
        except Exception:
            pass
        return

    # default: if no bits/bytes specified, print some info and first 64 bits
    bits = lfsr_stream_bits(taps, init_state, 15)
    print(f"Taps (p3,p2,p1,p0) = {taps}")
    print(f"Initial state (s3..s0) = {init_state}")
    print("First 15 output bits (s0 each clock):")
    print("".join(str(b) for b in bits))

if __name__ == "__main__":
    main(sys.argv[1:])
