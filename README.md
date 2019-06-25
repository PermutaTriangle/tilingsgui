# GUI FOR TILINGS

## RUN:

python main.py basis

Example: python main.py 1234_1324

## CONTROLS:

- Left/right to switch strategies, strategy is visible in window title
- Left click to apply strategy at mouse position (right click for obstruction in cell insertion)
- Backspace to go back (pop the stack)
- Escape to close

## macOS Mojave
There are issues on Mojave with PyGame. Install with these steps (uninstall pygame first if you have it)

1. brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf
2. cd python3.7.2/lib/python3.7/site-packages   (Note: you can find the site packages directory with python -m site)
3. git clone https://github.com/pygame/pygame.git
4. cd pygame
5. python setup.py -config -auto -sdl2
6. python setup.py install


