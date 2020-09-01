"""Execute processes in the system"""
import click
from coin.coinbase import Coinbase
from coin.alphavantage import AlphaVantage
from coin.coin import Coin


@click.group()
def cli():
    """Communicate with your Crypto Account throgh this CLI"""
    pass

@cli.command()
@click.argument('currency')
def get_rating(currency):
    c = Coinbase(currency)
    crypto = Coin(currency)
    a = AlphaVantage(currency)
    a.get_crypto_rating(crypto)
    click.echo(crypto)

@cli.command()
@click.argument('currency')
def get_current(currency):
    c = Coinbase(currency)
    crypto = c.get_current()
    click.echo(crypto)

@cli.command()
@click.argument('currency')
@click.option('--n_elements', default=1, help='Number of elements to get from historic data')
@click.option('--start', default=None, help='Start date to filter historic data')
@click.option('--end', default=None, help='End date to filter historic data')
@click.option('--granularity', default="1day", help='Set granularity to filter historic data: [1minute, 5minutes, 15minutes, 1hour, 6hours, 1day]')
def get_historics(currency, n_elements, start, end, granularity):
    c = Coinbase(currency)
    cryptos = c.get_historic_rates(start=start, end=end, n_elements=n_elements, gran=granularity)
    for crypto in cryptos:
        click.echo(crypto)

@cli.command()
@click.argument('currency')
@click.argument('date')
def get_value_from_date(currency, date):
    a = AlphaVantage(currency)
    crypto = a.get_value_from_date(date)
    click.echo(crypto)

@cli.command()
@click.argument('currency')
@click.argument('start')
@click.argument('end')
def get_historics_from_alphavantage(currency, start, end):
    a = AlphaVantage(currency)
    cryptos = a.get_historics(start, end)
    for crypto in cryptos:
        click.echo(crypto)


if __name__ == '__main__':
    cli()
