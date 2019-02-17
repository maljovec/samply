import samply.directional


def normal(self, count=1, dimensionality=2):
    return np.clip(
        np.random.normal(loc=0.5, scale=0.15, size=(count, dimensionality)),
        0,
        1,
    )


def shell(count=1, dimensionality=2):
    directions = samply.directional.uniform(count, dimensionality)
    r = np.random.uniform(low=0.5, high=1, size=(count, 1))
    X = ((r * directions) + 1) / 2.
    return X


def concentric_shells(count=1, dimensionality=2, levels=2, gap_ratio=0.4):
    a = np.random.choice(a=range(levels), size=count)
    width = 1 / (levels * (gap_ratio + 1))
    gap = width * gap_ratio
    low = gap
    r = np.zeros(size=(count, 1))
    for i in range(levels):
        high = low + width
        mask = np.where(a == i)[0]
        r[mask] = np.random.uniform(low=low, high=high, size=(len(mask), 1))
        low = high + gap

    directions = samply.directional.uniform(count, dimensionality)
    X = ((r * directions) + 1) / 2.
    return X


def cross(count=1, dimensionality=2):
    sgn = np.random.choice(a=[False, True], size=(count, dimensionality - 1))
    low = 0.2
    high = 0.8
    x = np.random.uniform(low=low, high=high, size=(count, 1))
    y = x + np.random.uniform(
        low=-0.1, high=0.1, size=(count, dimensionality - 1)
    )
    y[sgn] = 1 - y[sgn]
    X = np.hstack((x, y))
    return X


def curve(count=1, dimensionality=2):
    low = 0.05
    high = 0.95
    x = np.random.uniform(low=low, high=high, size=(count, 1))
    y = (
        x
        + 0.5 * np.sin(2 * np.pi * x)
        + np.random.uniform(
            low=-0.1, high=0.1, size=(count, dimensionality - 1)
        )
    )
    X = np.hstack((x, y))
    return X


def stripes(count=1, dimensionality=2):
    b = np.random.choice(a=[-0.5, 0.0, 0.5], size=(count, 1))
    low = 0.0
    high = 0.5
    x = np.random.uniform(low=low, high=high, size=(count, 1))
    mask = np.where(b < 0)[0]
    low = 0.6
    high = 0.8
    x[mask] = np.random.uniform(low=low, high=high, size=(len(mask), 1))
    mask = np.where(b > 0)[0]
    low = 0.2
    high = 0.5
    x[mask] = np.random.uniform(low=low, high=high, size=(len(mask), 1))
    eps = np.random.uniform(
        low=-0.05, high=0.05, size=(count, dimensionality - 1)
    )
    y = np.clip(x + eps + b, 0, 1)
    X = np.hstack((x, y))
    return X


def distinct_mixture(count, dimensionality):
    a = np.random.choice(a=[0, 1, 2], size=count)
    cov = 0.00125 * np.eye(dimensionality)
    mean = 0.25 * np.ones(dimensionality)
    X = np.clip(np.random.multivariate_normal(mean, cov, size=count), 0, 1)
    mask = np.where(a == 1)[0]
    mean = 0.5 * np.ones(dimensionality)
    X[mask] = np.clip(
        np.random.multivariate_normal(mean, cov, size=len(mask)), 0, 1
    )
    mask = np.where(a == 2)[0]
    mean = 0.75 * np.ones(dimensionality)
    # Set every other dimension to 0.25
    mean[1::2] = 0.25
    X[mask] = np.clip(
        np.random.multivariate_normal(mean, cov, size=len(mask)), 0, 1
    )
    return X


def overlap_mixture(count, dimensionality):
    a = np.random.choice(a=[0, 1, 2], size=count)
    mean = 0.5 * np.ones(dimensionality)
    cov = 0.0125 * np.eye(dimensionality)
    X = np.clip(np.random.multivariate_normal(mean, cov, size=count), 0, 1)
    mask = np.where(a == 1)[0]
    mean = 2. / 3. * np.ones(dimensionality)
    cov = 0.001 * np.eye(dimensionality)
    X[mask] = np.clip(
        np.random.multivariate_normal(mean, cov, size=len(mask)), 0, 1
    )
    mask = np.where(a == 2)[0]
    mean = 1. / 3. * np.ones(dimensionality)
    cov = 0.001 * np.eye(dimensionality)
    X[mask] = np.clip(
        np.random.multivariate_normal(mean, cov, size=len(mask)), 0, 1
    )
    return X
