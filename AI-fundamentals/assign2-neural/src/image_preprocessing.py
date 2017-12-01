from image import IMAGE_ROW_WIDTH


def get_mask_sum(pixels, i, j):
    """
    Calculates the sum of pixels grey levels around the pixel at location [i,j] (3x3 mask)
    :param pixels: pixels matrix
    :param i: row
    :param j: column
    :return:
    """
    mask_sum = 0
    mask_sum += pixels[i - 1][j - 1]
    mask_sum += pixels[i][j - 1]
    mask_sum += pixels[i + 1][j - 1]
    mask_sum += pixels[i - 1][j]
    mask_sum += pixels[i][j]
    mask_sum += pixels[i + 1][j]
    mask_sum += pixels[i - 1][j + 1]
    mask_sum += pixels[i][j + 1]
    mask_sum += pixels[i + 1][j + 1]
    return mask_sum


def blur_images(images):
    """
    Blurs the images passed by reference.
    :param images: images to blur
    """
    for image in images:
        pixels = image.pixels
        blurred_pixels = []
        for i in range(IMAGE_ROW_WIDTH):
            row = []
            for j in range(IMAGE_ROW_WIDTH):
                row.append(0)
            blurred_pixels.append(row)
        for i in range(1, IMAGE_ROW_WIDTH - 1):
            for j in range(1, IMAGE_ROW_WIDTH - 1):
                blurred_pixels[i][j] = get_mask_sum(pixels, i, j) / 9

        image.pixels = blurred_pixels


def rotate_images(images):
    """
    Detects the eyebrows of the images and rotate the images so the eyebrows are always on the top half.
    :param images: images to rotate
    """
    def rotate_square(i, j, times):
        for k in range(times):
            i, j = IMAGE_ROW_WIDTH - 1 - j, i
        return i, j

    # Rotate the image by trying to find eyes (darkest chunk of pixels)
    quarters_indexes = [(0, 0), (0, 1), (1, 1), (1, 0)]

    # rotate all the images depending on the eyebrows
    for image in images:
        pixels = image.pixels
        maximums = []
        maximums_ind = []

        for quarter_indexes in quarters_indexes:
            a, b = quarter_indexes
            maximum = 0
            max_i = 0
            max_j = 0

            half_row = int(IMAGE_ROW_WIDTH / 2)  # 2 = sqrt(4)

            # cut the image pixels in 4 submatrices
            for i in range(a * half_row + 1, (a + 1) * half_row - 1):  # row indexes
                for j in range(b * half_row + 1, (b + 1) * half_row - 1):  # col indexes
                    sum = get_mask_sum(pixels, i, j)
                    if sum > maximum:
                        maximum = sum
                        max_i = i
                        max_j = j

            maximums.append(maximum)
            maximums_ind.append((max_i, max_j))

        # get maximum mask center (first eyebrow)
        max1 = max(maximums)
        max_index1 = maximums.index(max1)
        # delete first maximum mask center
        maximums[max_index1] = 0

        # get second maximum mask center (second eyebrow)
        max2 = max(maximums)
        max_index2 = maximums.index(max2)

        # create new pixels
        rotated_pixels = []
        for i in range(IMAGE_ROW_WIDTH):
            row = []
            for j in range(IMAGE_ROW_WIDTH):
                row.append(0)
            rotated_pixels.append(row)

        # compute every case to find the right number of rotation to do
        rot_square = 0
        if (max_index1 == 1 and max_index2 == 2) or (max_index1 == 2 and max_index2 == 1):
            rot_square = 1
        elif (max_index1 == 2 and max_index2 == 3) or (max_index1 == 3 and max_index2 == 2):
            rot_square = 2
        elif (max_index1 == 3 and max_index2 == 0) or (max_index1 == 0 and max_index2 == 3):
            rot_square = 3

        for i in range(IMAGE_ROW_WIDTH):
            for j in range(IMAGE_ROW_WIDTH):
                new_i, new_j = rotate_square(i, j, rot_square)
                rotated_pixels[new_i][new_j] = pixels[i][j]

        image.pixels = rotated_pixels
