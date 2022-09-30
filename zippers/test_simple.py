from ..zipper import ( zipper, vector_zipper,
                       up, down, left, right,
                       node, root, replace, edit,
                       insert_left, insert_right)
                       
from pyrsistent  import pmap, pvector, m, v, PMap, PVector
from functools import reduce

def pipe( arg, fs, extra_args=[] ):
    """Executes a function pipe, passing each result as input to the next function.
    
    Given a list of functions [f1, f2, ..., fn], compute f1(args) and pass
    the result to f2, pass that result to f3, and so on, returning the result
    from the call to fn.

    In general, each fi will be either a function or a list [func, *argsi];
    given the result from the previous stage (or args) as result, apply
    func to result and any args in argsi and extra_args in order.

    The list extra_args is passed to every function.
    """
    def rf( result, f ):
        if isinstance(f, list):
            return f[0](result, *(f[1:] + extra_args[:]))
        else:
            return f(result, *extra_args)
    return reduce(rf, fs, arg)      


def test_basic_zipper_moves():
    data = [[1, 2, [3, 30, [300]]], 4, 5]
    z = vector_zipper(data)
    zd2d = pipe(z, [down , [down, 2]])

    out = node(zd2d)
    assert out == [3, 30, [300]]
    assert pipe(zd2d, [left, node]) == 2
    assert pipe(zd2d, [left, right, node]) == out
    # assert node(leftmost(zd2d)) == 1
    # assert node(rightmost(up(zd2d))) == 5

    assert pipe(zd2d, [[down, 2], node]) == [300]
    assert pipe(zd2d, [[down, 2], root]) == data

    assert pipe(zd2d, [[down, 2], down, node]) == 300

    assert pipe(zd2d, [[down, 2], up, node]) == [3, 30, [300]]

    assert node(down(z, 1)) == 4
    
def test_basic_zipper_mods():
    data = [[1, 2, [3, 30, [300]]], 4, 5]
    z = vector_zipper(data)
                        
    assert pipe(z, [down, [replace, 10], root]) == [10, 4, 5]
    assert pipe(z, [[down, 1], [insert_right, 10], left, remove, root]) == [4, 10, 5]
