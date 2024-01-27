from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSlider, QComboBox, QMessageBox

import os
import time


def change_brightness(new_brightness_value: int | float, screen_identifiet: str) -> None:
    """Change the gamma value of the screen.

    Args:
        new_gamma_value (int | float): The new gamma value.
    """
    
    cmd = f"xrandr --output {screen_identifiet} --brightness {new_brightness_value}"
    
    os.system(cmd)

def get_screen_identifiers() -> list[str]:
    """Get all screen identifiers.

    Returns:
        list[str]: The screen identifiers.
    """
    
    cmd = "xrandr | grep ' connected' | awk '{print $1}'"
    
    output = os.popen(cmd).read()
    
    return output.split("\n")[:-1]



# set up GUI
#
# dropdown selection for screen
#slider from 0.1 to 3.0 in 0.1 steps
#button to set gamma value
#once button is pressed, set gamma value and:
#set a 15 sec countdown timer + dialog box to confirm
#if no confirmation, reset gamma value to 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Brightness Controller")

        self.layout = QVBoxLayout()

        self.comboBox = QComboBox()
        self.comboBox.addItems(get_screen_identifiers())
        self.layout.addWidget(self.comboBox)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(300)
        self.slider.setValue(100)
        self.layout.addWidget(self.slider)

        self.button = QPushButton("Set Brightness")
        self.button.clicked.connect(self.set_brightness)
        self.layout.addWidget(self.button)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.reset_brightness)
        
        self.message_box: QMessageBox | None = None

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_brightness(self):
        screen_identifier = self.comboBox.currentText()
        brightness_value = self.slider.value() / 100.0
        change_brightness(brightness_value, screen_identifier)
        self.timer.start(15_00) # 15_000ms = 15 seconds
        self.message_box = QMessageBox()
        r = self.message_box.question(self, '', "Do you want to keep this brightness?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if r == QMessageBox.No:
            self.reset_brightness()
        else:
            self.timer.stop()
        
        self.message_box.close()
        self.message_box = None
        
        

    def reset_brightness(self):
        print("resetting Brighntess")
        screen_identifier = self.comboBox.currentText()
        change_brightness(1.0, screen_identifier)
        
        
        if self.message_box is not None:
            #close message box
            self.message_box.close()
            self.message_box = None

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()