import time
import numpy as np
import unittest 

def create_right_and_left_column_data(right_column):
    characters_right_list = []
    characters_left_dict = {}

    for char in right_column:
        if char != '$':
            if char in characters_left_dict:
                characters_left_dict[char] += 1
            else:
                characters_left_dict[char] = 1

        characters_right_list.append((char, characters_left_dict[char] - 1) if char != '$' else ('$', -1))

    characters_left_dict = {key: characters_left_dict[key] for key in sorted(characters_left_dict)}

    return characters_right_list, characters_left_dict


def check_valid_char(char, valid_chars):
    if char not in valid_chars.keys():
        print(f"Error: Character {char} is not one of the characters from the input string: {list(valid_chars.keys())}")
        return False
    return True


def search_for_target(target_str, characters_right_list, characters_left_dict):

    if check_valid_char(target_str[-1], characters_left_dict) == False:
        return None, None
    
    length_left = characters_left_dict[target_str[-1]]

    starting_position_left = 0

    for i in range(len(target_str)):
        
        char_target = target_str[-(i + 1)]
        char_target_next = target_str[-(i + 2)] if i < len(target_str) - 1 else "/"

        if char_target_next == "/":
            absolute_offset = 0

            for key, value in characters_left_dict.items():
                if key != char_target:
                    absolute_offset += value
                else:
                    break
            absolute_indexes = [i + absolute_offset for i in found_indexes]
            
            return char_target, absolute_indexes

        if (check_valid_char(char_target, characters_left_dict) and check_valid_char(char_target_next, characters_left_dict)) == False:
            return None, None

        starting_position_right = 0

        for key, value in characters_left_dict.items():
            if key != char_target:
                starting_position_right += value
            else:
                break

        starting_position_right += starting_position_left + 1

        length_right = length_left


        length_left = 0
        starting_position_left = -1
        found_indexes = []
        for char_tuple in characters_right_list[starting_position_right: starting_position_right + length_right + 0]:
            if char_tuple[0] == char_target_next:
                length_left += 1
                found_indexes.append(char_tuple[1])
                if starting_position_left == -1:
                    starting_position_left = char_tuple[1]

        if starting_position_left == -1:
            print("The target string is not contained in the input string.")
            return None, None

def search_classic(input_str, target_str, right_column, sa):

    characters_right_list, characters_left_dict = create_right_and_left_column_data(right_column)

    start_time = time.time()

    first_target_char, found_row_indexes = search_for_target(target_str, characters_right_list, characters_left_dict)

    target_indexes_ = None
    
    if first_target_char and found_row_indexes:
        target_indexes_ = [sa[i+1] for i in found_row_indexes]
        print(f"Found {len(target_indexes_)} positions in the input for the pattern {target_str}.")
        print(f"Positions of the pattern in the input text: {target_indexes_}")
        target_indexes_.reverse()
    else:
        print(f"There is no pattern {target_str} in the input text.")

    end_time = time.time()
    search_time = end_time - start_time

    print(f"Searching time: {search_time}")
    vars = {"right_column":right_column, "characters_right_list":characters_right_list, "characters_left_dict":characters_left_dict, "sa":sa, "found_row_indexes":found_row_indexes}
    memory_usage_of_all_vars(vars)
    print("========================================\n\n")
    return target_indexes_




class suffix:
     
    def __init__(self):
         
        self.index = 0
        self.rank = [0, 0]
 
def buildSuffixArray(txt, n):
     
    suffixes = [suffix() for _ in range(n)]
 
    for i in range(n):
        suffixes[i].index = i
        suffixes[i].rank[0] = (ord(txt[i]) - ord("a"))
        suffixes[i].rank[1] = (ord(txt[i + 1]) - ord("a")) if ((i + 1) < n) else -1
 
    suffixes = sorted(suffixes, key = lambda x: (x.rank[0], x.rank[1]))
    ind = [0] * n
    k = 4
    while (k < 2 * n):
        rank = 0
        prev_rank = suffixes[0].rank[0]
        suffixes[0].rank[0] = rank
        ind[suffixes[0].index] = 0

        for i in range(1, n):
            if (suffixes[i].rank[0] == prev_rank and
                suffixes[i].rank[1] == suffixes[i - 1].rank[1]):
                prev_rank = suffixes[i].rank[0]
                suffixes[i].rank[0] = rank   
            else:  
                prev_rank = suffixes[i].rank[0]
                rank += 1
                suffixes[i].rank[0] = rank
            ind[suffixes[i].index] = i

        for i in range(n):
            nextindex = suffixes[i].index + k // 2
            suffixes[i].rank[1] = suffixes[ind[nextindex]].rank[0] \
                if (nextindex < n) else -1
 
        suffixes = sorted(
            suffixes, key = lambda x: (
                x.rank[0], x.rank[1]))
 
        k *= 2
 
    suffixArr = [0] * n
     
    for i in range(n):
        suffixArr[i] = suffixes[i].index
    return suffixArr

