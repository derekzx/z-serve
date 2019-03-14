# This file is LGPL3 Licensed

#
#@title Elliptic curve operations on twist points for alt_bn128
#@author Derek Chin chinzhixian@gmail.com
#

struct G1Point:
    X : uint256
    Y : uint256

#Encoding of field elements is X[0] * z + X[1]
struct G2Point:
    X : uint256[2]
    Y : uint256[2]

struct VerifyingKey :
    A : G2Point
    B : G1Point
    C : G2Point
    gamma : G2Point
    gammaBeta1 : G1Point
    gammaBeta2 : G2Point
    Z : G2Point
    #right now 6 + 1
    IC : G1Point[7]

struct Proof:
    A : G1Point
    A_p : G1Point
    B : G2Point
    B_p : G1Point
    C : G1Point
    C_p : G1Point
    K : G1Point
    H : G1Point


#Returns G1 Point
contract libMul:
    def mul2(arg1 : uint256[3]) -> uint256[2] : constant


contract libPairingProd3:
    def mul3(arg1 : uint256[18]) -> uint256[1] : constant

contract libPairingProd4:
    def mul4(arg1 : uint256[24]) -> uint256[1] : constant

Verfied: event({
    s : bytes[8]
})


#Initialisation Variables
FIELD_MODULUS : uint256
TWISTBX : uint256
TWISTBY : uint256
PTXX : int128
PTXY : int128
PTYX : int128
PTYY : int128
PTZX : int128
PTZY : int128

#For ECTwistAdd/Mul
# pt3 : uint256[6]
# pt2 : uint256[6]

@public
def __init__():
    self.FIELD_MODULUS = 21888242871839275222246405745257275088696311157297823662689037894645226208583
    self.TWISTBX = 19485874751759354771024239261021720505790618469301721065564631296452457478373
    self.TWISTBY = 266929791119991161246907387137283842545076965332900288569378510910307636690
    self.PTXX = 0
    self.PTXY = 1
    self.PTYX = 2
    self.PTYY = 3
    self.PTZX = 4
    self.PTZY = 5

@public
def GetFieldModulus() -> uint256:
    return self.FIELD_MODULUS

@public
def _addmod(a : uint256, b : uint256, n : uint256) -> uint256:
    return (a+b)%n

@public
def _submod(a : uint256, b : uint256, n : uint256) -> uint256:
    return self._addmod(a , n-b , n)

@public
def _mulmod(a : uint256, b : uint256, n : uint256) -> uint256:
    return (a*b)%n

@public
def _modInv(a : uint256, n : uint256) -> uint256:
    oldT : uint256
    t : uint256 
    newT : uint256
    oldR : uint256
    r : uint256
    newR : uint256
    q : uint256
    t = 0
    newT = 1
    r = n
    newR = a
    #Note: Loop problem
    for i in range(1000000):
        if newR != 0:
            q = r / newR
            oldT = t
            t = newT
            newT = self._submod(oldT, self._mulmod(q, newT, n), n)
            oldR = r
            r = newR
            newR = oldR - q * newR
        else:
            break
    return t

@public
def _FQ2Mul(
        xx : uint256, xy : uint256,
        yx : uint256, yy : uint256
    ) -> (uint256, uint256):
    return (
        self._submod(self._mulmod(xx, yx, self.FIELD_MODULUS), self._mulmod(xy, yy, self.FIELD_MODULUS), self.FIELD_MODULUS),
        self._addmod(self._mulmod(xx, yy, self.FIELD_MODULUS), self._mulmod(xy, yx, self.FIELD_MODULUS), self.FIELD_MODULUS)
    )

@public
def _FQ2Muc(
        xx : uint256,   xy : uint256,
        c : uint256
    ) -> (uint256, uint256):
    return (
        self._mulmod(xx, c, self.FIELD_MODULUS),
        self._mulmod(xy, c, self.FIELD_MODULUS)
    )

@public
def _FQ2Add(
        xx : uint256, xy : uint256,
        yx : uint256, yy : uint256
    ) -> (uint256, uint256):
    return (
        self._addmod(xx, yx, self.FIELD_MODULUS),
        self._addmod(xy, yy, self.FIELD_MODULUS)
    )

@public
def _FQ2Sub(
        xx : uint256, xy : uint256,
        yx : uint256, yy : uint256
    ) -> (uint256, uint256):
    return (
        self._submod(xx, yx, self.FIELD_MODULUS),
        self._submod(xy, yy, self.FIELD_MODULUS)
    )

@public
def _FQ2Inv(
        x: uint256, y: uint256
    ) -> (uint256, uint256):
    inv : uint256
    inv = self._modInv( self._addmod( self._mulmod(y, y, self.FIELD_MODULUS), 
                                    self._mulmod(x, x, self.FIELD_MODULUS), 
                                    self.FIELD_MODULUS), 
                        self.FIELD_MODULUS)
    return (
        self._mulmod(x, inv, self.FIELD_MODULUS),
        self.FIELD_MODULUS - self._mulmod(y, inv, self.FIELD_MODULUS)
    )

@public
def _FQ2Div(
        xx : uint256, xy : uint256,
        yx : uint256, yy : uint256
    ) -> (uint256, uint256):
    yx , yy = self._FQ2Inv(yx, yy)
    return self._FQ2Mul(xx, xy, yx, yy)
    



@public
def _toJacobian(
    pt1xx : uint256, pt1xy : uint256,
    pt1yx : uint256, pt1yy : uint256
    ) -> (
        uint256, uint256,
        uint256, uint256,
        uint256, uint256
    ):
    return (
        pt1xx, pt1xy,
        pt1yx, pt1yy,
        1,     0
    )

