# qd_dda_level_generation

## To Run

PyPy is used to have the code run quickly but unfortunately it is not compatible with matplotlib. So separate processes of python are run to create the graphs. You'll also need to go into [mario.py](./mario.py) and [dungeongram.py](./dungeongram.py) and assign paths to their level directory. For mario, use [The VGLC](https://github.com/TheVGLC/TheVGLC/tree/0e86a8f31f20ecad4eaa5741ff061af88767f7fb/Super%20Mario%20Bros/Processed).

```
pypy3 mario.py
pypy3 dungeongram.py
```