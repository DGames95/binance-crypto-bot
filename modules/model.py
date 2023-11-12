# contains all code regarding training and predictions using the neural net
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, BatchNormalization
import time
from os import listdir
from sklearn.preprocessing import StandardScaler
from data_manipulations import arrayofgradients, ratios, distance_to_prev_high, add_simple_moving_averages, conv_df_to_arrays


def define_model(shape):
    # commented layers mean testing different complexities
    model_definition = Sequential()
    model_definition.add(LSTM(50, input_shape=(1, shape), return_sequences=True))
    model_definition.add(Dropout(0.2))
    model_definition.add(BatchNormalization())

    model_definition.add(LSTM(50, return_sequences=True))
    model_definition.add(Dropout(0.2))
    model_definition.add(BatchNormalization())

    model_definition.add(LSTM(50))
    model_definition.add(Dropout(0.2))
    model_definition.add(BatchNormalization())

    model_definition.add(Dense(1, activation='sigmoid'))

    return model_definition


def prep_data_model(crypto_df, bitcoin_df):
    # export X and Y every time for simplicity
    # X = array of input arrays, Y = 1 if crypto price goes up, 0 if price goes down in the next hour

    # add 3 different SMAs to the dataframe
    crypto_df = add_simple_moving_averages(crypto_df)

    # convert the useful dataframe columns to numpy arrays
    price, volume, SMA_5, SMA_8, SMA_13, bitcoin_price = conv_df_to_arrays(crypto_df, bitcoin_df)

    # create inputs
    price_grad = arrayofgradients(price).T
    volume_grad = arrayofgradients(volume).T
    SMA_ratios = ratios(SMA_5, SMA_8, SMA_13).T
    dist_high_tensor = distance_to_prev_high(price)
    price_tensor = price.reshape(len(price), 1)
    bitcoin_ratio = np.array([]).reshape((0, 1))
    for i in range(len(price)):
        ratio = float(bitcoin_price[i]) / float(price[i])
        bitcoin_ratio = np.vstack([bitcoin_ratio, ratio])

    amount_inputs = 11  # specify here the number of input values as it is used later to shape the input arrays

    # turn data into standardized input (X), output (y)
    X = np.array([]).reshape((0, amount_inputs))
    Y = np.array([]).reshape((0, 1))

    num_hours_predict = 1  # number of hours into the future to predict up or down
    for i in range(len(price_grad)):
        input_line = np.concatenate((price_tensor[i], SMA_ratios[i],
                                     price_grad[i], dist_high_tensor[i],  # volume_grad[i],
                                     bitcoin_ratio[i]), axis=0)
        X = np.vstack([X, input_line])

        if i >= len(price_grad) - num_hours_predict:  # because no n+1 for current data point
            continue
        elif price[i + num_hours_predict] > price[i]:
            Y = np.vstack([Y, 1])
        else:
            Y = np.vstack([Y, 0])

    X = X[:-num_hours_predict]  # because we have no prediction for current datapoint we can't train last row
    scaler = StandardScaler()  # standardize

    # returning X_scaled, and Y
    return scaler.fit_transform(X), Y


def predict(ticker, X_scaled):
    # load the model, choose the most recent model
    models_available = listdir('C:/Users/damia/OneDrive/Desktop/Python Projects/Crypto Analysis/models')
    print('\nusing model: ' + models_available[-1] + ', making prediction...')
    model_name = models_available[-1]
    model = keras.models.load_model(f'C:/Users/damia/OneDrive/Desktop/Python Projects/Crypto Analysis/models/{model_name}')

    recent_values = X_scaled[-119:-1]
    # reshape here because predictions need a 3d input, for some reason
    recent_values = recent_values.reshape(recent_values.shape[0], 1, recent_values.shape[1])

    # use the model to make a prediction
    # we input the whole data set and then take the final most recent prediction
    prediction = model.predict(recent_values)
    # print(prediction)
    return prediction[-1][0]


def train_model(ticker, X_scaled, Y):
    # now split into a training and an evaluation set
    # 96 days = 4 days of 24 hours
    num_hours = 96

    X_train = X_scaled[-num_hours:-int(num_hours * 0.2)]
    Y_train = Y[-num_hours:-int(num_hours * 0.2)]
    X_evaluate = X_scaled[-int(num_hours * 0.2):]
    Y_evaluate = Y[-int(num_hours * 0.2):]

    # define LSTM Keras model
    # this is to give the correct input for an LSTM layer
    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_evaluate = X_evaluate.reshape(X_evaluate.shape[0], 1, X_evaluate.shape[1])

    model = define_model(X_train.shape[2])

    # compile and test the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X_train, Y_train, validation_data=(X_evaluate, Y_evaluate), epochs=200, batch_size=24)
    _, accuracy = model.evaluate(X_evaluate, Y_evaluate)

    # save the model to be loaded later on, with the time created
    name = f'{ticker}_price_predictor,{time.time()}'
    model.save(f'C:/Users/damia/OneDrive/Desktop/Python Projects/Crypto Analysis/models/{name}.h5')
    print('Accuracy: %.2f' % (accuracy * 100))
