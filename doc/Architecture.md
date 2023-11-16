# FSM for model

## Continuous learning, minimize control error
continually learning model. I don't want to say train, and then deploy. I want every new/ set of new data points to trigger a training from the new data. There is in some sense a control error here of the account growth percentage.

so lets start with basic models to make this easier.

### event driven model needs states:

what is an event? every time a new data point is added, the panel of indicators update, then the indicators must learn from the previous prediction

the bot might just wait until a certain criteria is met, e.g. more than 75% of indicators are positive/negative. 

Parts:

Bot: total state of the model

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

event occurs every hour - price update

bot stores the current total portfolio stored accross all managers

now the bot must look at the indicators and the available trading pairs from the account managers, and decide on opening a trade order with the relevant account manager

the bot can see the prices of many assets and the indicators
the bot must evaluate the risk of the portfolio