import numpy as np

n = 100_000
ARR = np.random.default_rng(seed=8675309).integers(10, size=(2, n))


@profile
def my_func(input_array):
    """Compute the dot product of an array with its transpose."""
    nrow, ncol = input_array.shape
    result = np.zeros((nrow, nrow), dtype=int)
    for rix in range(nrow):
        for cix in range(nrow):
            for eix in range(ncol):
                result[rix, cix] += input_array[rix, eix] * input_array.T[eix, cix]
    return result


if __name__ == "__main__":
    np.testing.assert_array_equal(
        my_func(ARR),
        np.array([[2842216, 2016906], [2016906, 2840381]]),
    )
