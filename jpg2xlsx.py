from PIL import Image
import xlsxwriter
import sys

im = Image.open(sys.argv[1])
pix = im.load()

width = im.size[0]
height = im.size[1]

workbook = xlsxwriter.Workbook(sys.argv[2] + '.xlsx')
worksheet = workbook.add_worksheet()

for x in range(width):
	for y in range(height):
 		style_format = workbook.add_format()
		style_format.set_bg_color('#%02x%02x%02x' % pix[x,y])
		worksheet.set_row(x, 1.4)
		worksheet.write(y, x, '', style_format)

worksheet.set_column(0,width, 0.15)

workbook.close()
