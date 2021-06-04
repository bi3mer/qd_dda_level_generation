# QD DDA Level Generation

## Assets

Text files in [MarioLevels](./MarioLevels) and [IcarusLevels](./IcarusLevels) come from [The VGLC](https://github.com/TheVGLC/TheVGLC).

## To Run

Setup submodules if you have not already.

```bash
git submodule init
git submodule update
```

I recommend using [PyPy3](https://www.pypy.org/) otherwise it will take a pretty longtime to run.

```bash
pypy3 main.py --mario # run Mario pipeline
pypy3 main.py --dungeongram # run DungeonGrams pipeline
```

## Note To Self

`TheGoodStuff` folder needs to be renamed to something sensible. 