@public
def _fromJacobian(
        pt1xx : uint256, pt1xy : uint256,
        pt1yx : uint256, pt1yy : uint256,
        pt1zx : uint256, pt1zy : uint256
    ) -> (
        uint256, uint256,
        uint256, uint256
    ):
    pt2xx : uint256
    pt2xy : uint256
    pt2yx : uint256
    pt2yy : uint256
    invzx : uint256
    invzy : uint256
    invzx, invzy = self._FQ2Inv(pt1zx, pt1zy)
    pt2xx, pt2xy = self._FQ2Mul(pt1xx, pt1xy, invzx, invzy)
    pt2yx, pt2yy = self._FQ2Mul(pt1yx, pt1yy, invzx, invzy)

    return pt2xx, pt2xy, pt2yx, pt2yy


@public
def _isOnCurve(
        xx : uint256, xy : uint256,
        yx : uint256, yy : uint256
    ) -> bool:
    yyx : uint256
    yyy : uint256
    xxxx : uint256
    xxxy : uint256
    yyx, yyy = self._FQ2Mul(yx, yy, yx, yy)
    xxxx, xxxy = self._FQ2Mul(xx, xy, xx, xy)
    xxxx, xxxy = self._FQ2Mul(xxxx, xxxy, xx, xy)
    yyx, yyy = self._FQ2Sub(yyx, yyy, xxxx, xxxy)
    yyx, yyy = self._FQ2Sub(yyx, yyy, self.TWISTBX, self.TWISTBY)
    return yyx==0 and yyy==0

@public
def _ECTwistDoubleJacobian(
        pt1xx : uint256, pt1xy : uint256,
        pt1yx : uint256, pt1yy : uint256,
        pt1zx : uint256, pt1zy : uint256
    ) -> (
        uint256, uint256,
        uint256, uint256,
        uint256, uint256
    ):
    new_pt1xx : uint256 = pt1xx
    new_pt1xy : uint256 = pt1xy
    new_pt1yx : uint256 = pt1yx
    new_pt1yy : uint256 = pt1yy
    new_pt1zx : uint256 = pt1zx
    new_pt1zy : uint256 = pt1zy
    pt2xx : uint256
    pt2xy : uint256
    pt2yx : uint256
    pt2yy : uint256
    pt2zx : uint256
    pt2zy : uint256

    (pt2xx, pt2xy) = self._FQ2Muc(new_pt1xx, new_pt1xy, 3)                          # 3 * x
    (pt2xx, pt2xy) = self._FQ2Mul(pt2xx, pt2xy, new_pt1xx, new_pt1xy)               # W = 3 * x * x
    (new_pt1zx, new_pt1zy) = self._FQ2Mul(new_pt1yx, new_pt1yy, new_pt1zx, new_pt1zy) # S = y * z
    (pt2yx, pt2yy) = self._FQ2Mul(new_pt1xx, new_pt1xy, new_pt1yx, new_pt1yy)  # x * y
    (pt2yx, pt2yy) = self._FQ2Mul(pt2yx, pt2yy, new_pt1zx, new_pt1zy) # B = x * y * S
    (new_pt1xx, new_pt1xy) = self._FQ2Mul(pt2xx, pt2xy, pt2xx, pt2xy) # W * W
    (pt2zx, pt2zy) = self._FQ2Muc(pt2yx, pt2yy, 8)            # 8 * B
    (new_pt1xx, new_pt1xy) = self._FQ2Sub(new_pt1xx, new_pt1xy, pt2zx, pt2zy) # H = W * W - 8 * B
    (pt2zx, pt2zy) = self._FQ2Mul(new_pt1zx, new_pt1zy, new_pt1zx, new_pt1zy) # S_squared = S * S
    (pt2yx, pt2yy) = self._FQ2Muc(pt2yx, pt2yy, 4)            # 4 * B
    (pt2yx, pt2yy) = self._FQ2Sub(pt2yx, pt2yy, new_pt1xx, new_pt1xy) # 4 * B - H
    (pt2yx, pt2yy) = self._FQ2Mul(pt2yx, pt2yy, pt2xx, pt2xy) # W * (4 * B - H)
    (pt2xx, pt2xy) = self._FQ2Muc(new_pt1yx, new_pt1yy, 8)            # 8 * y
    (pt2xx, pt2xy) = self._FQ2Mul(pt2xx, pt2xy, new_pt1yx, new_pt1yy) # 8 * y * y
    (pt2xx, pt2xy) = self._FQ2Mul(pt2xx, pt2xy, pt2zx, pt2zy) # 8 * y * y * S_squared
    (pt2yx, pt2yy) = self._FQ2Sub(pt2yx, pt2yy, pt2xx, pt2xy) # newy = W * (4 * B - H) - 8 * y * y * S_squared
    (pt2xx, pt2xy) = self._FQ2Muc(new_pt1xx, new_pt1xy, 2)            # 2 * H
    (pt2xx, pt2xy) = self._FQ2Mul(pt2xx, pt2xy, new_pt1zx, new_pt1zy) # newx = 2 * H * S
    (pt2zx, pt2zy) = self._FQ2Mul(new_pt1zx, new_pt1zy, pt2zx, pt2zy) # S * S_squared
    (pt2zx, pt2zy) = self._FQ2Muc(pt2zx, pt2zy, 8)            # newz = 8 * S * S_squared

    return pt2xx, pt2xy, pt2yx, pt2yy, pt2zx, pt2zy


