#importowanie bibliotek niezbednych do dzialania kalkulatora
import tkinter as tk
import math

#funkcja otwierajaca okno kalkulatora
def openWindow():
    window = tk.Tk() #zainicjowanie interpretera tkinter i utworznie okna glownego
    window.title('Kalkulator') #nazwa w oknie programu
    return window

#funkcja generujaca podglad wykonywanych dzialan matematycznych w oknie
def showPreview(window):
    preview = tk.Label(window, width = 32) #implementacja pola wyswietlania
    preview.grid(columnspan = 5)  #umieszczenie pola w strukturze okna
    return preview

#funkcja generujaca pole do wprowadzania danych
def showScreen(window):
    screen = tk.Entry(window, width = 24, bg="light grey") #implementaccja pola do wprowadzania danych
    screen.grid(columnspan = 5, pady= (0,10)) #umieszczenie pola w strukturze okna
    return screen

#tablica symboli klawiatury (bez znaku rownosci)
symbol_table = ['%', 'π', 'e', 'C', '←',
                'x^2', 'sin', 'cos', 'tan', 'ctg',
                '√x', '(', ')', 'n!', '/',
                'x^y', '7','8', '9', '*',
                '10^x', '4', '5', '6', '-',
                'log', '1', '2', '3', '+',
                'In', '+/-', '0', '.']

#funkcja generujaca klawisze kalkulatora
def showButtons(window, screen):
    buttons = [tk.Button(window, text = symbol, borderwidth = 0) for symbol in symbol_table] #implementacja przyciskow
    #petla umieszczajaca przyciski w glownym oknie
    row = 2
    for i in range(len(buttons)):
        if i % 5 == 0:
            row += 1
        margin = 4 - len(symbol_table[i])
        buttons[i].grid(row = row, column = i % 5, ipadx = margin, pady= (0,10)) #umieszczenie przyciskow w strukturze okna
        buttons[i].configure(command=buttonAction(screen, buttons[i]["text"], preview)) #przypisanie przyciskom funkcji

    equal = tk.Button(window, text = "=", command = equalAction(screen, preview), borderwidth = 0) #implementacja przycisku "="
    equal.grid(row = 9, column = 4, pady= (0,10)) #umieszczenie przycisku w strukturze okna
    return buttons

#funkcja wywolujaca akcje po kliknieciu przycisku
def buttonAction(screen, symbol, preview):
    def click():
        try:
            if symbol == "←":
                operations = screen.get()[:-1] #przypisanie bez ostatniego znaku
                screen.delete(0, tk.END) #wyczyszczenie pola do wprowadzania danych
                screen.insert(0, operations) #umieszczenie w polu usunietego ciagu bez ostatnniego elementu
            elif symbol == "C":
                preview['text'] = "" #wyczyszczenie pola wyswietlania
                screen.delete(0, tk.END)
            else:
                #operacje matematyczne
                if symbol == "%":
                    preview['text'] = ""
                    value = float(screen.get())
                    value = value / 100
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, value)
                elif symbol == "x^2":
                    screen.insert(tk.END, "^2")
                elif symbol == "√x":
                    x = float(screen.get())
                    preview['text'] = "√", x, "="
                    value = math.sqrt(x)
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, value)
                elif symbol == "x^y":
                    screen.insert(tk.END, "^")
                elif symbol == "10^x":
                    screen.insert(tk.END, "10^")
                elif symbol == "log":
                    x = float(screen.get())
                    preview['text'] = "log(", x, ")", "="
                    value = math.log10(x)
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, value)
                elif symbol == "In":
                    x = float(screen.get())
                    preview['text'] = "In(", x, ")", "="
                    value = math.log10(x)/math.log10(math.e)
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, value)
                elif symbol == "π":
                    value = math.pi
                    screen.insert(tk.END, value)
                elif symbol == "e":
                    value = math.e
                    screen.insert(tk.END, value)
                elif symbol == "sin":
                    x = float(screen.get())
                    preview['text'] = "sin(", x, ")", "="
                    value = math.sin(math.radians(x))
                    value = round(value, 3)
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, value)
                elif symbol == "cos":
                    x = float(screen.get())
                    preview['text'] = "cos(", x, ")", "="
                    value = math.cos(math.radians(x))
                    value = round(value, 3)
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, value)
                elif symbol == "tan":
                    x = float(screen.get())
                    preview['text'] = "tan(", x, ")", "="
                    value = math.tan(math.radians(x))
                    value = round(value, 3)
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, value)
                elif symbol == "ctg":
                    x = float(screen.get())
                    preview['text'] = "ctg(", x, ")", "="
                    value = 1 / math.tan(math.radians(x))
                    value = round(value, 3)
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, value)
                elif symbol == "n!":
                    n = float(screen.get())
                    preview['text'] = n, "!", "="
                    def silnia(n): #funkcja obliczajaca silnie
                        return n * silnia(n - 1) if n > 1 else 1
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, silnia(n))
                elif symbol == "+/-":
                    value = float(screen.get())
                    if value != 0:
                        screen.delete(0, tk.END)
                        value *= -1
                        screen.insert(tk.END, value)
                else:
                    screen.insert(tk.END, symbol) #umieszczenie symbolu w polu do wprowadzania danych
        except:
            preview['text'] = "Nieprawidłowe dane wejściowe" #wyswietlanie w przypadku bledu
    return click

#funkcja przypisana do przycisku "="
def equalAction(screen, preview):
    def calculate():
        operations = screen.get() #przypisanie zawartosci pola do wprowadzania danych
        try:
            preview['text'] = str(operations) + ' =' #wyswietlenie aktualnie przeprowadzanych dzialan matematycznych
            #petla zamieniajaca znak "^" na "**" w celu obliczenia poteg
            r = len(operations)
            i = 1
            while i < r:
                if operations[i] == "^":
                    r += 1
                    operations = operations[ : i] + "**" + operations[i + 1 : ] #zastepowanie symbolu "^" -> "**"
                i += 1
            screen.delete(0, tk.END)
            screen.insert(0, str(eval(operations))) #wyswietlenie wyniku obliczanego dzialania matematycznego
        except:
            preview['text'] = "Nieprawidłowe dane wejściowe" #wyswietlanie w przypadku bledu
            screen.insert(tk.END, operations) #umieszczenie w polu do wprowadzania danych dzialan w celu naniesienia poprawek
    return calculate

#wywolanie funkcji
window = openWindow()
preview = showPreview(window)
screen = showScreen(window)
buttons = showButtons(window, screen)
window.mainloop() #uniemozliwa zamkniecie okna bez zgody uzytkownika