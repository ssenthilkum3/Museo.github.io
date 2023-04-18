import qrcode
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as can
from reportlab.pdfbase.pdfmetrics import stringWidth
import tkinter as tk
from PIL import Image, ImageTk
import pypdfium2 as pdfium
import random

def create_QR_code_png(input_link, file_name='QRCode'):
    # Creates QR code png
    path = './GeneratedQRCodes/'
    if not os.path.exists(path):
        os.makedirs(path)
    img = qrcode.make(input_link)
    img.save(path+file_name+'.png')
    
def create_pdf(file_name, title, description, title_font='Helvetica', title_size=24, description_font='Helvetica', description_size=12, spacing=50, qr_size=(400, 400)):
    # Creates pdf and adds title and description in desired font and size
    qr_width, qr_height = qr_size
    path = './PDFs/'
    if not os.path.exists(path):
        os.makedirs(path)
    pdf = can.Canvas(path+file_name+'.pdf', pagesize=letter)
    page_width, page_height = letter
    title_x = (page_width-stringWidth(title, title_font, title_size))/2
    title_y = (page_height+spacing+qr_height)/2
    pdf.setFont(title_font, title_size)
    pdf.drawString(title_x, title_y, title)
    description_y = (page_height-title_size-spacing-qr_height)/2
    pdf.setFont(description_font, description_size)
    if ('\n' not in description) and ('\\n' not in description):
        # Single line description
        description_x = (page_width-stringWidth(description, description_font, description_size))/2
        pdf.drawString(description_x, description_y, description)
    else:
        # Multi line description
        description_split = None
        if '\n' in description:
            description_split = description.split('\n')
        else:
            description_split = description.split('\\n')
        num_lines = len(description_split)
        for i in range(num_lines):
            description_x = (page_width-stringWidth(description_split[i], description_font, description_size))/2
            pdf.drawString(description_x, description_y-(i*description_size*1.2), description_split[i])

    pdf.drawImage('./GeneratedQRCodes/'+file_name+'.png', (page_width-qr_width)/2, (page_height-qr_height)/2, width=qr_width, height=qr_height)
    pdf.save()

def create_pdf_preview(file_name='preview', title='Title', description='Description', title_font='Helvetica', title_size=24, description_font='Helvetica', description_size=12, spacing=50, qr_size=(400, 400)):
    # Creates pdf and adds title and description in desired font and size
    qr_width, qr_height = qr_size
    path = './Preview/'
    if not os.path.exists(path):
        os.makedirs(path)
    pdf = can.Canvas(path+file_name+'.pdf', pagesize=letter)
    page_width, page_height = letter
    title_x = (page_width-stringWidth(title, title_font, title_size))/2
    title_y = (page_height+spacing+qr_height)/2
    pdf.setFont(title_font, title_size)
    pdf.drawString(title_x, title_y, title)
    description_y = (page_height-title_size-spacing-qr_height)/2
    pdf.setFont(description_font, description_size)
    if ('\n' not in description) and ('\\n' not in description):
        # Single line description
        description_x = (page_width-stringWidth(description, description_font, description_size))/2
        pdf.drawString(description_x, description_y, description)
    else:
        # Multi line description
        description_split = None
        if '\n' in description:
            description_split = description.split('\n')
        else:
            description_split = description.split('\\n')
        num_lines = len(description_split)
        for i in range(num_lines):
            description_x = (page_width-stringWidth(description_split[i], description_font, description_size))/2
            pdf.drawString(description_x, description_y-(i*description_size*1.2), description_split[i])
    img = qrcode.make('Preview QR Code')
    img.save('./Preview/QR'+file_name+'.png')
    pdf.drawImage('./Preview/QR'+file_name+'.png', (page_width-qr_width)/2, (page_height-qr_height)/2, width=qr_width, height=qr_height)
    pdf.save()
    pdf = pdfium.PdfDocument('./Preview/preview.pdf')
    preview_pdf = pdf.get_page(0)
    preview_png = preview_pdf.render().to_pil()
    preview_png.save('./Preview/preview.png')
    

