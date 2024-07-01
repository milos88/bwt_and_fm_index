import sys
import argparse
from bwt_all import read_fasta, bwtViaSa, create_fm_index, search_classic, search_optimized
sys.setrecursionlimit(10**6)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", help="Path to the input fasta file", type=str)
    parser.add_argument("--sa-skip", help="fraction of rows kept in SA", type=int, default=32)
    parser.add_argument("--tally-skip", help="fraction of rows kept in Tally structure", type=int, default=128)
    parser.add_argument("--patterns", help="Patterns for searching", nargs="+")
    args = parser.parse_args()
    name = args.input_file

    with open(name) as fp:
        for _, seq in read_fasta(fp):
            input_str = seq.upper()
            input_str = input_str[:20000]+"$"

    skip = args.tally_skip
    k = args.sa_skip # fraction of rows kept in SA
    target_strs = list(args.patterns)# ["ATGCATG", "TCTCTCTA", "TTCACTACTCTCA"]
    bwt, sa = bwtViaSa(input_str)
    partial_sa = {i: si for i, si in enumerate(sa) if si % k == 0}
    bwt_len = len(bwt)
    C, occ = create_fm_index(bwt, skip)

    print(f"Searching patterns inside {name.split("/")[-1]} file")
    for target_str in target_strs:
        
        print(f"Performance for pattern {target_str}")
        print("Classic algorithm\n============================================")
        search_classic(input_str, target_str, bwt, sa)
        
        print("Optimized algorithm\n============================================")
        search_optimized(bwt, C, occ, skip, bwt_len, target_str, partial_sa)
        print("\n")