@public
def _ECTwistAddJacobian(
        pt1xx : uint256, pt1xy : uint256,
        pt1yx : uint256, pt1yy : uint256,
        pt1zx : uint256, pt1zy : uint256,
        pt2xx : uint256, pt2xy : uint256,
        pt2yx : uint256, pt2yy : uint256,
        pt2zx : uint256, pt2zy : uint256
    ) -> uint256[6]:

    pt3 : uint256[6]
    if (pt1zx == 0 and pt1zy == 0):
        pt3[self.PTXX] = pt2xx
        pt3[self.PTXY] = pt2xy
        pt3[self.PTYX] = pt2yx
        pt3[self.PTYY] = pt2yy
        pt3[self.PTZX] = pt2zx
        pt3[self.PTZY] = pt2zy
        return pt3
    
    elif (pt1zx == 0 and pt1zy == 0):
        pt3[self.PTXX] = pt2xx
        pt3[self.PTXY] = pt2xy
        pt3[self.PTYX] = pt2yx
        pt3[self.PTYY] = pt2yy
        pt3[self.PTZX] = pt2zx
        pt3[self.PTZY] = pt2zy
        return pt3

    new_pt2yx : uint256 = pt2yx
    new_pt2yy : uint256 = pt2yy
    new_pt2xx : uint256 = pt2xx
    new_pt2xy : uint256 = pt2xy
    
    new_pt2yx, new_pt2yy = self._FQ2Mul(pt2yx, pt2yy, pt1zx, pt1zy) # U1 = y2*z1
    pt3[self.PTYX], pt3[self.PTYY] = self._FQ2Mul(pt1yx, pt1yy, pt2zx, pt2zy) # U2 = y1 * z2
    new_pt2xx, new_pt2xy = self._FQ2Mul(pt2xx, pt2xy, pt1zx, pt1zy) # V1 = x2 * z1
    pt3[self.PTZX], pt3[self.PTZY] = self._FQ2Mul(pt1xx, pt1xy, pt2zx, pt2zy) # V2 = x1 * z2

    if (new_pt2xx == pt3[self.PTZX] and new_pt2xy == pt3[self.PTZY]):
        if (new_pt2yx == pt3[self.PTYX] and new_pt2yy == pt3[self.PTYY]):
            (pt3[self.PTXX], pt3[self.PTXY],
            pt3[self.PTYX], pt3[self.PTYY],
            pt3[self.PTZX], pt3[self.PTZY]) = self._ECTwistDoubleJacobian(pt1xx, pt1xy, pt1yx, pt1yy, pt1zx, pt1zy)
            return pt3
        pt3[self.PTXX] = 0
        pt3[self.PTXY] = 0
        pt3[self.PTYX] = 0
        pt3[self.PTYY] = 0
        pt3[self.PTZX] = 0
        pt3[self.PTZY] = 0
        return pt3
    
    new_pt1xx : uint256 = pt1xx
    new_pt1xy : uint256 = pt1xy
    new_pt1yx : uint256 = pt1yx
    new_pt1yy : uint256 = pt1yy
    new_pt1zx : uint256 = pt1zx
    new_pt1zy : uint256 = pt1zy
    new_pt2zx : uint256 = pt2zx
    new_pt2zy : uint256 = pt2zy

    (new_pt2zx,     new_pt2zy)     = self._FQ2Mul(pt1zx, pt1zy, pt2zx,     pt2zy)     # W = z1 * z2
    (new_pt1xx,     new_pt1xy)     = self._FQ2Sub(new_pt2yx, new_pt2yy, pt3[self.PTYX], pt3[self.PTYY]) # U = U1 - U2
    (new_pt1yx,     new_pt1yy)     = self._FQ2Sub(new_pt2xx, new_pt2xy, pt3[self.PTZX], pt3[self.PTZY]) # V = V1 - V2
    (new_pt1zx,     new_pt1zy)     = self._FQ2Mul(new_pt1yx, new_pt1yy, new_pt1yx, new_pt1yy)     # V_squared = V * V
    (new_pt2yx,     new_pt2yy)     = self._FQ2Mul(new_pt1zx, new_pt1zy, pt3[self.PTZX], pt3[self.PTZY]) # V_squared_times_V2 = V_squared * V2
    (new_pt1zx,     new_pt1zy)     = self._FQ2Mul(new_pt1zx, new_pt1zy, new_pt1yx,     new_pt1yy)     # V_cubed = V * V_squared
    (pt3[self.PTZX], pt3[self.PTZY]) = self._FQ2Mul(new_pt1zx, new_pt1zy, new_pt2zx,     new_pt2zy)    # newz = V_cubed * W
    (new_pt2xx,     new_pt2xy)     = self._FQ2Mul(new_pt1xx, new_pt1xy, new_pt1xx,     new_pt1xy)     # U * U
    (new_pt2xx,     new_pt2xy)     = self._FQ2Mul(new_pt2xx, new_pt2xy, new_pt2zx,     new_pt2zy)     # U * U * W
    (new_pt2xx,     new_pt2xy)     = self._FQ2Sub(new_pt2xx, new_pt2xy, new_pt1zx,     new_pt1zy)     # U * U * W - V_cubed
    (new_pt2zx,     new_pt2zy)     = self._FQ2Muc(new_pt2yx, new_pt2yy, 2)                    # 2 * V_squared_times_V2
    (new_pt2xx,     new_pt2xy)     = self._FQ2Sub(new_pt2xx, new_pt2xy, new_pt2zx,     new_pt2zy)     # A = U * U * W - V_cubed - 2 * V_squared_times_V2
    (pt3[self.PTXX], pt3[self.PTXY]) = self._FQ2Mul(new_pt1yx, new_pt1yy, new_pt2xx,     new_pt2xy)    # newx = V * A
    (new_pt1yx,     new_pt1yy)     = self._FQ2Sub(new_pt2yx, new_pt2yy, new_pt2xx,     new_pt2xy)     # V_squared_times_V2 - A
    (new_pt1yx,     new_pt1yy)     = self._FQ2Mul(new_pt1xx, new_pt1xy, new_pt1yx,     new_pt1yy)     # U * (V_squared_times_V2 - A)
    (new_pt1xx,     new_pt1xy)     = self._FQ2Mul(new_pt1zx, new_pt1zy, pt3[self.PTYX], pt3[self.PTYY]) # V_cubed * U2
    (pt3[self.PTYX], pt3[self.PTYY]) = self._FQ2Sub(new_pt1yx, new_pt1yy, new_pt1xx,     new_pt1xy)    # newy = U * (V_squared_times_V2 - A) - V_cubed * U2

    return pt3


