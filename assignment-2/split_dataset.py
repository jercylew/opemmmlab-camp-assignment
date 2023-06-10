import os
from shutil import copyfile
import random


SOURCE_DIR = './orig_fruits_dataset'
OUTPUT_DIR = './output'
classes_fruits = ['山竹', '柠檬', '椰子', '猕猴桃', '胡萝卜', '苦瓜', '草莓', '葡萄-白', '西红柿', '黄瓜', '哈密瓜', '杨梅',
                  '桂圆', '榴莲', '石榴', '脐橙', '苹果-红', '荔枝', '葡萄-红', '车厘子', '圣女果', '柚子', '梨', '火龙果',
                  '砂糖橘', '芒果', '苹果-青', '菠萝', '西瓜', '香蕉']
SPLIT_CATEGORIES = ['training_set', 'val_set', 'test_set']


def copy_files(filenames, source_dir, output_dir, class_name, split_category):
    """Copy files in source directory to specified output directory
        All files in `source_dir` are copied to `output_dir/split_category/class_name`
        split_category: training_set | val_set | test_set
    """
    for filename in filenames:
        this_file = os.path.join(source_dir, class_name, filename)
        destination = os.path.join(output_dir, split_category, class_name, filename)
        # print('Copying file ', this_file, ' -> ', destination)
        copyfile(this_file, destination)


def split_files(source_dir, classes, output_dir, split_ratio_train, split_ratio_validate):
    """Split the original dataset into train, validation and test groups
    Args:
        source_dir (string): The source directory of the top level of the dataset.
        classes (int): The list of classes in the dataset
        output_dir (string): The top level output directory of the split files
        split_ratio_train (string): The ratio at which the files are split into the output directory for train
        split_ratio_validate (string): The ratio at which the files are split into the output directory for validation

    Returns:
        None
    """
    for class_name in classes:
        print('Splitting files for class ' + class_name)
        files = []
        for filename in os.listdir(os.path.join(source_dir, class_name)):
            file = os.path.join(source_dir, class_name, filename)
            if os.path.getsize(file) > 0:
                files.append(filename)
            else:
                print(filename + " is zero length, so ignoring.")

        # First train and validate
        training_length = int(len(files) * split_ratio_train)
        validate_length = int(len(files) * split_ratio_validate)

        # Then the left are put into test if there are some
        testing_length = int(len(files) - training_length - validate_length)
        if testing_length < 0:
            testing_length = 0

        shuffled_set = random.sample(files, len(files))
        training_set = shuffled_set[0:training_length]
        validate_set = shuffled_set[training_length:training_length+validate_length]
        testing_set = []
        if testing_length > 0:
            testing_set = shuffled_set[:testing_length]

        copy_files(training_set, source_dir, output_dir, class_name, 'training_set')
        copy_files(validate_set, source_dir, output_dir, class_name, 'val_set')
        copy_files(testing_set, source_dir, output_dir, class_name, 'test_set')


def main():
    try:
        for category in SPLIT_CATEGORIES:
            if not os.path.exists(os.path.join(OUTPUT_DIR, category)):
                os.mkdir(os.path.join(OUTPUT_DIR, category))

            for class_name in classes_fruits:
                if not os.path.exists(os.path.join(OUTPUT_DIR, category, class_name)) :
                    os.mkdir(os.path.join(OUTPUT_DIR, category, class_name))

        split_files(SOURCE_DIR, classes_fruits, OUTPUT_DIR, 0.8, 0.1)

    except OSError:
        pass


if __name__ == '__main__':
    main()
