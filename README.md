# ftx-screener

This is a simple python script that scans FTX futures markets and gives you the futures with the highest by abs value funding rate (for perpetual contracts), or the futures with the highest by abs value premiums (for dated futures)

## Prerequisites

You need `pandas` and `requests` installed to run the screener

## Configuration 

Set the `future_code` to a desired date
Example: to screen futures expiring on March 24 you need to set the `future_code` to `0324`

## Running

`python main.py diff` for dated futures premiums
`python main.py funding` for perpetual futures funding ratess
