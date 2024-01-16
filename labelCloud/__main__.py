import argparse
import logging
import sys
import os
# sys.path.append("C:\\Users\\ailab\\git\\labelCloud\\labelCloud")
sys.path.append("C:/Users/ailab/git/labelCloud")
from glob import glob
import json
# from labelCloud import __version__


def main():
    parser = argparse.ArgumentParser(
        description="Label 3D bounding boxes inside point clouds."
    )
    parser.add_argument(
        "-e",
        "--example",
        action="store_true",
        help="Setup a project with an example point cloud and label.",
    )
    # parser.add_argument(
    #     "-v", "--version", action="version", version="%(prog)s " + __version__
    # )
    args = parser.parse_args()

    if args.example:
        setup_example_project()
    src_path = "C:\\Users\\ailab\\git\\labelCloud\\custom_data\\src"
    dst_path = "C:\\Users\\ailab\\git\\labelCloud\\custom_data\\dst"
    export_rscube_to_json(src_path, dst_path)
    start_gui()


def setup_example_project() -> None:
    import shutil
    from pathlib import Path

    import pkg_resources

    from labelCloud.control.config_manager import config

    logging.info(
        "Starting labelCloud in example mode.\n"
        "Setting up project with example point cloud ,label and default config."
    )
    cwdir = Path().cwd()

    # Create folders
    pcd_folder = cwdir.joinpath(config.get("FILE", "pointcloud_folder"))
    pcd_folder.mkdir(exist_ok=True)
    label_folder = cwdir.joinpath(config.get("FILE", "label_folder"))
    label_folder.mkdir(exist_ok=True)
    
    # Copy example files
    shutil.copy(
        pkg_resources.resource_filename("labelCloud.resources", "default_config.ini"),
        str(cwdir.joinpath("config.ini")),
    )
    shutil.copy(
        pkg_resources.resource_filename(
            "labelCloud.resources.examples", "exemplary.ply"
        ),
        str(pcd_folder.joinpath("exemplary.ply")),
    )
    shutil.copy(
        pkg_resources.resource_filename("labelCloud.resources", "default_classes.json"),
        str(label_folder.joinpath("_classes.json")),
    )
    shutil.copy(
        pkg_resources.resource_filename(
            "labelCloud.resources.examples", "exemplary.json"
        ),
        str(label_folder.joinpath("exemplary.json")),
    )
    logging.info(
        f"Setup example project in {cwdir}:"
        "\n - config.ini"
        "\n - pointclouds/exemplary.ply"
        "\n - labels/exemplary.json"
    )

def export_rscube_to_json(src_root, dst_root):
    # read label txt
    src_labels = glob(os.path.join(src_root, '*.txt'))
    for src_label in src_labels:
        write_str = ''
        output_dict = {}
        folder = src_label.split(os.sep)[-2];
        filename = src_label.split(os.sep)[-1];
        path = os.path.join('custom_data', dst_root, folder)
        # obj_list = []
        output_dict['folder'] = folder
        output_dict['filename'] = filename
        output_dict['path'] = path
        
        # read label txt
        with open(src_label, 'r') as f:
            lines = f.readlines()
        # write label json
        dst_label = src_label.replace(src_root, dst_root)
        
        if not os.path.isfile(dst_label):
            for line in lines:
                
                line = line.strip().split(' ')
                centroid_x = line[0]
                centroid_y = line[1]
                centroid_z = line[2]

                dimensions_length = line[3]
                dimensions_width = line[4]
                dimensions_height = line[5]
                
                rotations_z = line[6]
        
                detection_conf = line[7]
                class_conf = line[8]
                label_idx = line[9]
                
                name = line[10]
                
                write_str += "{} 0 0 0 0 0 0 0 {} {} {} {} {} {} {} {} {} {}\n".format(name, dimensions_height, dimensions_width, dimensions_length, centroid_x, centroid_y, centroid_z, rotations_z, label_idx, detection_conf, class_conf)
                # with open(dst_label, 'a') as dst_txt:
                #     dst_txt.write("{} 0 0 0 0 0 0 0 {} {} {} {} {} {} {} \n".format(name, dimensions_height, dimensions_width, dimensions_length, centroid_x, centroid_y, centroid_z, rotations_z))
            with open(dst_label, 'w') as dst_txt:
                dst_txt.write(write_str)

def start_gui():
    import sys

    from PyQt5.QtWidgets import QApplication, QDesktopWidget

    from labelCloud.control.controller import Controller
    from labelCloud.view.gui import GUI

    app = QApplication(sys.argv)

    # Setup Model-View-Control structure
    control = Controller()
    view = GUI(control)

    # Install event filter to catch user interventions
    app.installEventFilter(view)

    # Start GUI
    view.show()

    app.setStyle("Fusion")
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - view.width()) // 2
    height = (desktop.height() - view.height()) // 2
    view.move(width, height)

    logging.info("Showing GUI...")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
