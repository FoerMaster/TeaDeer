import cv2
import random
import string
import os


def calcDiff(img1, img2):
    diff = cv2.absdiff(img1, img2)
    thresh_diff = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)[1]
    thresh_diff_gray = cv2.cvtColor(thresh_diff, cv2.COLOR_BGR2GRAY)
    total_pixels = img1.shape[0] * img1.shape[1] * 1.0
    diff_on_pixels = cv2.countNonZero(thresh_diff_gray) * 1.0
    difference_measure = diff_on_pixels / total_pixels
    return difference_measure


def markVideo(_class, path, save_directory):
    vidcap = cv2.VideoCapture(path)
    success, prev_image = vidcap.read()
    capt = 0
    frame_counter = 0  # Переменная-счетчик для каждого 60-го кадра
    while success:
        success, image = vidcap.read()
        if success:
            frame_counter += 1
            if (frame_counter % 60 != 0) or calcDiff(prev_image,
                                                     image) > 0.05:  # Пропускаем каждый кадр, кроме каждого 60-го
                prev_image = image
                continue

            # Добавляем полупрозрачный текст на кадр
            mask = image.copy()
            text_bg_color = (111, 190, 248)
            cv2.putText(mask, _class, (8, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, text_bg_color, 1, cv2.LINE_AA)
            alpha = 0.7
            image_with_transparent_text = cv2.addWeighted(image, 1 - alpha, mask, alpha, 0)
            random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Calculate the aspect ratio of the original image
            aspect_ratio = gray_image.shape[1] / gray_image.shape[0]

            # Define the new dimensions
            new_width = 1280
            new_height = int(new_width / aspect_ratio)

            # If the new height is still greater than 720, adjust the width accordingly
            if new_height > 720:
                new_height = 720
                new_width = int(new_height * aspect_ratio)

            # Resize the image without stretching
            resized_image = cv2.resize(gray_image, (new_width, new_height))

            cv2.putText(resized_image, _class, (12, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1,
                        cv2.LINE_AA)
            cv2.putText(resized_image, _class, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                        cv2.LINE_AA)
            cv2.imwrite(save_directory + _class + "_%d_%s.jpg" % (capt, random_chars), resized_image)
            capt += 1
            prev_image = image


def markImage(_class, file, save_directory):
    image = cv2.imread(file)
    random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the aspect ratio of the original image
    aspect_ratio = gray_image.shape[1] / gray_image.shape[0]

    # Define the new dimensions
    new_width = 1280
    new_height = int(new_width / aspect_ratio)

    # If the new height is still greater than 720, adjust the width accordingly
    if new_height > 720:
        new_height = 720
        new_width = int(new_height * aspect_ratio)

    # Resize the image without stretching
    resized_image = cv2.resize(gray_image, (new_width, new_height))

    cv2.putText(resized_image, _class, (12, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1,
                cv2.LINE_AA)
    cv2.putText(resized_image, _class, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                cv2.LINE_AA)


    cv2.imwrite(save_directory + _class + "_%s.jpg" % random_chars, resized_image)


file_types = {
    'jpg': 'img',
    'jpeg': 'img',
    'png': 'img',
    'mp4': 'vid',
    'avi': 'vid',
    'mkv': 'vid',
}


def get_file_type(file_path):
    extension = os.path.splitext(file_path)[1][1:].lower()
    file_type = file_types.get(extension, 'Неизвестный тип файла')
    return file_type
