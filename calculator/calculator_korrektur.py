import tkinter  # GUI-Bibliothek importieren
import math     # Mathe-Funktionen für √ importieren

# Beschriftungen der Buttons als 2D-Liste
button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

# Symbole auf der rechten Seite (Operatoren)
right_symbols = ["÷", "×", "-", "+", "="]

# Symbole in der oberen Reihe
top_symbols = ["AC", "+/-", "%"]

# Anzahl der Reihen und Spalten berechnen
row_count = len(button_values)
column_count = len(button_values[0])

# Farben definieren
color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

# Fenster erstellen
window = tkinter.Tk()
window.title("Calculator")        # Fenstertitel setzen
window.resizable(False, False)    # Fenstergröße fixieren

# Rahmen für Anzeige + Buttons
frame = tkinter.Frame(window)

# Display-Label für die Anzeige
label = tkinter.Label(
    frame,
    text="0",                     # Standardanzeige
    font=("Arial", 45),           # Schriftgröße
    background=color_black,       # Hintergrund
    foreground=color_white,       # Schriftfarbe
    anchor="e",                   # Text rechtsbündig
    width=column_count            # Breite in Spalten
)

label.grid(row=0, column=0, columnspan=column_count, sticky="we")  # Anzeige platzieren

# Rechenvariablen initialisieren
A = "0"        # erster Wert
operator = None  # aktueller Operator
B = None         # zweiter Wert


def clear_all():
    """Alles zurücksetzen."""
    global A, B, operator
    A = "0"
    operator = None
    B = None


def remove_zero_decimal(num):
    """Nachkommastellen entfernen, falls Zahl ganzzahlig ist."""
    if num % 1 == 0:
        num = int(num)
    return str(num)


def button_clicked(value):
    """Reaktion auf jeden Buttonklick."""
    global right_symbols, top_symbols, label, A, B, operator

    # Prüfen, ob rechter Operator gedrückt wurde
    if value in right_symbols:

        # Gleichheitszeichen = Ergebnis berechnen
        if value == "=":
            if A is not None and operator is not None:
                B = label["text"]          # B aus Display lesen
                numA = float(A)            # A in Zahl umwandeln
                numB = float(B)            # B in Zahl umwandeln

                try:
                    if operator == "+":
                        label["text"] = remove_zero_decimal(numA + numB)
                    elif operator == "-":
                        label["text"] = remove_zero_decimal(numA - numB)
                    elif operator == "×":
                        label["text"] = remove_zero_decimal(numA * numB)
                    elif operator == "÷":
                        label["text"] = remove_zero_decimal(numA / numB)
                except ZeroDivisionError:
                    label["text"] = "Error"  # Division durch 0

                clear_all()  # Reset nach Berechnung

        # Wenn ein Operator gedrückt wurde (+, -, ×, ÷)
        elif value in "+-×÷":
            if operator is None:          # Nur setzen, wenn kein Operator aktiv
                A = label["text"]         # A speichern
                label["text"] = "0"       # Display zurücksetzen
                B = "0"                   # B vorbereiten
            operator = value              # den neuen Operator setzen

    # Quadratwurzel berechnen
    elif value == "√":
        try:
            num = float(label["text"])
            if num < 0:
                label["text"] = "Error"   # Wurzel aus negativer Zahl = Fehler
                clear_all()
            else:
                result = math.sqrt(num)   # √ berechnen
                label["text"] = remove_zero_decimal(result)
                clear_all()               # Zustand zurücksetzen
        except ValueError:
            label["text"] = "Error"
            clear_all()

    # Obere Funktionsbuttons
    elif value in top_symbols:

        # AC = alles löschen
        if value == "AC":
            clear_all()
            label["text"] = "0"

        # +/- = Vorzeichen invertieren
        elif value == "+/-":
            try:
                result = float(label["text"]) * -1
                label["text"] = remove_zero_decimal(result)
            except ValueError:
                label["text"] = "Error"
                clear_all()

        # % = Prozent rechnen
        elif value == "%":
            try:
                result = float(label["text"]) / 100
                label["text"] = remove_zero_decimal(result)
            except ValueError:
                label["text"] = "Error"
                clear_all()

    # Zahlen oder Dezimalpunkt gedrückt
    else:
        if value == ".":                      # Dezimalpunkt
            if value not in label["text"]:    # Nur erlauben, wenn noch kein Punkt enthalten ist
                label["text"] += value

        elif value in "0123456789":           # Zahl gedrückt
            if label["text"] == "0":          # Anfangs-0 ersetzen
                label["text"] = value
            else:
                label["text"] += value        # Ziffer anhängen


# Buttons erzeugen und formatieren
for row in range(row_count):
    for column in range(column_count):

        value = button_values[row][column]  # Buttonwert holen

        # Button erstellen
        button = tkinter.Button(
            frame,
            text=value,                    # Text auf dem Button
            font=("Arial", 30),            # Schriftgröße
            width=column_count - 1,        # Buttonbreite
            height=1,                      # Buttonhöhe
            command=lambda value=value: button_clicked(value)  # Funktion ausführen
        )

        # Buttonfarbe festlegen
        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_gray)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
        else:
            button.config(foreground=color_white, background=color_dark_gray)

        # Button ins Grid einfügen
        button.grid(row=row + 1, column=column)

# Rahmen in Fenster einfügen
frame.pack()

# Fenster zentrieren
window.update()                        # Größe berechnen
window_width = window.winfo_width()    # Fensterbreite
window_height = window.winfo_height()  # Fensterhöhe
screen_width = window.winfo_screenwidth()   # Bildschirmbreite
screen_height = window.winfo_screenheight() # Bildschirmhöhe

# Mittelpunkt errechnen
window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

# Fensterposition setzen
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Hauptloop starten
window.mainloop()
