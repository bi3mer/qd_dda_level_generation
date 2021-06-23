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
pypy3 main.py --help
```

If you are doing a full run where you are confident that the code is going to work, then PyPy can be made a bit faster with the -O flag before `main.py`.

## Note To Self

`TheGoodStuff` folder needs to be renamed to something sensible. 