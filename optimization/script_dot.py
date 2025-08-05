import numpy as np
import line_profiler

n = 100_000
ARR = np.random.default_rng(seed=8675309).integers(10, size=(2, n))


@line_profiler.profile
def my_func(input_array):
    """Compute the dot product of an array with its transpose."""
    result = input_array @ input_array.T
    return result


if __name__ == "__main__":
    np.testing.assert_array_equal(
        my_func(ARR),
        np.array([[2842216, 2016906], [2016906, 2840381]]),
    )
