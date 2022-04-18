# line-diagrams
Generates line diagrams like [those in my gallery](https://nate.mrvichin.com/line-diagrams/).

![sample](/sample.jpg)

# introduction
I thought [Mathologer's video about Tesla's 3-6-9 and vortex math](https://www.youtube.com/watch?v=6ZrO90AI0c8) was cool. As a spoiler for the question is this the key to the universe, no. No, this is not. I didn't know it needed a key. Was it locked? I had to make one of these a 240-7417 diagram since, when I saw that one in the Mathologer video, that was when I knew I had to write Python code to make a lot of these.

# packages
This requires `matplotlib` and utilizes `cycler` for color palettes.

# run the script
`colors` is a color pallette.

```
colors = ['#d62828', '#f77f00', '#fcbf49', '#eae2b7']
```

`line_width` is set to 0.01 unless otherwise specified.

An image subdirectory is created in the same folder as the script for the images. To run the code.

```
colors = ['#d62828', '#f77f00', '#fcbf49', '#eae2b7']

ld = LineDiagram()

ld.new_diagram(multiplier=240,
               modulus=7417,
               colors=colors)
```

The code is set to render matplotlib figsizes of 4, 6, 8, and 11.
