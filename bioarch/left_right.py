#!/usr/bin/env python


import inspect
from statistics import mean


def best_effort_avg(left, right):
    if left is None:
        return right
    if right is None:
        return left

    if isinstance(left, int):
        return int(mean((left, right)))

    if isinstance(left, float):
        return mean((left, right))

    if hasattr(left, 'avg') and inspect.isfunction(left.avg):
        arg_spec = inspect.getfullargspec(left.avg)
        if len(arg_spec.args) != 2:
            raise ValueError
        if arg_spec.args[0] == 'self':
            raise ValueError
        if arg_spec.varargs is not None:
            raise ValueError
        if arg_spec.varkw is not None:
            raise ValueError
        return left.avg(left, right)

    arg_spec = inspect.getfullargspec(left.__init__)
    if arg_spec.varargs is not None:
        raise ValueError
    if arg_spec.varkw is not None:
        raise ValueError

    avg_args = []
    for key in arg_spec.args[1:]:
        if key.startswith('_'):
            key = key[1:]
        left_val = getattr(left, key)
        right_val = getattr(right, key)
        avg = best_effort_avg(left_val, right_val)
        avg_args.append(avg)
    return left.__class__(*avg_args)


class LeftRight(object):
    """Wrapper around measurements taken on both the left and right sides.
    This augments the two measurements by adding a meta-measurement with the "avg"/"best" combination of both."""

    __slots__ = ['left', 'right']

    def __init__(self, left, right):
        if type(left) != type(right) and left is not None and right is not None:  # pylint: disable=C0123
            raise ValueError(f'Left and right types not the same: left="{type(left)}", left="{type(right)}"')
        self.left = left
        self.right = right

    def avg(self):
        """meta-measurement with the "avg"/"best" combination of both."""
        return best_effort_avg(self.left, self.right)

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) != type(self):  # pylint: disable=C0123
            raise NotImplementedError
        return ((self.left, self.right) == (other.left, other.right))  # pylint: disable=C0325

    def __repr__(self):
        return f'{self.__class__.__name__}({self.left}, {self.right})'

    def __str__(self):
        return f'left: "{self.left}", right: "{self.right}")'


if __name__ == "__main__":
    raise RuntimeError('No main available')
