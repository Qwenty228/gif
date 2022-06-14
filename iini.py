from tkinter.tix import Tree
import pygame as pg
import numpy as np
import os, sys
import asyncio


pg.init()

def greyscale(surface):
    arr = pg.surfarray.pixels3d(surface)
    mean_arr = np.dot(arr[:,:,:], [0.216, 0.587, 0.144])
    mean_arr3d = mean_arr[..., np.newaxis]
    new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
    return pg.surfarray.make_surface(new_arr)  #, new_arr

def ascale(surface):
    arr = pg.surfarray.pixels3d(surface)
    mean_arr = np.dot(arr[:,:,:], [0.216, 0.587, 0.144])
    return mean_arr #pg.surfarray.make_surface(new_arr), new_arr

def tint(surf, tint_color):
    """ adds tint_color onto surf.
    """
    surf = surf.copy()
    '''overlay = pg.Surface(surf.get_size(), pg.SRCALPHA, 32)
    r,g,b = tint_color
    a = 200
    overlay.fill((r, g, b, a))
    surf.blit(overlay, (0, 0))'''
    surf.fill(tint_color[0:3] + (0, ), None, pg.BLEND_RGBA_ADD)
    surf.fill(tint_color[0:3] + (0, ), None, pg.BLEND_RGBA_MULT)
    return surf


progress = 0



async def create_image(*file: str, sp: int=20, bp: int=50):
    """
    creating image inside image
    [file] first one is background and second one is pixel
    """
    image = pg.image.load(file[0])

    IMAGE_SIZE = image.get_size()
    big_image_pixel = bp if bp != 0 else max(IMAGE_SIZE)

    w, h = [int(big_image_pixel*x/max(IMAGE_SIZE)) for x in IMAGE_SIZE]
    big_img =  pg.transform.scale(image.copy(), (big_image_pixel, big_image_pixel))

    img_arr = pg.surfarray.pixels3d(big_img)

    

    

    if len(file) > 1:
        s = pg.image.load(file[1])
        small_image_pixel = sp if sp != 0 else max(s.get_size())
        small_img = pg.transform.scale(s, (small_image_pixel, small_image_pixel))
    else:
        small_image_pixel = sp if sp != 0 else max(IMAGE_SIZE)
        small_img = pg.transform.scale(image.copy(), (small_image_pixel, small_image_pixel))

    ARR = pg.Surface((w*small_image_pixel, h*small_image_pixel))

    global progress
    for x in range(w):
        for y in range(h):
            #surf = tint(greyscale(small_img.copy()), img_arr[x, y])
            
            surf = tint(small_img.copy(), img_arr[x, y])
            ARR.blit(surf, (x*small_image_pixel, y*small_image_pixel))
            await asyncio.sleep(0)
        progress = round(100*((x+1)/w))
        _, tail = os.path.split(file[0])

    pg.image.save(ARR, f'results/result_{tail}')
        
async def counting():
    while True:
        print(progress)
        await asyncio.sleep(0.05)


async def main():
    done, pending = await asyncio.wait([create_image(os.path.join('images', 'chi2.png'), sp=20, bp=20, infi=True), counting()], return_when=asyncio.FIRST_COMPLETED)
    print(done)

if __name__ == "__main__":
    asyncio.run(main())