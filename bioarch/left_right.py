#!/usr/bin/env python


import inspect
from statistics import mean
from typing import Any, cast, Generic, List, Optional, TypeVar


T = TypeVar('T')


def best_effort_avg(left: Optional[T], right: Optional[T]) -> Optional[T]:
    if left is None:
        return right
    if right is None:
        return left

    if isinstance(left, int):
        if not isinstance(right, int):
            raise TypeError
        return cast(T, int(mean((left, right))))

    if isinstance(left, float):
        if not isinstance(right, float):
            raise TypeError
        return cast(T, mean((left, right)))

    if right.__class__ != left.__class__:
        raise TypeError
    type_class = left.__class__

    if hasattr(type_class, 'avg') and inspect.isfunction(getattr(type_class, 'avg')):
        avg_func = getattr(type_class, 'avg')
        arg_spec = inspect.getfullargspec(avg_func)
        if len(arg_spec.args) != 2:
            raise ValueError
        if arg_spec.args[0] == 'self':
            raise ValueError
        if arg_spec.varargs is not None:
            raise ValueError
        if arg_spec.varkw is not None:
            raise ValueError
        return cast(T, avg_func(left, right))

    arg_spec = inspect.getfullargspec(type_class)
    if arg_spec.varargs is not None:
        raise ValueError
    if arg_spec.varkw is not None:
        raise ValueError

    avg_args: List[Any] = []
    for key in arg_spec.args[1:]:
        if key.startswith('_'):
            key = key[1:]
        left_val = getattr(left, key)
        right_val = getattr(right, key)
        avg = best_effort_avg(left_val, right_val)
        avg_args.append(avg)
    return type_class(*avg_args)  # type: ignore


class LeftRight(Generic[T]):
    """Wrapper around measurements taken on both the left and right sides.
    This augments the two measurements by adding a meta-measurement with the "avg"/"best" combination of both."""

    __slots__ = ['left', 'right']

    def __init__(self, left: Optional[T], right: Optional[T]):
        if type(left) != type(right) and left is not None and right is not None:  # pylint: disable=C0123
            raise ValueError(f'Left and right types not the same: left="{type(left)}", left="{type(right)}"')
        self.left: Optional[T] = left
        self.right: Optional[T] = right

    def avg(self) -> Optional[T]:
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
