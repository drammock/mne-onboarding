import numpy as np

n = 10_000_000
ARR = np.random.default_rng(seed=8675309).integers(10, size=(2, n))


def my_func(input_array):
    """Compute the dot product of an array with its transpose."""
    nrow = input_array.shape[0]
    result = np.empty((nrow, nrow), dtype=int)
    for rix in range(nrow):
        for cix in range(nrow):
            result[rix, cix] = np.sum(input_array[rix] * input_array.T[:, cix])
    return result


if __name__ == "__main__":
    print(my_func(ARR))
