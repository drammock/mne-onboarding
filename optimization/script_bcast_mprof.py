import numpy as np

n = 100_000
ARR = np.random.default_rng(seed=8675309).integers(10, size=(2, n))


@profile  # noqa: F821
def my_func(input_array):
    """Compute the dot product of an array with its transpose."""
    nrow, ncol = input_array.shape
    result = np.zeros((nrow, nrow), dtype=int)
    for rix in range(nrow):
        result[rix] = np.sum(input_array[rix][:, np.newaxis] * input_array.T, axis=0)
    return result


if __name__ == "__main__":
    np.testing.assert_array_equal(
        my_func(ARR),
        np.array([[2842216, 2016906], [2016906, 2840381]]),
    )
