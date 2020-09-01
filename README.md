# pycoin

This is a repo with the purpose of automatically monitoring multiple crypto currencies of interest for you and make automatic trades so you buy when the currency start climbing or sell before you are loosing too much. The main purpose would not be to have a predictive model that will allow you know before hand when to buy/sell, but to constantly have a watcher of the state of the market, increase your earnings, but most importantly, reduce the losses.

## Objectives

- Gather historic and real time data from at least one source.
- Create a STOP LOSS, i.e. set a % that you are comfortable selling after the trending of the currency is down. Eg, say that you have one currency with a current value of $10 and you set the STOP LOSS to 0.5%, then the lower limit will be 10-0.05=9.5. The currency start increasing and reach 15, the lower limit would then be 15-(15*0.5/100). If the value goes up, the lower limit goes up as well, but if it goes down, it will stay the same. If the value of the currency goes below that limit, the system sells.
- Study and test different algorithms that can allow us stablish short term tendencies to decide if it's appropriate to buy or sell. We can tests these algorithms with different parameters, including the window in which the tests are being done, and determine if they are worth using.
- Investigate for correlations of different variables that might be helpful to the decision making process.
- Determine helpful trendings and variables. One that I have found that is often accurate with what is happening in real time is the ratio of all the book's buys and sells at one time. When this ratio goes up, the chances of that trending following the same behaviour seem to be higher (when number of buys are >> number of sells, then the currency tends to go up, and viceversa).
- Investigate and test different models with different number of data points and time range.
- Create a wrapper for the different Wallets that we decide to use. The first one will be my current one: Coinbase Pro.
- Create a constant watch for ALL the coins that you have in your account (Maybe have a web socket for all the coins and have the processes and analysis running in paralel ¯\_(ツ)_/¯).
- Be able to buy/sell based on the implemented logic.
- Have the system running in a server (currently on a Raspberry Pi). If there are algorithms that need more resources, then the system will meet the Cloud! The part of the sysmem that manages the account can probably stay in the Raspi and the heavier tasks can run on the Cloud. If the system evolves in a way that we need to divide the system, then we can create another API for that purpose using Flask.
- Determine if a database is needed to store the information.
- Have an alerting system that will let me know when subscribed important alerts.


### Environment Requirements

- `ALPHAVANTAGE_KEY`: Key given by AlphaVantage to access to the API
- `CB_API_SECRET`: Secret provided by Coinbase Pro
- `CB_ACCESS_KEY`: Key provided by Coinbase Pro
- `CB_ACCESS_PASSPHRASE`: Pass phrase generated in Coinbase Pro
- `COINBASE_PRO_SANDBOX`: Set to 1 to use Sandbox

### Installing executable

```
$ virtualenv venv
$ . venv/bin/activate
$ pip install --editable .

$ pycoin --help
```
