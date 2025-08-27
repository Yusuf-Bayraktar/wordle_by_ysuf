import tkinter as tk
import random

with open("5 harfli_zemberek.txt", 'r') as file:
    dosya = file.read()

kelimeler = dosya.split()

screen = tk.Tk()

screen_width = screen.winfo_screenwidth() - 640
screen_height = screen.winfo_screenheight() - 360
screen.geometry(f"{screen_width}x{screen_height}")
screen.config(bg="gray10")

label_size = 50
labels = []
buttons = []

widths = (50, 30, 25, 40)
heights = (50, 40)

harfler = ("E", "R", "T", "Y", "U", "I", "O", "P", "Ğ", "Ü", "A", "S", "D", "F", "G", "H", "J", "K", "L",
           "Ş", "İ", "ENTER", "Z", "C", "V", "B", "N", "M", "Ö", "Ç", "<-")

yazilan_kelime = ""
yazilan_leimeler = ["     ", "     ", "     ", "     ", "     ", "     "]
yazi_index = 0

secilen_kelime = kelimeler[random.randint(0, len(kelimeler) - 1)]
print(secilen_kelime)


def label_place():
    global screen_width, screen_height, label_size

    for k in range(6):
        for ll in range(5):
            labels[k * 5 + ll].place(width=label_size, height=label_size,
                                     x=((screen_width / 2 - label_size / 2) + (ll - 2) * (label_size + 10)),
                                     y=((screen_height / 2 - label_size / 2) - (4.5 - k) * (label_size + 10)))


def button_place():
    global screen_width, screen_height
    for m in range(31):
        if m < 10:
            buttons[m].place(width=30, height=40,
                             x=((screen_width / 2 - 30 / 2) + (m - 4) * (30 + 5) - 15),
                             y=screen_height / 1.4)
        elif m < 21:
            buttons[m].place(width=25, height=40,
                             x=((screen_width / 2 - 30 / 2) + (m - 15) * (25 + 5) + 5),
                             y=screen_height / 1.4 + 45)
        elif m == 21 or m == 30:
            buttons[m].place(width=40, height=40,
                             x=((screen_width / 2 - 40 / 2) + (m - 25) * (30 + 5) - 20 + (m - 20)),
                             y=screen_height / 1.4 + 90)
        else:
            buttons[m].place(width=30, height=40,
                             x=((screen_width / 2 - 30 / 2) + (m - 25) * (30 + 5) - 15),
                             y=screen_height / 1.4 + 90)


def label_yaz():
    global yazilan_leimeler
    for n in range(6):
        for o in range(5):
            labels[n * 5 + o].config(text=yazilan_leimeler[n][o])


def kontrol():
    global yazilan_leimeler, yazi_index, labels
    yazilmis_kelime = yazilan_leimeler[yazi_index]
    secilen_kelime2 = secilen_kelime.upper()

    if secilen_kelime2 != yazilmis_kelime:
        yazilmis_kelime = yazilmis_kelime.replace("İ", "I")

    secilen_kelime_count = {}
    for a in secilen_kelime2:
        secilen_kelime_count[a] = secilen_kelime2.count(a)

    for iki in range(5):
        if yazilmis_kelime[iki] in secilen_kelime2 and yazilmis_kelime[iki] != secilen_kelime2[iki]:
            if secilen_kelime_count[yazilmis_kelime[iki]] > 0:
                labels[yazi_index * 5 + iki].config(bg="yellow")
                buttons[(harfler.index(yazilmis_kelime[iki]))].config(bg="yellow")
                secilen_kelime_count[yazilmis_kelime[iki]] -= 1
        else:
            buttons[(harfler.index(yazilmis_kelime[iki]))].config(bg="gray20")

    print(secilen_kelime_count)

    for bir in range(5):
        if yazilmis_kelime[bir] == secilen_kelime2[bir]:
            labels[yazi_index * 5 + bir].config(bg="green")
            buttons[(harfler.index(secilen_kelime2[bir]))].config(bg="green")
            secilen_kelime_count[secilen_kelime2[bir]] -= 1
        else:
            pass
            # buttons[(harfler.index(yazilmis_kelime[bir]))].config(bg="gray20")

    print(secilen_kelime_count)


for i in range(6):
    for j in range(5):
        labels.append(tk.Label(screen, text="", font=("Calibry", "30"), bg="gray20", fg="white"))

label_place()

for i in range(31):
    def click_event(text=i):
        global yazilan_kelime, harfler, yazilan_leimeler, yazi_index
        if text == 21:
            if len(yazilan_kelime) == 5:
                if yazi_index > 5:
                    pass
                else:
                    kontrol()
                    yazi_index += 1
                    yazilan_kelime = ""
        elif text == 30:
            if len(yazilan_kelime) > 0:
                yazilan_kelime = yazilan_kelime[0:len(yazilan_kelime) - 1]
        else:
            if len(yazilan_kelime) < 5:
                yazilan_kelime += harfler[text]

        yazilan_leimeler[yazi_index] = yazilan_kelime + (5 - len(yazilan_kelime)) * " "
        label_yaz()


    buttons.append(tk.Button(screen, text=harfler[i], bg="gray35", fg="white", relief="flat", command=click_event))

button_place()


def resize(e):
    global screen_width
    global screen_height
    width = e.width
    height = e.height
    if (width not in widths) and (height not in heights):
        screen_width = width
        screen_height = height
        label_place()
        button_place()


screen.bind("<Configure>", resize)

screen.mainloop()
