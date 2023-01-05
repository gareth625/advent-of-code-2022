from typing import List, Union


def partition(size: int, xs: Union[List, str]) -> List:
    return [xs[i: i+size] for i in range(len(xs))]
