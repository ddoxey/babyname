# BabyName

Lookup SSA popular baby names

The SSA doesn't seem do mind everyone scraping their popular baby name
database.

```
https://www.ssa.gov/OACT/babynames/index.html
```

This module makes it convenient to do quick lookups on baby names. The
results are cached in the user's home directory to improve performance
on repetitive lookups.

# Usage

```
    from babyname import BabyName

    bn = BabyName()

    result = bn.lookup('George', 1980, 'male')
```

The result will look something like:
```
    {'name': 'George',
     'rankings': [{'rank': 133, 'year': 2020},
                  {'rank': 119, 'year': 2019},
                  {'rank': 127, 'year': 2018}],
     'sex': 'Male',
     'start': '2018'}
```
