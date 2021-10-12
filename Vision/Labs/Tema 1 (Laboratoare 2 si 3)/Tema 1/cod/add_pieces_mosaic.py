from parameters import *
import numpy as np
import pdb
import timeit
import random

def get_mean_color_small_images(params: Parameters, c):
    N, H, W, C = params.small_images.shape
    mean_color_pieces = np.zeros((N, c))
    
    for i in range(N):
        cnt_img = params.small_images[i].copy()
        for ch in range(c):
            mean_color_pieces[i, ch] = np.float32(cnt_img[:,:,ch].mean())

    return mean_color_pieces

def get_sorted_distances(mean_color_patch, mean_color_pieces):
    dist = np.sum((mean_color_pieces - mean_color_patch) ** 2, axis=1)
    return np.argsort(dist)

def add_pieces_grid(params: Parameters):
    start_time = timeit.default_timer()
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape
    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal

    if params.criterion == 'aleator':
        for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
                indx = random.randint(0, len(params.small_images) - 1)
                img = params.small_images[indx]
                img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = img
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))

    elif params.criterion == 'distantaCuloareMedie':
        mean_color = get_mean_color_small_images(params, c)
        for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
                cnt_patch = params.image_resized[i * H : (i + 1) * H, j * W : (j + 1) * W, :]
                mean_clr = np.mean(cnt_patch, axis=(0, 1))
                sorted_indices = get_sorted_distances(mean_clr, mean_color)
                idx = sorted_indices[0]

                img_mosaic[i * H : (i + 1) * H, j * W : (j + 1) * W, :] = params.small_images[idx]
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j) / num_pieces))
    else:
        print('Error! unknown option %s' % params.criterion)
        exit(-1)

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return img_mosaic


def add_pieces_random(params: Parameters):
    start_time = timeit.default_timer()
    N, H, W, C = params.small_images.shape
    h, w, c = params.image_resized.shape
    img_mosaic = np.zeros((h + H, w + W, c), np.uint8)
    mean_color_pieces = get_mean_color_small_images(params, c)
    bigger_image = np.zeros((h + H, w + W, c), np.unit8)
    bigger_image[:-H, :-W, :] = params.image_resized.copy()
    free_pixels = np.ones((img_mosaic.shape[0], img_mosaic.shape[1]), dtype=np.int32)

    for i in range(free_pixels.shape[0]):
        for j in range(free_pixels.shape[1]):
            free_pixels[i][j] = i * free_pixels.shape[1] + j

    free_pixels[h:, :] = -1
    free_pixels[:, w:] = -1

    while True:
        f = free_pixels[free_pixels>-1]
        if (len(f) == 0):
            break

        index = np.random.randint(low=0, high=len(f), size=1)
        row = int(f[index]/free_pixels.shape[1])
        col = int(f[index]% free_pixels)
        patch=bigger_image[row:row+H,col:col+W,:]




    end_time = timeit.default_timer()
    print('running time:', (end_time - start_time), 's')
    return None


def add_pieces_hexagon(params: Parameters):
    start_time = timeit.default_timer()
    end_time = timeit.default_timer()
    print('running time:', (end_time - start_time), 's')
    return None
