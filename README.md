# Swapmania
Swapmania is a cellular automata, aka a 0-player game. This one consists of swapping cells around and has a variety of cells already. They are:
- Swapper: This cell swaps itself with the cell in front of it.
- Cycle clockwise/counterclockwise: This cell cycles the cells around it, like the ridges of a gear. It also rotates the cells.
- Rotate clockwise/counterclockwise: This cell rotates the cells around it.
- Normal: Does nothing, and can be swapped in any way.
- Slide: Like the normal cell, but can only move either horizontally or vertically, depending on the rotation
- Immovable: Cannot be moved. These can serve as borders.
- Duplicate: Duplicates the cell behind it, putting it in front of it. If there is something in front of it, then it replaces that cell.
- Trash: Deletes any cell that tries to swap with it.

## Versions
- v1 (Jun 22, 2024): The basic game. It has 9 different types of cells, and is displayed with the console.
- v1.1 (Jun 27, 2024): Adds the trash cell, a cell that deletes a cell if it tries to swap with the cell. Also fixes a generator bug that lets you replace immovable blocks.

## Community
The swapmania game, even though no one really plays it, does have a discord server. You can find it here: https://discord.gg/JEadbF3Ayy.