def create_QR_codes_from_CSV(CSV_file_name):
    # Opens CSV file and reads all rows
    with open(CSV_file_name, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        num_QR_codes = 0
        # Creates QR code file from each row
        for row in csv_reader:
            if row[1] == 'png':
                create_QR_code_png(row[0], row[2])
            else:
                create_QR_code_png(row[0], row[2])
                # Automatically sets font if not given
                if row[4] == '':
                    row[4] = 'Helvetica'
                if row[5] == '':
                    row[5] = '24'
                if row[7] == '':
                    row[7] = 'Helvetica'
                if row[8] == '':
                    row[8] = '12'
                if row[9] == '':
                    row[9] = '400'
                if row[10] == '':
                    row[10] = '50'
                create_pdf(row[2],row[3],row[6],row[7],int(row[8]), int(row[10]), row[4], int(row[5]), (int(row[9]), int(row[9])))
            num_QR_codes += 1
    return num_QR_codes

def launch_gui():
    record = []
    #GUI Methods
    def preview():
        create_pdf_preview(title=title_entry.get(), description=description_entry.get(), description_font=description_font.get(), description_size=int(description_size.get()), spacing=int(spacing_scale.get()), title_font=title_font.get(), title_size=int(title_size.get()), qr_size=(int(qr_size_scale.get()), int(qr_size_scale.get())))
        img = ImageTk.PhotoImage(Image.open('./Preview/preview.png').resize((int(letter[0]/2), int(letter[1]/2))))
        pdf_preview.configure(image=img)
        pdf_preview.image = img
    def update_record():
        if record_lb.size()>0:
            record_lb.delete(0, record_lb.size())
        for i in range(len(record)):
            info = record[i]['filename']+'.pdf'+', '+record[i]['link']
            record_lb.insert(i+1, info)
    def clear():
        record.clear()
        update_record()
    def remove():
        if len(record_lb.curselection())>0:
            del record[record_lb.curselection()[0]]
            update_record()
    def add():
        if save_as_entry.get()=='' and link_entry.get()=='':
            error_label.configure(text='Link and filename needed.')
        elif link_entry.get()=='':
            error_label.configure(text='Link needed.')
        elif save_as_entry.get()=='':
            error_label.configure(text='Filename needed.')
        else:
            error_label.configure(text='')
            args = {'filename':save_as_entry.get(), 'link':link_entry.get(), 'title':title_entry.get(), 'description':description_entry.get(), 'description_font':description_font.get(), 'description_size':int(description_size.get()), 'spacing':int(spacing_scale.get()), 'title_font':title_font.get(), 'title_size':int(title_size.get()), 'qr_size':(int(qr_size_scale.get()), int(qr_size_scale.get()))}
            record.append(args)
            update_record()
    def generate_qr_codes():
        for r in record:
            create_QR_code_png(r['link'], file_name=r['filename'])
            create_pdf(r['filename'], r['title'], r['description'], r['title_font'], r['title_size'], r['description_font'], r['description_size'], r['spacing'], r['qr_size'])
    gui = tk.Tk()
    gui.title('QR Code Generator')
    #GUI widgets (organized by row)
    #Title Entry
    link_label = tk.Label(gui, text='Link').grid(row=0, column=0)
    link_entry = tk.Entry(gui, width=45)
    link_entry.grid(row=0, column=1, columnspan=3)
    #Title Entry
    title_label = tk.Label(gui, text='Title').grid(row=1, column=0)
    title_entry = tk.Entry(gui)
    title_entry.grid(row=1, column=1)
    #Title Fonts Listbox
    fonts = can.Canvas('').getAvailableFonts()
    title_font = tk.StringVar(gui, fonts[1])
    title_font_om = tk.OptionMenu(gui, title_font, *fonts).grid(row=1, column=2)
    #Title Sizes Listbox
    title_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 40, 48, 64, 80, 100, 120]
    title_size = tk.StringVar(gui, title_sizes[15])
    title_size_om = tk.OptionMenu(gui, title_size, *title_sizes).grid(row=1, column=3)
    #Title Entry
    description_label = tk.Label(gui, text='Description').grid(row=2, column=0)
    description_entry = tk.Entry(gui)
    description_entry.grid(row=2, column=1)
    #Description Fonts Listbox
    fonts = can.Canvas('').getAvailableFonts()
    description_font = tk.StringVar(gui, fonts[0])
    description_font_om = tk.OptionMenu(gui, description_font, *fonts).grid(row=2, column=2)
    #Description Sizes Listbox
    description_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 40, 48, 64, 80]
    description_size = tk.StringVar(gui, description_sizes[11])
    description_size_om = tk.OptionMenu(gui, description_size, *description_sizes).grid(row=2, column=3)
    #Spacing
    spacing_label = tk.Label(gui, text='Spacing').grid(row=3, column=0)
    spacing_scale = tk.Scale(gui, from_=10, to=700, orient='horizontal')
    spacing_scale.grid(row=3, column=1)
    spacing_scale.set(100)
    #QR Size
    qr_size_label = tk.Label(gui, text='QR Code Size').grid(row=3, column=2)
    qr_size_scale = tk.Scale(gui, from_=30, to=700, orient='horizontal')
    qr_size_scale.grid(row=3, column=3)
    qr_size_scale.set(300)
    #PDF preview image
    path = './Preview/'
    if not os.path.exists(path):
        os.makedirs(path)
    #Create empty preview
    inititial_preview = can.Canvas('./Preview/preview.pdf', pagesize=letter)
    inititial_preview.setFont('Helvetica', 24)
    inititial_preview.drawString(180, 400, 'Preview will appear here.')
    inititial_preview.save()
    inititial_preview_pdf = pdfium.PdfDocument('./Preview/preview.pdf')
    preview_pdf = inititial_preview_pdf.get_page(0)
    preview_png = preview_pdf.render().to_pil()
    preview_png.save('./Preview/preview.png')
    img = ImageTk.PhotoImage(Image.open('./Preview/preview.png').resize((int(letter[0]/2), int(letter[1]/2))))
    pdf_preview = tk.Label(gui, image=img)
    pdf_preview.grid(row = 4, column = 0, columnspan=5)
    #Preview Button
    preview_button = tk.Button(gui, text='Preview', command=preview).grid(row=5, column=0, columnspan=5)
    #Save As Entry
    save_as_label = tk.Label(gui, text='Save As:').grid(row=6, column=0)
    save_as_entry = tk.Entry(gui, width=30)
    save_as_entry.grid(row=6, column=1)
    save_as_format_label = tk.Label(gui, text='.pdf').grid(row=6, column=2)
    #Add Button
    add_button = tk.Button(gui, text='Add', command=add).grid(row=6, column=3)
    #Error Label
    error_label = tk.Label(gui, text='')
    error_label.grid(row=6, column=4)
    #Record Listbox
    record_lb = tk.Listbox(gui, width=50)
    record_lb.grid(row=7, column=0, columnspan=4)
    #Remove Button
    remove_button = tk.Button(gui, text='Remove Selection', command=remove).grid(row=8, column=0)
    #Clear Button
    clear_button = tk.Button(gui, text='Clear All', command=clear).grid(row=8, column=1)
    #Generate QR Codes Button
    generate_button = tk.Button(gui, text='Generate QR Codes', command=generate_qr_codes).grid(row=8, column=2)
    #Quit Button
    quit_button = tk.Button(gui, text='Exit', command=gui.destroy).grid(row=8, column=3)
    gui.mainloop()

if __name__ == "__main__":
    launch_gui()