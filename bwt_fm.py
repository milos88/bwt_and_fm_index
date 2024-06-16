def suffixArray(s):
    """ Given T return suffix array SA(T).  We use Python's sorted
        function here for simplicity, but we can do better. """
    satups = sorted([(s[i:], i) for i in range(len(s))])
    # Extract and return just the offsets
    return map(lambda x: x[1], satups)

def bwtViaSa(t):
    """ Given T, returns BWT(T) by way of the suffix array. """
    bw = []
    sa = list(suffixArray(t))
    for si in sa:
        if si == 0: bw.append('$')
        else: bw.append(t[si-1])
    return ''.join(bw), list(sa)

def calculate_checkpoint(pos, c, l, occ, skip, bwt_len):
    remainder = (pos - 1) % skip
    index = int((pos - 1) / skip)
    if remainder == 0:
        occ_pos = occ[c][index]
    else:
        if remainder > skip - remainder and (index + 1) * skip < bwt_len:
            occ_pos = occ[c][index + 1]
            for i in range((index + 1) * skip, pos - 1 - 1, -1):
                if l[i] == c:
                    occ_pos -=1
        else:
            occ_pos = occ[c][index]
            for i in range(index * skip + 1, pos, 1):
                if l[i] == c:
                    occ_pos += 1
    
    return occ_pos

def update_range(l, c, C, occ, skip, bwt_len, start=None, end=None):
    keys = list(C.keys())
    index = keys.index(c) + 1
    end_next_c = C[keys[index]] if index < len(keys) else bwt_len

    if start and end:
        occ_start = calculate_checkpoint(start, c, l, occ, skip, bwt_len)
        occ_end = calculate_checkpoint(end, c, l, occ, skip, bwt_len)

    start = C[c] + (occ_start if start else 0)
    end = C[c] + occ_end if end else end_next_c

    return start, end

def find_positions(l, C, occ, skip, bwt_len, p, sa):

    c = p[-1]
    start, end = update_range(l, c, C, occ, skip, bwt_len)
    for i in range(len(p) - 2, -1, -1):
        c = p[i]
        start, end = update_range(l, c, C, occ, skip, bwt_len, start, end)
        
        if start > end:
            return None # there is no patern p in input text
    pos = [sa[i] for i in range(start, end, 1)]

    return pos

def create_fm_index(bwt, skip):
    C = {} # dict to save position of first character in F array
    occ = {} # dict to save the number of occurrences of a character up to a given position in the BWT string.
    pos = 0
    for c in sorted(set(bwt)):
        C[c] = pos
        pos += bwt.count(c)
        occ[c] = [0] * (int(len(bwt) / skip) + 1)
    
    for i in range(int(len(bwt) / skip) + 1):
        if i == 0:
            char = bwt[i]
            for key in occ.keys():
                occ[key][i] = 1 if key == char else 0
            continue
        for j in range(1, skip + 1):
            if (i - 1) * skip + j >= len(bwt):
                break
            char = bwt[(i - 1) * skip + j]
            for key in occ.keys():
                if j == 1:
                    occ[key][i] = occ[key][i - 1] + (1 if key == char else 0)
                else:
                    occ[key][i] += 1 if key == char else 0
    return C, occ

if __name__=="__main__":
    text = "ATGCGTACGTTAGCTAGCGTACGATCGATCGTAGCTAGCGTACGATCGTAGCTAGCGTACGATCGTAGCCGATCGTAGCTAGCGTACGATCGTAGCTAGCGTACGATCGTAGCTAGCGTACGATCGTAGCTAGCGTACCGATCGTAGCTAGCGTACGATCGTAGCTAGCGTACGATCGTAGCTAGCGTACGATCGTAGCTAGCGTAC$"
    p = "CGTACGATCGTAGC"
    # text = "ACTGAACACAGATATTATTACGTCCATTA$"
    # p = "ATTA"
    # text = "banana$"
    # p = "ana"
    skip = 12
    bwt, sa = bwtViaSa(text)
    bwt_len = len(bwt)
    C, occ = create_fm_index(bwt, skip)
    pos = find_positions(bwt, C, occ, skip, bwt_len, p, sa)
    
    if pos:
        print(f"Positions of the pattern {p} in the input text: {sorted(pos)}")
    else:
        print("There is no pattern {p} in the input text")
