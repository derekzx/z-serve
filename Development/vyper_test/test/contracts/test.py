# test_a : constant(uint256) = 0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47
# test_a : constant(uint256) = 21888242871839275222246405745257275088696311157297823662689037894645226208583

# Creation: event({
#     _test_a: uint256
# })


# struct G1Point:
#     X : uint256
#     Y : uint256

struct G2Point:
    X : int128[2]
    Y : int128[2]

# test_a : uint256
# test_b : uint256
# test_c : uint256
# test_x : uint256



# @public
# def __init__():
#     self.test_a = 100
#     pt3 : uint256[6]
#     pt3[0] = self.test_a


    
# @public
# def test1(d : uint256, e : uint256) -> (uint256, uint256):
#     log.Creation(self.test_x)
#     return d+e, d-e

# @public
# def test2(a : uint256) -> (uint256, uint256):
#     newA : uint256 = a
#     newB : uint256 = 10
#     if (1==1):
#         newA = newA - 1
#         return 1, 1
#     elif (1==0):
#         return 1, 0
#     return 1,1

# @public
# def looptest(aa : uint256, bb : uint256) -> (uint256, uint256):
#     maxtimes : uint256
#     maxtimes = 100
#     aaa : uint256
#     aaa = aa
#     for i in range(115792089237316195423570985008687907853269984665640564039457584007913129639935):
#         if aaa == 0:
#             break
#         else:
#             aaa = aaa / 2
#             log.Creation(aaa)
#     return aaa, bb
#     #test

@public
def test() -> G2Point:
    # return G1Point({
    #     X : 11559732032986387107991004021392285783925812861821192530917403151452391805634,
    #     Y : 4082367875863433681332203403145435568316851327593401208105741076214120093531
    # })
    return G2Point({
        X : [1,2],
        Y : [2,3]
    })
