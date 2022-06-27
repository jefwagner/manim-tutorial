## Manim Tutorial

This repo holds a practice `.py` file to create scenes using the [Manim](https://docs.manim.community/en/stable/) python based animation tool. 

This file creats scenes that:
* Render equations using latex
* Creating a graph and shading the area for an integral
* Moving the camera around a scene
* Moving an obect around a scene
* Defining an using a custom color pallet
* Loading in a drawing an SVG
* Animating an SVG between 'frames'

To render any of the scenes in low quality (480p 15 fps)[1] install manim[2] and run
```
> python -m manim -ql scene.py <SCENE_NAME>
```
where `<SCENE_NAME>` is replaced with the scene name in the `scene.py` file. The rendered videos are placed somewhere deep within the media folder.

[1] You can find instructions for installing manim in the [Installation](https://docs.manim.community/en/stable/installation.html) page of the documention.

[2] A list of more command line flags and some other examples are available in the [Configuration](https://docs.manim.community/en/stable/tutorials/configuration.html) page of the documentation. 