def bwtViaSa(t):
    """ Given T, returns BWT(T) by way of the suffix array. """
    bw = []
    start = time.time()
    sa = buildSuffixArray(t, len(t))
    end = time.time()
    print(f"Sort time: {end - start}")
    for si in sa:
        if si == 0: bw.append('$')
        else: bw.append(t[si-1])
    return ''.join(bw), list(sa)

def calculate_checkpoint(pos, c, l, occ, skip, bwt_len):
    remainder = pos % skip
    index = int(pos / skip)
    if pos >= bwt_len:
        index -= 1
    if remainder == 0 and pos < bwt_len:
        occ_pos = occ[c][index]
    else:
        if remainder > skip - remainder and (index + 1) * skip < bwt_len:
            occ_pos = occ[c][index + 1]
            for i in range((index + 1) * skip, pos, -1):
                if l[i] == c:
                    occ_pos -=1
        else:
            occ_pos = occ[c][index]
            for i in range(index * skip + 1, pos + 1, 1):
                if i >= bwt_len:
                    break
                if l[i] == c:
                    occ_pos += 1
    
    return occ_pos

def update_range(l, c, C, occ, skip, bwt_len, start=None, end=None):
    keys = list(C.keys())
    if c not in keys:
        print(f"Error: Character {c} is not one of the characters from the input string")
        return 0, 0
    index = keys.index(c) + 1
    end_next_c = C[keys[index]] if index < len(keys) else bwt_len
    occ_start = 0
    occ_end = 0

    if start and end:
        occ_start = calculate_checkpoint(start - 1, c, l, occ, skip, bwt_len)
        occ_end = calculate_checkpoint(end - 1, c, l, occ, skip, bwt_len)

    start = C[c] + occ_start
    end = C[c] + occ_end if end else end_next_c

    return start, end

def find_indices_in_input(l, C, occ, sa, start, end, skip, bwt_len):
    positions = []
    for i in range(start, end, 1):
        pos = i
        steps = 0
        while pos not in sa.keys():
            char = l[pos]
            pos = C[char] + calculate_checkpoint(pos - 1, char, l, occ, skip, bwt_len)
            steps += 1
        positions.append((sa[pos] + steps) % len(l))

    return positions
    
def find_positions(l, C, occ, skip, bwt_len, p, sa):

    c = p[-1]
    start, end = update_range(l, c, C, occ, skip, bwt_len)
    for i in range(len(p) - 2, -1, -1):
        c = p[i]
        start, end = update_range(l, c, C, occ, skip, bwt_len, start, end)
        
        if start > end:
            return None # there is no patern p in input text
        
    positions = find_indices_in_input(l, C, occ, sa, start, end, skip, bwt_len)
    

    return positions if len(positions) > 0 else None

def create_fm_index(bwt, skip):
    C = {} # dict to save position of first character in F array
    occ = {} # dict to save the number of occurrences of a character up to a given position in the BWT string.
    pos = 0
    for c in sorted(set(bwt)):
        C[c] = pos
        pos += bwt.count(c)
        occ[c] = [0] * (int(len(bwt) / skip) + (1 if len(bwt) % skip != 0 else 0))
    
    for i in range(int(len(bwt) / skip) + (1 if len(bwt) % skip != 0 else 0)):
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

# Memory usage calculation
import sys

def get_size(obj, seen=None):
    """Recursively finds the size of objects."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

def memory_usage_of_all_vars(vars):
    variables = vars 
    total_size = 0
    for name, obj in variables.items():
        size = get_size(obj)
        total_size += size
        print(f"{name}: {size} bytes")
    print(f"Total memory usage: {total_size / (1024 ** 2):.2f} MB")

def read_fasta(fp):
    name, seq = None, []
    i = 0
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
             
    if name: yield (name, ''.join(seq))

def search_optimized(bwt, C, occ, skip, bwt_len, p, partial_sa):
    start_time = time.time()
    pos = find_positions(bwt, C, occ, skip, bwt_len, p, partial_sa)
    if pos:
        pos.reverse()
    end_time = time.time()

    if pos:
        print(f"Found {len(pos)} positions in the input for the pattern {p}.")
        print(f"Positions of the pattern {p} in the input text: {pos}")
    else:
        print(f"There is no pattern {p} in the input text.")
    print(f"Searching time: {end_time - start_time}")
    vars = {"C": C, "occ":occ, "partial_sa":partial_sa, "bwt":bwt}
    memory_usage_of_all_vars(vars)
    print("========================================\n\n")
    return pos
