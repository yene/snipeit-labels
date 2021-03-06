from fpdf import FPDF
import qrcode
import os
import csv
import math

pdf_w=210
box_w=pdf_w/3
pdf_h=297
box_h=pdf_h/8
box_h=37.0
print(box_w, box_h)

# x is first, ->
# y is second, down

data = []
input_filename = 'all.csv'
output_filename = input_filename.replace('csv', 'pdf')
font = 'Arial'
printer_margin = 4 #mm

with open(input_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_header = True
    for row in csv_reader:
      if is_header:

        is_header = False
        continue

      data.append({'tag': row[0].strip(), 'serial': row[1].strip()})

print('print labels: ' + str(len(data)))

pdf=FPDF('P', 'mm', format='A4') #page format. A4 is the default value of the format, you don't have to specify it.
pdf.compress = False
per_page = 7*3
num_pages = math.ceil(len(data)/per_page)

counter = 0

for page_i in range(num_pages):
  pdf.add_page()
  offset_x = 0
  offset_y = 0
  for row_i in range(7):
    for column_i in range(3):
      if counter == len(data):
        continue

      company_name = 'bob Finance'
      asset_tag = data[counter]['tag']
      asset_serial = data[counter]['serial']
      off_x = column_i*box_w
      off_y = row_i*box_h
      # box
      if False:
        pdf.line(off_x, off_y, off_x + box_w, off_y)
        pdf.line(off_x + box_w, off_y, off_x + box_w, off_y + box_h)
        pdf.line(off_x + box_w, off_y + box_h, off_x, off_y + box_h)
        pdf.line(off_x, off_y, off_x, off_y + box_h)
      # qrcode
      qr_margin_top = 5
      qr_margin_left = 4
      pdf.set_xy(off_x + qr_margin_left, off_y + qr_margin_top)
      qrcode_side = box_h - (qr_margin_top*2)
      qr = qrcode.QRCode(
          version=1,
          error_correction=qrcode.constants.ERROR_CORRECT_L,
          box_size=5,
          border=0,
      )
      qr.add_data(asset_tag)
      img = qr.make_image()
      img.save('qrcode.png')
      pdf.image('qrcode.png',  link='', type='', w=qrcode_side, h=qrcode_side)
      os.remove('qrcode.png')

      middle_x = off_x + qrcode_side + 6
      off_y = off_y + 3
      pdf.set_xy(middle_x, off_y)
      pdf.set_font(font, '', 8)
      pdf.set_text_color(64, 64, 64)
      pdf.cell(middle_x, 6, 'tag')

      pdf.set_xy(middle_x, off_y + 3)
      pdf.set_font(font, 'B', 16)
      pdf.set_text_color(0)
      pdf.cell(middle_x, 9, asset_tag)

      off_y = off_y + 7 + 3
      pdf.set_xy(middle_x, off_y)
      pdf.set_font(font, '', 8)
      pdf.set_text_color(64, 64, 64)
      pdf.cell(middle_x, 6, 'company')

      pdf.set_xy(middle_x, off_y + 3)
      pdf.set_font(font, '', 12)
      pdf.set_text_color(0)
      pdf.cell(middle_x, 9, company_name)

      # Use multicell if you want to line break serial https://pyfpdf.readthedocs.io/en/latest/reference/multi_cell/index.html

      if asset_serial != '':
        off_y = off_y + 7 + 3
        pdf.set_xy(middle_x, off_y)
        pdf.set_font(font, '', 8)
        pdf.set_text_color(64, 64, 64)
        pdf.cell(middle_x, 6, 'serial')

        pdf.set_xy(middle_x, off_y + 3)
        pdf.set_font(font, '', 12)
        pdf.set_text_color(0)
        pdf.cell(middle_x, 9, asset_serial)

      counter = counter + 1


pdf.output(output_filename, 'F')
