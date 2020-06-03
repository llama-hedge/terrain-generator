# terrain-generator
A program that procedurally generates maps of terrain.

The process by which the terrain is generated is as follows:

1) OpenSimplex noise is used to create the starting terrain. Noise-based terrain is common but has several shortcomings, notably a lack of mountain ranges and rivers, and a tendency to look blobby and unrealistic on large scales. Despite this, it is an acceptable starting point which can be modified to look more realistic.

2) Sea level is established such that the desired percentage of the map's surface is water.

3) Noise-based terrain has a tendency to produce the wrong distribution of island sizes, so some islands are sunk by inverting their topography. This process always preserves the largest continent.

4) Mountain ranges are added. The way this is done is by identifying a random selection of land masses and then for each land mass chosen:
  - temporarily shift the sea level slightly up or down (the selection is done twice, once moving the sea level up to move the island borders inland and make inland mountain ranges, and again moving the sea level down to make offshore ones)
  - redetermine the island's boundaries according to the new sea level
  - offset the position of that island by a random amount and in a random direction
  - take a sliver of area that is on land for the island in its original position, but not for the offset island. This shape is a random edge of the island.
  - reduce the edge to a line, then blur and distort that line
  - add the line to the original heightmap

After each stage in the process, the heightmap is saved as a csv file.

The generator currently has a tendency to produce maps with an unrealistically high number of inland seas. These do exist in real life, but are uncommon. The plan is to add a new step where rivers are added to join some of these inland seas to the main ocean, and fill in the rest. Realistic rivers are a relatively hard problem in procedural generation become most terrain generation relies Perlin noise or something similar, which tends to create blob-shaped structures rather than line-shaped ones.
