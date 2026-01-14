# Billard
Numerical simulation of a billiard

## dependencies: 
```bash
uv
```

## Installation 

```bash
uv sync
```

Better if you use uv and if you always want to use the defined `PYTHONPATH`
```bash
touch .env && echo PYTHONPATH=\"$PWD\" > .env
```

```bash
uv run python main.py --mode=<US|FR>
# For the FR version
uv run python main.py --mode=FR
# For the US version
uv run python main.py --mode=US
```

With those command you'll be able to launch any version of the Billiard simulation
