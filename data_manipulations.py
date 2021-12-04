import numpy as np

# all mappings are done because sometimes numpy stores numbers as strings


def arrayofgradients(dataset):
    # all the ints are meant to prevent typeerror
    dataset = list(map(float, dataset))
    dataset = list(map(int, dataset))
    hr_grad_8 = [(dataset[z] - dataset[int(z) - 8]) / 8 for z in range(int(len(dataset)))]
    hr_grad_5 = [(dataset[z] - dataset[int(z) - 5]) / 5 for z in range(int(len(dataset)))]  # average over previous hours
    hr_grad_3 = [(dataset[z] - dataset[int(z) - 3]) / 3 for z in range(int(len(dataset)))]
    hr_grad_2 = [(dataset[z] - dataset[int(z) - 2]) / 2 for z in range(int(len(dataset)))]
    hr_grad_1 = [(dataset[z] - dataset[int(z) - 1]) for z in range(len(dataset))]
    return np.array([hr_grad_1, hr_grad_2, hr_grad_3, hr_grad_5, hr_grad_8])


def distance_to_prev_high(dataset):  # referring to price difference, input price here
    dataset = list(map(float, dataset))
    dataset = list(map(int, dataset))
    previous_high = dataset[0]
    dist_high = np.array([]).reshape(0, 1)
    for item in dataset:
        if item > previous_high:
            previous_high = item
        dist_high = np.vstack([dist_high, [previous_high - item]])
    return dist_high


def ratios(item1, item2, item3):
    ratio1 = item1 / item2
    ratio2 = item1 / item3
    ratio3 = item2 / item3
    return np.array([ratio3, ratio1, ratio2])


def add_simple_moving_averages(crypto_df):
    crypto_df['close_SMA_5'] = crypto_df['close'].rolling(5).mean()
    crypto_df['close_SMA_8'] = crypto_df['close'].rolling(8).mean()
    crypto_df['close_SMA_13'] = crypto_df['close'].rolling(13).mean()
    return crypto_df


def conv_df_to_arrays(crypto_df, bitcoin_df):
    # get arrays for each column of interest
    price = np.array(crypto_df['open'].to_list())
    volume = np.array(crypto_df['volume'].to_list())
    SMA_5 = np.array(crypto_df['close_SMA_5'].to_list())
    SMA_8 = np.array(crypto_df['close_SMA_8'].to_list())
    SMA_13 = np.array(crypto_df['close_SMA_13'].to_list())
    bitcoin_price = np.array(bitcoin_df['open'].to_list())
    return price, volume, SMA_5, SMA_8, SMA_13, bitcoin_price
