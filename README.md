Whoosh
=====
A Python game engine for 2D physics games.

Whoosh is based on bindings to OpenGL ([pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home)) and Chipmunk ([pymunk](https://github.com/viblo/pymunk)).

The purpose of the engine is to provide a layer on top of these libraries, creating a more comfortable environment for actually making games in.

The design draws several concepts from the Irrlicht engine used to create [King Arthur's Gold](https://www.kag2d.com/en/), but also from other engines such as [LÖVE](https://love2d.org/) and [Unity](https://unity3d.com/).

An eventual goal is for the engine to offer a complete network syncing system for game objects, so that it is easy to create games are playable by multiple players over the internet.

Main features
-----
* Entity/Component system for game objects
* Module based, extensible engine
* Event based system - components and modules hook into events like `on_render`, `on_tick` etc.
* Sprite animation handling
* User input handling
* Camera implementation with pan & zoom

Dependencies
----
* `pyglet == 1.2.4`
* `pymunk == 5.1.0`
* (For building documentation) `sphinx`

Examples
-----
Run the examples as a module like
```
$ python -m examples.fireball
```

Tests
-----
To run the test bed
```
$ python -m unittest discover tests "*.py"
```
Or use the handy shell script
```
$ bash runtests.sh
```

Contributing
-----
For now all development is done on the `master` branch. 

Feel free to submit a pull request. Ensure that your branch is named like `feature/add_chocolate_cake` and is based on the latest commit on `master`.