@public
def ECTwistAdd(
        pt1xx: uint256, pt1xy: uint256, 
        pt1yx: uint256, pt1yy: uint256,
        pt2xx: uint256, pt2xy: uint256,
        pt2yx: uint256, pt2yy: uint256
        ) -> (
            uint256, uint256,
            uint256, uint256
        ):
    ptsOnCurve : bool
    ptsOnCurve = self._isOnCurve(pt1xx, pt1xy, pt1yx, pt1yy)
    assert(ptsOnCurve)

    pt3 : uint256[6]
    pt3 = self._ECTwistAddJacobian(
        pt1xx,  pt1xy,
        pt1yx,  pt1yy,
        1,      0,
        pt2xx,  pt2xy,
        pt2yx,  pt2yy,
        1,      0
    )

    return self._fromJacobian(
        pt3[self.PTXX], pt3[self.PTXY],
        pt3[self.PTYX], pt3[self.PTYY],
        pt3[self.PTZX], pt3[self.PTZY]
    )

@public
def _ECTwistMulJacobian(
    d : uint256,
    pt1xx : uint256, pt1xy : uint256,
    pt1yx : uint256, pt1yy : uint256,
    pt1zx : uint256, pt1zy : uint256
    ) -> uint256[6]:

    new_d : uint256 = d
    new_pt1xx : uint256 = pt1xx
    new_pt1xy : uint256 = pt1xy
    new_pt1yx : uint256 = pt1yx
    new_pt1yy : uint256 = pt1yy
    new_pt1zx : uint256 = pt1zx
    new_pt1zy : uint256 = pt1zy
    pt2 : uint256[6]

    for i in range(10000):
        if new_d == 0:
            break
        # elif ((new_d and 1) != 0):
        elif(new_d - 1 != 0):
            pt2 = self._ECTwistAddJacobian(
                pt2[self.PTXX], pt2[self.PTXY],
                pt2[self.PTYX], pt2[self.PTYY],
                pt2[self.PTZX], pt2[self.PTZY],
                new_pt1xx, new_pt1xy,
                new_pt1yx, new_pt1yy,
                new_pt1zx, new_pt1zy
            )
        (new_pt1xx, new_pt1xy,
        new_pt1yx, new_pt1yy,
        new_pt1zx, new_pt1zy) = self._ECTwistDoubleJacobian(
            new_pt1xx, new_pt1xy,
            new_pt1yx, new_pt1yy,
            new_pt1zx, new_pt1zy)
        new_d = new_d/2
    return pt2

@public    
def ECTwistMul(
        s: uint256,
        pt1xx: uint256, pt1xy: uint256,
        pt1yx: uint256, pt1yy: uint256
    ) -> (
        uint256, uint256,
        uint256, uint256):
    ptsOnCurve : bool
    ptsOnCurve = self._isOnCurve(pt1xx, pt1xy, pt1yx, pt1yy)
    assert (ptsOnCurve)
    pt2 : uint256[6]
    pt2 = self._ECTwistMulJacobian(
        s,
        pt1xx,  pt1xy,
        pt1yx,  pt1yy,
        1,      0,
    )

    return self._fromJacobian(
        pt2[self.PTXX], pt2[self.PTXY],
        pt2[self.PTYX], pt2[self.PTYY],
        pt2[self.PTZX], pt2[self.PTZY]
    )

#Returns the generator of G1
@public
# def P1() -> uint256[2]:
#     X : uint256 = 1
#     Y : uint256 = 2
#     return [X,Y]

def P1() -> G1Point:
    return G1Point({
        X : 1,
        Y : 2
    })

# Returns the generator of G2
@public
def P2() -> G2Point:
    return G2Point({
        X : [11559732032986387107991004021392285783925812861821192530917403151452391805634,
             10857046999023057135944570762232829481370756359578518086990519993285655852781],
        Y : [4082367875863433681332203403145435568316851327593401208105741076214120093531,
             8495653923123431417604973247489272438418190587263600148770280649306958101930]
    })

    # /// @return the generator of G2
    # function P2() pure internal returns (G2Point) {
    #     return G2Point(
    #         [11559732032986387107991004021392285783925812861821192530917403151452391805634,
    #          10857046999023057135944570762232829481370756359578518086990519993285655852781],
    #         [4082367875863433681332203403145435568316851327593401208105741076214120093531,
    #          8495653923123431417604973247489272438418190587263600148770280649306958101930]
    #     );
    # }

#Returns the negation of p, i.e. p.addition(p.negate()) should be zero.
@public
def negate(p : G1Point) -> G1Point:
    # The prime q in the base field F_q for G1
    q : uint256 = 21888242871839275222246405745257275088696311157297823662689037894645226208583
    if (p.X == 0 and p.Y == 0):
        return G1Point({
            X : 0,
            Y : 0
        })
    return G1Point({
            X : p.X,
            Y : q - (p.Y % q)
        })


    # /// @return the negation of p, i.e. p.addition(p.negate()) should be zero.
    # function negate(G1Point p) pure internal returns (G1Point) {
    #     // The prime q in the base field F_q for G1
    #     uint q = 21888242871839275222246405745257275088696311157297823662689037894645226208583;
    #     if (p.X == 0 && p.Y == 0)
    #         return G1Point(0, 0);
    #     return G1Point(p.X, q - (p.Y % q));
    # }

# contract libAdd:
#     def add(arg1 : uint256[4]) -> uint256[2]: constant

#uint256 is 32 bytes
@public
def G1addition(p1 : G1Point, p2 : G2Point) -> (G1Point):
    input : uint256[4]
    r : uint256[2]
    input[0] = p1.X
    input[1] = p1.Y
    input[2] = p2.X
    input[3] = p2.Y
    success : bool
    r = raw_call(0x6, input, 32*2, 8000000)
    return r

    # /// @return the sum of two points of G1
    # function addition(G1Point p1, G1Point p2) internal returns (G1Point r) {
    #     uint[4] memory input;
    #     input[0] = p1.X;
    #     input[1] = p1.Y;
    #     input[2] = p2.X;
    #     input[3] = p2.Y;
    #     bool success;
    #     assembly {
    #         success := call(sub(gas, 2000), 6, 0, input, 0xc0, r, 0x60)
    #         // Use "invalid" to make gas estimation work
    #         switch success case 0 { invalid() }
    #     }
    #     require(success);
    # }

