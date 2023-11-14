# FSM for model

## Continuous learning, minimize control error
continually learning model. I don't want to say train, and then deploy. I want every new/ set of new data points to trigger a training from the new data. There is in some sense a control error here of the account growth percentage.

so lets start with basic models to make this easier.

### event driven model needs states:

what is an event? every time a new data point is added, the panel of indicators update, then the indicators must learn from the previous prediction

the account manager will wait until a certain criteria is met, e.g. more than 75% of indicators are positive/negative. 

#### account manager states

completing order - prevent ordering more if the previous order is not coming back complete
await_prediciton - waiting for prediction from indicator
await_data - waiting for api to respond
idle - nothing

#### indicator/model states

up_to_date
behind

training

#### bot states

look at it from outside: I have trading bot