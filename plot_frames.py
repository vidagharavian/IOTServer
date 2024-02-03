import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from PIL import Image

def plot_rectangle(image_path,raw_data,output_name):
    im = Image.open(image_path)

    # Create figure and axes
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(im)
    for r in raw_data:
        if r['updatable'] == True:
    # Create a Rectangle patch
            rect = patches.Rectangle((r['x'], r['y']), 35, 35, linewidth=1, edgecolor='r', facecolor='none')

        # Add the patch to the Axes
            ax.add_patch(rect)
            ax.text(r['x'], r['y'], r['id'], style='italic',
                    fontsize=13, color="b")
    fig.savefig(f'output/{output_name}')
    # plt.show()
    plt.savefig('books_read.png')
    fig.clf()
    plt.close()

def plot_all_frames(frame_name):
    for n in range(1,151):
        image_path = f"test_data/{frame_name}/{n:03}.jpg"
        label =pd.read_csv(f"output/{n:03}.csv")
        df = label.to_dict('records')
        plot_rectangle(image_path,df,f"{n:03}.jpg")

plot_all_frames(49)

def create_video():
    import cv2
    import numpy as np
    import glob

    img_array = []
    for i in range(1,151):
        img = cv2.imread(f"C:\\Users\\vghar\\PycharmProjects\\iot_server\\output\\{i:03}.jpg")
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    out = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
create_video()