# Return the sum of two points of G2
@public
def G2addition(p1 : G2Point, p2 : G2Point) -> G2Point:
    r : G2Point
    r.X[1], r.X[0], r.Y[1], r.Y[0] = self.ECTwistAdd(p1.X[1], p1.X[0], p1.Y[1], p1.y[0], p2.X[1], p2.X[0], p2.Y[1], p2.Y[0])
    return r



    # /// @return the sum of two points of G2
    # function addition(G2Point p1, G2Point p2) internal pure returns (G2Point r) {
    #     (r.X[1], r.X[0], r.Y[1], r.Y[0]) = BN256G2.ECTwistAdd(p1.X[1],p1.X[0],p1.Y[1],p1.Y[0],p2.X[1],p2.X[0],p2.Y[1],p2.Y[0]);
    # }

# Return th eproduct of a point on G1 and a scalar
# p == p.scalar_mul(1) and p.addition(p == p.scalar_mul(2) for all points P

@public
def scalar_mul(p : G1Point, s : uint256) -> G1Point:
    r : G1Point
    input : uint256[3]
    success : bool
    input[0] = p.X
    input[1] = p.Y
    input[2] = s
    r = libMul(0x7)
    return r

    # /// @return the product of a point on G1 and a scalar, i.e.
    # /// p == p.scalar_mul(1) and p.addition(p) == p.scalar_mul(2) for all points p.
    # function scalar_mul(G1Point p, uint s) internal returns (G1Point r) {
    #     uint[3] memory input;
    #     input[0] = p.X;
    #     input[1] = p.Y;
    #     input[2] = s;
    #     bool success;
    #     assembly {
    #         success := call(sub(gas, 2000), 7, 0, input, 0x80, r, 0x60)
    #         // Use "invalid" to make gas estimation work
    #         switch success case 0 { invalid() }
    #     }
    #     require (success);
    # }

# @return the result of computing the pairing check
# e(p1[0], p2[0]) *  .... * e(p1[n], p2[n]) == 1
# For example pairing([P1(), P1().negate()], [P2(), P2()]) should
# return true.
# contract libPairingProd2:
#     def mul(arg1 : uint256[12]) -> uint256[1] : constant

def pairingProd2(p1 : G1Point[2], p2 : G2Point[2]) -> bool:
    # inputsize = elements * 6
    input : uint256[12]
    out : uint256[1]
    for i in range(2):
        input[i * 6 + 0] = p1[i].X
        input[i * 6 + 1] = p1[i].Y
        input[i * 6 + 2] = p2[i].X[0]
        input[i * 6 + 3] = p2[i].X[1]
        input[i * 6 + 4] = p2[i].Y[0]
        input[i * 6 + 5] = p2[i].Y[1]
    out = r = raw_call(0x8, input, 32, 8000000)
    return out[0] != 0

def pairingProd3(p1 : G1Point[3], p2 : G2Point[3]) -> bool:
    # inputsize = elements * 6
    input : uint256[18]
    out : uint256[1]
    for i in range(3):
        input[i * 6 + 0] = p1[i].X
        input[i * 6 + 1] = p1[i].Y
        input[i * 6 + 2] = p2[i].X[0]
        input[i * 6 + 3] = p2[i].X[1]
        input[i * 6 + 4] = p2[i].Y[0]
        input[i * 6 + 5] = p2[i].Y[1]
    out = raw_call(0x8, input, 32, 8000000)
    return out[0] != 0


def pairingProd4(p1 : G1Point[4], p2 : G2Point[4]) -> bool:
    # inputsize = elements * 6
    input : uint256[24]
    out : uint256[1]
    for i in range(2):
        input[i * 6 + 0] = p1[i].X
        input[i * 6 + 1] = p1[i].Y
        input[i * 6 + 2] = p2[i].X[0]
        input[i * 6 + 3] = p2[i].X[1]
        input[i * 6 + 4] = p2[i].Y[0]
        input[i * 6 + 5] = p2[i].Y[1]
    out = raw_call(0x8, input, 32, 8000000)
    return out[0] != 0



#     /// @return the result of computing the pairing check
#     /// e(p1[0], p2[0]) *  .... * e(p1[n], p2[n]) == 1
#     /// For example pairing([P1(), P1().negate()], [P2(), P2()]) should
#     /// return true.
#     function pairing(G1Point[] p1, G2Point[] p2) internal returns (bool) {
#         require(p1.length == p2.length);
#         uint elements = p1.length;
#         uint inputSize = elements * 6;
#         uint[] memory input = new uint[](inputSize);
#         for (uint i = 0; i < elements; i++)
#         {
#             input[i * 6 + 0] = p1[i].X;
#             input[i * 6 + 1] = p1[i].Y;
#             input[i * 6 + 2] = p2[i].X[0];
#             input[i * 6 + 3] = p2[i].X[1];
#             input[i * 6 + 4] = p2[i].Y[0];
#             input[i * 6 + 5] = p2[i].Y[1];
#         }
#         uint[1] memory out;
#         bool success;
#         assembly {
#             success := call(sub(gas, 2000), 8, 0, add(input, 0x20), mul(inputSize, 0x20), out, 0x20)
#             // Use "invalid" to make gas estimation work
#             switch success case 0 { invalid() }
#         }
#         require(success);
#         return out[0] != 0;
#     }
#     /// Convenience method for a pairing check for two pairs.
#     function pairingProd2(G1Point a1, G2Point a2, G1Point b1, G2Point b2) internal returns (bool) {
#         G1Point[] memory p1 = new G1Point[](2);
#         G2Point[] memory p2 = new G2Point[](2);
#         p1[0] = a1;
#         p1[1] = b1;
#         p2[0] = a2;
#         p2[1] = b2;
#         return pairing(p1, p2);
#     }
#     /// Convenience method for a pairing check for three pairs.
#     function pairingProd3(
#             G1Point a1, G2Point a2,
#             G1Point b1, G2Point b2,
#             G1Point c1, G2Point c2
#     ) internal returns (bool) {
#         G1Point[] memory p1 = new G1Point[](3);
#         G2Point[] memory p2 = new G2Point[](3);
#         p1[0] = a1;
#         p1[1] = b1;
#         p1[2] = c1;
#         p2[0] = a2;
#         p2[1] = b2;
#         p2[2] = c2;
#         return pairing(p1, p2);
#     }
#     /// Convenience method for a pairing check for four pairs.
#     function pairingProd4(
#             G1Point a1, G2Point a2,
#             G1Point b1, G2Point b2,
#             G1Point c1, G2Point c2,
#             G1Point d1, G2Point d2
#     ) internal returns (bool) {
#         G1Point[] memory p1 = new G1Point[](4);
#         G2Point[] memory p2 = new G2Point[](4);
#         p1[0] = a1;
#         p1[1] = b1;
#         p1[2] = c1;
#         p1[3] = d1;
#         p2[0] = a2;
#         p2[1] = b2;
#         p2[2] = c2;
#         p2[3] = d2;
#         return pairing(p1, p2);
#     }
# }

