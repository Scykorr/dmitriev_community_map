from PyQt5.QtGui import QImage
a = '100'
print(int(a))
IMG_FILE_NAME = 'test.bmp'

img = QImage(IMG_FILE_NAME)
width = img.size().width()
print(width)
height = img.size().height()
print(height)

# 1 сантиметр равно 37.936267 Пикселей
# self.img = self.img.scaled(width * 3, height * 3)
# self.img_width = self.img.size().width()
# self.img_height = self.img.size().height()
#
# # Размер окна под размер картинок
# self.resize(self.img_width * 2 + 20, self.img_height + 20)
#
# # Сгенерируем список координат пикселей
# self.pixel_list = [(y, x) for y in range(self.img_height) for x in range(self.img_width)]


"""
Как вставить изображение при нажатии на кнопку в PyQt5?
Как импортировать изображение после нажатия на кнопку? Я пробовал делать
def image(self):
    self.lbl = QtWidgets.QLabel(self)
    self.pix = QtGui.QPixmap("image/Rock.png")
    print(self.pix.isNull())
    self.lbl.setPixmap(self.pix)
    self.lbl.resize(400, 400)
    self.lbl.move(30, 1150)
    
    
Здраствуйте! Вы неправильно делаете, в кодеself.pix = QtGui.QPixmap("image/Rock.png")
есть ошибка. В нём нужно указать полный путь к файлу. Например:
self.pix = QtGui.QPixmap("C:\\Users\\Имя пользователя\\Image.png")    
"""
