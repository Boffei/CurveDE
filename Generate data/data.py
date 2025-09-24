import os
import numpy as np
import matplotlib.pyplot as plt


def curve_func(x, y0, A1, t1, A2, t2):
    return y0 + A1*(1 - np.exp(-x/t1)) + A2*(1 - np.exp(-x/t2))


x = np.linspace(0, 35, 70)


y0_range = (55, 85)
A1_range = (200, 600)
t1_range = (9, 40)
A2_range = (700, 950)
t2_range = (0.8, 3)


save_folder = 'output_images'
os.makedirs(save_folder, exist_ok=True)
coord_folder = 'output_coordinates'
os.makedirs(coord_folder, exist_ok=True)


plot_counter = 151
while plot_counter < 201:
    n = np.random.randint(3, 5)
    plt.figure()

    coord_list = []
    for _ in range(n):
        y0 = np.random.uniform(*y0_range)
        A1 = np.random.uniform(*A1_range)
        t1 = np.random.uniform(*t1_range)
        A2 = np.random.uniform(*A2_range)
        t2 = np.random.uniform(*t2_range)
        y = curve_func(x, y0, A1, t1, A2, t2)
        plt.plot(x, y)


        font = {'family': 'Calibri', 'weight': 'bold', 'size': 14}
        plt.xlabel('Strain / %', fontdict=font)
        plt.ylabel('Stress / MPa', fontdict=font)
        plt.xticks(fontweight='bold', fontfamily='Calibri',fontsize=14)
        plt.yticks(fontweight='bold', fontfamily='Calibri',fontsize=14)
        # plt.title(f' {plot_counter}')
        plt.xlim((0, 40))
        plt.ylim((0, 1200))
        save_path = os.path.join(save_folder, f'{plot_counter}.jpg')
        plt.savefig(save_path)


        image = plt.imread(save_path)
        height, width, _ = image.shape
        coords = []
        for x_val, y_val in zip(x, y):
            pixel_x = int((x_val * 497 / 40 )+ 80 )
            pixel_y = int(480 - ((y_val *369 / 1200) +53) )
            coords.append([pixel_x, pixel_y])
        coord_list.append(coords)

    plt.close()


    with open(os.path.join(coord_folder, f'{plot_counter}.txt'), 'w') as f:
        for coords in coord_list:
            f.write(str(coords) + '\n')

    plot_counter += 1

print('image output and save the pixel coordinates')