# contract Verifier {
#     using Pairing for *;
    


# struct 
#     struct VerifyingKey {
#         Pairing.G2Point A;
#         Pairing.G1Point B;
#         Pairing.G2Point C;
#         Pairing.G2Point gamma;
#         Pairing.G1Point gammaBeta1;
#         Pairing.G2Point gammaBeta2;
#         Pairing.G2Point Z;
#         Pairing.G1Point[] IC;
#     }




    # struct Proof {
    #     Pairing.G1Point A;
    #     Pairing.G1Point A_p;
    #     Pairing.G2Point B;
    #     Pairing.G1Point B_p;
    #     Pairing.G1Point C;
    #     Pairing.G1Point C_p;
    #     Pairing.G1Point K;
    #     Pairing.G1Point H;
    # }

def verifyingKey() -> VerifyingKey: 
    return VerifyingKey({
        A : G2Point({
            X : [0x2e86d7d71ee2c343972c8edce7b9fd265644c902fb56964107371972e677d478, 0x21426632cf61b8deec72056244cbec3cc5cc92fde7b653df3372043e8bf493f7],
            Y : [0x23a7a35306d80e8c99f6523f7fce72ba5758cb765f37882bb5dc267b1a6ae77f, 0x117e50ec8bf70a46d03113445e73136b1adec99e6cac59bce62830fd74c7b74e]
        }),
        B : G1Point({
            X : 0x1ecb66038b5aee41907a9026a43104446ed277567567022126b99d22d6768495,
            Y : 0xa5269edb83b9d5d497abd740d7450aadb16847d661b789e714eaabf1eb0f973
        }),
        C : G2Point({
            X : [0x3def3ca547c0f329657f29aa5b637d0b1ef2d72f52aa89a79c2ec2277c9c541, 0x23c86c925a2efb6c9c23b2145cf33201225fa489822b7c48bc4fbecb4328f5ce],
            Y : [0x1a1281dd870d0bcaafac6c9744828801a419ec31cc2bf8ae608766eb1be43d7, 0x27a9c0e52807c6ade61a11c3fcabf85685beb398f11e9503458e3a11ca547cdc]
        }),
        gamma : G2Point({
            X : [0x7887c75258a2f55d58ff210a85e83027d5d3cca86c0c20949c31790da63b0f4, 0x247275a9e1eff73baf32f68e2ed10d8a53770bc133b8ebcaa87454c7ec3fcaa0],
            Y : [0x286a9f230418f663b1548e6c986a1f523513e4cdb8718e9532d76073f2b5eca6, 0x27d6ae4ed0175840b56e30343ee85bb2108c8397c9cb0c4d38939a0f08b67ae7]
        }),
        gammaBeta1 : G1Point({
            X : 0x8f467f4524dbb8367dbd666b5ca7ece14ecf2eea70b1d8d1ac6aaddf547c023,
            Y : 0x65fe1e190aa95ab5fa26c659e9ba1e57d4f653a03e773e1649e0a98096d4e67
        }),
        gammaBeta2 : G2Point({
            X : [0x2f6590e3035056091cb5ea1f3e50b0544f5d9c14fb8862c3b595fe3a3e68977, 0xee0473633db1cd65a02821c3e88f6e8635d3cc04baf654365aab37925f15bbe],
            Y : [0x1b579812ce5608f23ee98bfa24ac94cdd5d392efa04fbf3b9b2d07e2af6fd0b2, 0x2d9b16d22c080c999802eba149a96c289870fe847628c2ee84a9a4d06a3b7783]
        }),
        Z : G2Point({
            X : [0x9f138130f8649bd4a9da4f253bb0152e6bfc4423aaa0aea97e5fe9a2e3a1604, 0xc9db90512e17b67aa27085776d65217a1f5f05284e1753c99355b5f487eed9b],
            Y : [0x137578e16bd872b1fe5d7e52529441821eedc355c1b56f17164cc99278b5c403, 0x17154cec8ad4be3eed9fab54fab1a3a52148246e275b387666443f19b9cce120]
        }),
        IC : [G1Point({
            X : 0x2a260a549c91d5b48b4c3eecba09ffab676781e06f5836a84e74d25a52bb356d,
            Y : 0xf7181ead50cf399acd87be174472770fa4372975af708e959ee64802ae1970f
        }), G1Point({
            X : 0x5b06f858e835056d73802487d0a53e4dd9c5a28c32854d6afec8b516925c16f,
            Y : 0x15f42770f7d27d14ef0c99ce689f1295b2e090e11e4cc54de74a2bfed48b61e6
        }), G1Point({
            X : 0x125410b9d0a9c73edcdbdb76f9eb5c4e66eaac35862ee647f419d23b91c668fd,
            Y : 0xa942646bb715616ed4ffed5f1762ba2eb389da82048656207bc0ff0d5e2639c
        }), G1Point({
            X : 0x13595237cd648d09f13272fb25999d368cea167b2baf1b9d7676eeb120655e54,
            Y : 0x28556005f4a1fa6a1a65a67c656e67cb91e6f609999067d97b44090d6937c22b
        }), G1Point({
            X : 0x2ca8543a85226e999cddc620cfdf88dfcfcb8bec33d9b89f9b6c5641106d94a0,
            Y : 0x291c7bf54911226a59f89373cabb87e811a2538f46cec68cf8752cd02f75ba3d
        }), G1Point({
            X : 0xdba73dfb7a766273b70752c20f6f3fb3f93680777eec245defefab6017401b1,
            Y : 0x2cb1484f863f6883962c5972c70b43281ee706a65ac392cf44caf5d2b44cc010
        }), G1Point({
            X : 0x282f03de764d3297d7643f6805151ef9968600f080944bdcc898648d146875c,
            Y : 0x24ec115477498a9e210bc0dc179ba60d7b7e01ae9f522a20b7b9d1e60ee7f40a
        })]

    })


    # function verifyingKey() pure internal returns (VerifyingKey vk) {
    #     vk.A = Pairing.G2Point([0x2e86d7d71ee2c343972c8edce7b9fd265644c902fb56964107371972e677d478, 0x21426632cf61b8deec72056244cbec3cc5cc92fde7b653df3372043e8bf493f7], [0x23a7a35306d80e8c99f6523f7fce72ba5758cb765f37882bb5dc267b1a6ae77f, 0x117e50ec8bf70a46d03113445e73136b1adec99e6cac59bce62830fd74c7b74e]);
    #     vk.B = Pairing.G1Point(0x1ecb66038b5aee41907a9026a43104446ed277567567022126b99d22d6768495, 0xa5269edb83b9d5d497abd740d7450aadb16847d661b789e714eaabf1eb0f973);
    #     vk.C = Pairing.G2Point([0x3def3ca547c0f329657f29aa5b637d0b1ef2d72f52aa89a79c2ec2277c9c541, 0x23c86c925a2efb6c9c23b2145cf33201225fa489822b7c48bc4fbecb4328f5ce], [0x1a1281dd870d0bcaafac6c9744828801a419ec31cc2bf8ae608766eb1be43d7, 0x27a9c0e52807c6ade61a11c3fcabf85685beb398f11e9503458e3a11ca547cdc]);
    #     vk.gamma = Pairing.G2Point([0x7887c75258a2f55d58ff210a85e83027d5d3cca86c0c20949c31790da63b0f4, 0x247275a9e1eff73baf32f68e2ed10d8a53770bc133b8ebcaa87454c7ec3fcaa0], [0x286a9f230418f663b1548e6c986a1f523513e4cdb8718e9532d76073f2b5eca6, 0x27d6ae4ed0175840b56e30343ee85bb2108c8397c9cb0c4d38939a0f08b67ae7]);
    #     vk.gammaBeta1 = Pairing.G1Point(0x8f467f4524dbb8367dbd666b5ca7ece14ecf2eea70b1d8d1ac6aaddf547c023, 0x65fe1e190aa95ab5fa26c659e9ba1e57d4f653a03e773e1649e0a98096d4e67);
    #     vk.gammaBeta2 = Pairing.G2Point([0x2f6590e3035056091cb5ea1f3e50b0544f5d9c14fb8862c3b595fe3a3e68977, 0xee0473633db1cd65a02821c3e88f6e8635d3cc04baf654365aab37925f15bbe], [0x1b579812ce5608f23ee98bfa24ac94cdd5d392efa04fbf3b9b2d07e2af6fd0b2, 0x2d9b16d22c080c999802eba149a96c289870fe847628c2ee84a9a4d06a3b7783]);
    #     vk.Z = Pairing.G2Point([0x9f138130f8649bd4a9da4f253bb0152e6bfc4423aaa0aea97e5fe9a2e3a1604, 0xc9db90512e17b67aa27085776d65217a1f5f05284e1753c99355b5f487eed9b], [0x137578e16bd872b1fe5d7e52529441821eedc355c1b56f17164cc99278b5c403, 0x17154cec8ad4be3eed9fab54fab1a3a52148246e275b387666443f19b9cce120]);
    #     vk.IC = new Pairing.G1Point[](7);
    #     vk.IC[0] = Pairing.G1Point(0x2a260a549c91d5b48b4c3eecba09ffab676781e06f5836a84e74d25a52bb356d, 0xf7181ead50cf399acd87be174472770fa4372975af708e959ee64802ae1970f);
    #     vk.IC[1] = Pairing.G1Point(0x5b06f858e835056d73802487d0a53e4dd9c5a28c32854d6afec8b516925c16f, 0x15f42770f7d27d14ef0c99ce689f1295b2e090e11e4cc54de74a2bfed48b61e6);
    #     vk.IC[2] = Pairing.G1Point(0x125410b9d0a9c73edcdbdb76f9eb5c4e66eaac35862ee647f419d23b91c668fd, 0xa942646bb715616ed4ffed5f1762ba2eb389da82048656207bc0ff0d5e2639c);
    #     vk.IC[3] = Pairing.G1Point(0x13595237cd648d09f13272fb25999d368cea167b2baf1b9d7676eeb120655e54, 0x28556005f4a1fa6a1a65a67c656e67cb91e6f609999067d97b44090d6937c22b);
    #     vk.IC[4] = Pairing.G1Point(0x2ca8543a85226e999cddc620cfdf88dfcfcb8bec33d9b89f9b6c5641106d94a0, 0x291c7bf54911226a59f89373cabb87e811a2538f46cec68cf8752cd02f75ba3d);
    #     vk.IC[5] = Pairing.G1Point(0xdba73dfb7a766273b70752c20f6f3fb3f93680777eec245defefab6017401b1, 0x2cb1484f863f6883962c5972c70b43281ee706a65ac392cf44caf5d2b44cc010);
    #     vk.IC[6] = Pairing.G1Point(0x282f03de764d3297d7643f6805151ef9968600f080944bdcc898648d146875c, 0x24ec115477498a9e210bc0dc179ba60d7b7e01ae9f522a20b7b9d1e60ee7f40a);
    # }

