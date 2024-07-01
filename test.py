from bwt_all import bwtViaSa, create_fm_index, search_classic, search_optimized
import sys

def test_bwt(input, correct_result):
    ret, _ = bwtViaSa(input)
    assert ret == correct_result


def test_search(input, target, correct_result):

    skip = 2
    k = 2
    bwt, sa = bwtViaSa(input)
    partial_sa = {i: si for i, si in enumerate(sa) if si % k == 0}
    bwt_len = len(bwt)
    C, occ = create_fm_index(bwt, skip)

    ret_c = search_classic(input, target, bwt, sa)
    ret_o = search_optimized(bwt, C, occ, skip, bwt_len, target, partial_sa)

    assert ret_c == correct_result
    assert ret_o == correct_result

    

def execute_tests():
    
    test_bwt(input="abaaba$", correct_result="abba$aa")
    test_bwt(input="banana$", correct_result="annb$aa")
    test_bwt(input="CCGTCCAAAGATACCTTTTAGAGGATGAGCCACGGGATACAGTGCCCAAATGATGGCCTCCCCTTTACTGCTATGA$", \
             correct_result="AGCCAATTCTTAGGCGGTGAGCCCATCGGTC$GCAACGCACCTTAGAGTATGTGATCCAAATTCGCAAAGCATTCTC")

    test_search(input="abaaba$", target="aba", correct_result=[0, 3])
    test_search(input="banana$", target="na", correct_result=[2, 4])
    test_search(input="CCGTCCAAAGATACCTTTTAGAGGATGAGCCACGGGATACAGTGCCCAAATGATGGCCTCCCCTTTACTGCTATGA$", \
                target="ATG", correct_result=[52, 49, 24, 72])
    
    test_search(input="abaaba$", target="bab", correct_result=None)
    test_search(input="banana$", target="nananana", correct_result=None)
    test_search(input="CCGTCCAAAGATACCTTTTAGAGGATGAGCCACGGGATACAGTGCCCAAATGATGGCCTCCCCTTTACTGCTATGA$", \
                target="ATGAC", correct_result=None)

    


sys.setrecursionlimit(10**6)

if __name__=="__main__":
    execute_tests()
