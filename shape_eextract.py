def extract(img_file: str, ext_name: str):
    from PIL import Image
    import numpy as np
    import imageio
    from skimage.transform import resize
    import matplotlib.pyplot as plt

    img = Image.open(img_file)
    img_array = np.array(img)
    trans_img = []
    for i in img_array:
        p = np.where(i == [29, 49, 80, 255], [50, 205, 50, 255], i)
        p = np.where(p == [228, 230, 234, 255], [50, 205, 50, 255], p)
        p = p.tolist()
        for r in range(len(p)):
            if p[r] == [255, 255, 255, 255]:
                p[r] = [0, 0, 0, 0]
        trans_img.append(p)

    trans_img = np.array(trans_img)
    imageio.imwrite(ext_name + ".png", trans_img)


extract("/Users/macbook/Desktop/alien.png","alien_t")
def resize_ext():
    from PIL import Image
    import imageio
    from skimage.transform import resize
    import matplotlib.pyplot as plt
    import numpy as np
    img = Image.open("alien_t.gif")
    img_arr = np.array(img)
    rez_img = resize(img_arr, (50,76))
    imageio.imwrite("alien_t.gif", rez_img)

resize_ext()