def verify(input : uint256[6], proof : Proof) -> uint256:
    vk : VerifyingKey
    vk = self.verifyingKey()
    #assert input.length + 1== vk.IC.length , no need because hardcoded at the moment
    #Compute linear combination vk_x
    vk_x : G1Point
    vk_x = G1Point({
        X : 0,
        Y : 0
    })
    for i in range(6):
        vk_x = self.addition(vk_x, self.scalar_mul(vk.IC[i+1], input[i]))
    vk = self.addition(vk_x, vk.IC[0])
    if (self.pairingProd2(proof.A, vk.A, self.negate(proof.A_p), self.P2())) != True:
        return 1
    if (self.pairingProd2(vk.B, proof.B, self.negate(proof.B_p), self.P2())) != True:
        return 2
    if (self.pairingProd2(proof.C, vk.C, self.negate(proof.C_p), self.P2())) != True:
        return 3
    if (self.pairingProd3(
        proof.K, vk.gamma, 
        self.negate(self.addition(vk_x, self.addition(proof.A, proof.C))), vk.gammaBeta2,
        self.negate(vk.gammaBeta1), proof.B)) != True:
        return 4
    if (self.pairingProd3(
            self.addition(vk_x, proof.A), proof.B,
            self.negate(proof.H), vk.Z,
            self.negate(proof.C), self.P2()
        )) != True:
        return 5
    return 0



    # function verify(uint[] input, Proof proof) internal returns (uint) {
    #     VerifyingKey memory vk = verifyingKey();
    #     require(input.length + 1 == vk.IC.length);
    #     // Compute the linear combination vk_x
    #     Pairing.G1Point memory vk_x = Pairing.G1Point(0, 0);
    #     for (uint i = 0; i < input.length; i++)
    #         vk_x = Pairing.addition(vk_x, Pairing.scalar_mul(vk.IC[i + 1], input[i]));
    #     vk_x = Pairing.addition(vk_x, vk.IC[0]);
    #     if (!Pairing.pairingProd2(proof.A, vk.A, Pairing.negate(proof.A_p), Pairing.P2())) return 1;
    #     if (!Pairing.pairingProd2(vk.B, proof.B, Pairing.negate(proof.B_p), Pairing.P2())) return 2;
    #     if (!Pairing.pairingProd2(proof.C, vk.C, Pairing.negate(proof.C_p), Pairing.P2())) return 3;
    #     if (!Pairing.pairingProd3(
    #         proof.K, vk.gamma,
    #         Pairing.negate(Pairing.addition(vk_x, Pairing.addition(proof.A, proof.C))), vk.gammaBeta2,
    #         Pairing.negate(vk.gammaBeta1), proof.B
    #     )) return 4;
    #     if (!Pairing.pairingProd3(
    #             Pairing.addition(vk_x, proof.A), proof.B,
    #             Pairing.negate(proof.H), vk.Z,
    #             Pairing.negate(proof.C), Pairing.P2()
    #     )) return 5;
    #     return 0;
    # }


    # event Verified(string s);



