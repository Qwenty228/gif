import asyncio
import pygame as pg
import numpy as np
import os, sys
import imageio as iio
from sklearn.manifold import smacof
from iini import greyscale




progress = 0

def tint(surf, tint_color):
    """ adds tint_color onto surf.
    """
    surf = surf.copy()
    surf.fill(tint_color[0:3] + (0, ), None, pg.BLEND_RGBA_MULT)
    return surf



async def create_gif(*file:str,  sp: int=20, bp: int=50):
    im = iio.get_reader(file[1])
    frames = []
    _, tail = os.path.split(file[1])
    writer = iio.get_writer(f"results/result_{tail}", fps=12)


    if file[0].endswith('.gif'):
        im2 = iio.get_reader(file[0])
    else:
        image = pg.image.load(file[0])

        IMAGE_SIZE = image.get_size()
        big_image_pixel = bp if bp != 0 else max(IMAGE_SIZE)

        w, h = [int(big_image_pixel*x/max(IMAGE_SIZE)) for x in IMAGE_SIZE]
        big_img =  pg.transform.scale(image.copy(), (big_image_pixel, big_image_pixel))

        img_arr = pg.surfarray.pixels3d(big_img)

    p = 0
    global progress
    for i, frame in enumerate(im):
        if i > 5:
            break
        
        
        if file[0].endswith('.gif'):
            image = pg.surfarray.make_surface(np.flip(np.rot90(list(im2)[i][:,:,:3], 3) ))
            IMAGE_SIZE = image.get_size()
            big_image_pixel = bp if bp != 0 else max(IMAGE_SIZE)

            w, h = [int(big_image_pixel*x/max(IMAGE_SIZE)) for x in IMAGE_SIZE]
            big_img =  pg.transform.scale(image.copy(), (big_image_pixel, big_image_pixel))

            img_arr = pg.surfarray.pixels3d(big_img)
            




        img = pg.surfarray.make_surface(np.flip(np.rot90(frame[:,:,:3], 3) ))
        
        small_image_pixel = sp if sp != 0 else max(img.get_size())
        
        small_img = pg.transform.scale(img, (small_image_pixel, small_image_pixel))
    
        ARR = pg.Surface((w*small_image_pixel, h*small_image_pixel))

        for x in range(w):
            for y in range(h):
                if 50 <= sum(img_arr[x, y]):
                    surf = tint( greyscale(small_img.copy()), img_arr[x, y])
                    ARR.blit(surf, (x*surf.get_width(), y*surf.get_height()))
                await asyncio.sleep(0)
            p += 1
            progress = round(100*(p/(6*w)))

        frames.append(ARR)

        arr = pg.surfarray.pixels3d(ARR)
        
        writer.append_data(np.rot90(arr, 3)[...,::-1,:])

    writer.close()



        
async def counting():
    while True:
        print(progress)
        await asyncio.sleep(0.05)


async def main():
    done, pending = await asyncio.wait([create_gif(os.path.join('images', 'amogus.gif'), os.path.join('images', "ada.jpg"), 20, 100), counting()], return_when=asyncio.FIRST_COMPLETED)
    print(done)

if __name__ == "__main__":
    asyncio.run(main())