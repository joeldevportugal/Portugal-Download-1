from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
import customtkinter
import os


def clear_widgets():
    Limagem.config(image='')
    cmb_qualidade_mp3.set('')
    cmb_qualidade_mp4.set('')
    Eurl.delete(0, END)
    Lestado.delete(0, END)


def download_mp3():
    url = Eurl.get()
    quality = cmb_qualidade_mp3.get()

    if not url or not quality:
        return

    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True, abr=quality).first()
    if stream:
        save_path = filedialog.asksaveasfilename(defaultextension=".mp3")
        if save_path:
            Lestado.delete(0, END)
            Lestado.insert(END, f"Downloading MP3 to {save_path}")
            stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
            Lestado.insert(END, "Download complete!")
        else:
            Lestado.insert(END, "Download canceled")


def download_mp4():
    url = Eurl.get()
    quality = cmb_qualidade_mp4.get()

    if not url or not quality:
        return

    yt = YouTube(url)
    stream = yt.streams.filter(res=quality, file_extension='mp4').first()
    if stream:
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if save_path:
            Lestado.delete(0, END)
            Lestado.insert(END, f"Downloading MP4 to {save_path}")
            stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
            Lestado.insert(END, "Download complete!")
        else:
            Lestado.insert(END, "Download canceled")


def show_video_info():
    url = Eurl.get()
    yt = YouTube(url)
    
    response = requests.get(yt.thumbnail_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img.thumbnail((535, 790))
    img = ImageTk.PhotoImage(img)
    Limagem.config(image=img)
    Limagem.image = img

    Lestado.delete(0, END)
    Lestado.insert(END, f"Título: {yt.title}")
    Lestado.insert(END, f"Visualizações: {yt.views}")
    Lestado.insert(END, f"Duração: {yt.length} segundos")

    url = Eurl.get()
    if not url:
        return

    yt = YouTube(url)

    cmb_qualidade_mp3['values'] = [stream.abr for stream in yt.streams.filter(only_audio=True)]
    cmb_qualidade_mp4['values'] = [stream.resolution for stream in yt.streams.filter(file_extension='mp4')]



janela = customtkinter.CTk()
janela.geometry('500x550+100+100')
janela.resizable(False, False)
janela.title('Portugal Download')
#janela.iconbitmap(r'C:\Users\HP\Desktop\Programas em python\ferramenta Download V2\icon.ico')

URL = customtkinter.CTkLabel(janela, text='URL:')
URL.place(x=10, y=10)

Eurl = customtkinter.CTkEntry(janela, width=400)
Eurl.place(x=40, y=10)

cmb_qualidade_mp3 = Combobox(janela, width=15, font=('arial 14'))
cmb_qualidade_mp3.place(x=50, y=60)
cmb_qualidade_mp3.set('Qualidade mp3')

cmb_qualidade_mp4 = Combobox(janela, width=15, font=('arial 14'))
cmb_qualidade_mp4.place(x=250, y=60)
cmb_qualidade_mp4.set('Qualidade mp4')

BMP3 = customtkinter.CTkButton(janela, text='Download MP3', command=download_mp3)
BMP3.place(x=40, y=80)

BMP4 = customtkinter.CTkButton(janela, text='Download MP4', command=download_mp4)
BMP4.place(x=185, y=80)


Limpar = customtkinter.CTkButton(janela, text='Limpar', command=clear_widgets)
Limpar.place(x=330, y=80)

Limagem = Label(janela, background='white')
Limagem.place(x=50, y=150)

Lestado = Listbox(janela, width=50, height=4, font=('arial 14 '))
Lestado.place(x=50, y=525)

InfoButton = customtkinter.CTkButton(janela, text='Mostrar Informações do Vídeo', command=show_video_info)
InfoButton.place(x=40, y=375)

lautor = customtkinter.CTkLabel(janela, text='© Dev Joel 2023')
lautor.place(x=290, y=375)

janela.mainloop()