@public
def verifyTx(
        a : uint256[2],
        a_p : uint256[2],
        b : uint256[2][2],
        c : uint256[2],
        c_p : uint256[2],
        h : uint256[2],
        k : uint256[2],
        input : uint256[6]
    ) -> bool:
    proof : Proof
    proof.A = G1Point({
        X : a[0],
        Y : a[1]    
    })
    proof.A_p = G1Point({
        X : a_p[0],
        Y : a_p[1]
    })
    proof.B = G2Point({
        X : [b[0][0], b[0][1]],
        Y : [b[1][0], b[1][1]]
    })
    proof.C = G1Point({
        X : c[0],
        Y : c[1]
    })
    proof.C_p = G1Point({
        X : c_p[0],
        Y : c_p[1]
    })
    proof.H = G1Point({
        X : h[0],
        Y : h[1]
    })
    proof.K = G1Point({
        X : k[0],
        Y : k[1]
    })
    inputValues : uint256[6]
    #Note: only 6 for this contract
    for i in range(6):
        inputValues[i] = input[i]
    if self.verify(inputValues, proof) == 0:
        log.Verified("Verified")
        return True
    else:
        return False



#     function verifyTx(
#             uint[2] a,
#             uint[2] a_p,
#             uint[2][2] b,
#             uint[2] b_p,
#             uint[2] c,
#             uint[2] c_p,
#             uint[2] h,
#             uint[2] k,
#             uint[6] input
#         ) public returns (bool r) {
#         Proof memory proof;
#         proof.A = Pairing.G1Point(a[0], a[1]);
#         proof.A_p = Pairing.G1Point(a_p[0], a_p[1]);
#         proof.B = Pairing.G2Point([b[0][0], b[0][1]], [b[1][0], b[1][1]]);
#         proof.B_p = Pairing.G1Point(b_p[0], b_p[1]);
#         proof.C = Pairing.G1Point(c[0], c[1]);
#         proof.C_p = Pairing.G1Point(c_p[0], c_p[1]);
#         proof.H = Pairing.G1Point(h[0], h[1]);
#         proof.K = Pairing.G1Point(k[0], k[1]);
#         uint[] memory inputValues = new uint[](input.length);
#         for(uint i = 0; i < input.length; i++){
#             inputValues[i] = input[i];
#         }
#         if (verify(inputValues, proof) == 0) {
#             emit Verified("Transaction successfully verified.");
#             return true;
#         } else {
#             return false;
#         }
#     }
# }
