# c'est une bibliothèque pour qu'on peut calculer l'integrale
from numpy import sin, cos, exp, log, sqrt
from scipy.integrate import quad
from pylab import *
from tkinter import ttk
import tkinter as tk
from tkinter import BOTH, END, LEFT
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib
matplotlib.use('TkAgg')


class Application(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)

        #self.attributes('-fullscreen', True)
        self.creer_widgets()

    def creer_widgets(self):

        self.grid()

        # Création du labelCombox
        self.labelcombo = tk.Label(self, text="Choisir la méthode:", font=(
            'Times', 12, 'underline'), bg='lavender', width=16, height=5)
        self.labelcombo.grid(row=1, column=3, padx=8, pady=5)
        # création du listBox
        self.numero = tk.StringVar()
        self.listeCombo = ttk.Combobox(
            self, width="28", textvariable=self.numero)
        self.listeCombo['values'] = (
            ' Méthode des rectangles', ' Point Milieux', ' Méthode de simpson', ' Methode des trapèzes')
        self.listeCombo.grid(row=1, column=4, padx=3, pady=10)
        self.listeCombo.current(0)
        # Création du label
        self.label = tk.Label(self, text="Saisir la fonction: ",
                              font=("Times", 12), bg='lavender')
        self.label.grid(row=2, column=3, padx=2, pady=5)
        self.txt_f = tk.Entry(self, width=28)
        self.txt_f.grid(row=2, column=4, padx=2, pady=5)
        self.txt_f.insert(0, "cos(x)")
        # Création du label a
        self.label_a = tk.Label(
            self, text="Saisir la valeur a:  ", font=("Times", 12), bg='lavender')
        self.label_a.grid(row=3, column=3, padx=2, pady=5)
        self.txt_a = tk.Entry(self, width=28)
        self.txt_a.grid(row=3, column=4, padx=2, pady=5)
        self.txt_a.insert(0, "-1")
        # Création du label b
        self.label_b = tk.Label(
            self, text="Saisir la valeur b:  ", font=("Times", 12), bg='lavender')
        self.label_b.grid(row=4, column=3, padx=2, pady=5)
        self.txt_b = tk.Entry(self, width=28)
        self.txt_b.grid(row=4, column=4, padx=2, pady=5)
        self.txt_b.insert(0, "2")
        # Création du label n
        self.label_n = tk.Label(
            self, text="Saisir la valeur n:  ", font=("Times", 12), bg='lavender')
        self.label_n.grid(row=5, column=3, padx=2, pady=5)
        self.txt_n = tk.Entry(self, width=28)
        self.txt_n.grid(row=5, column=4, padx=2, pady=5)
        self.txt_n.insert(0, "10")

        ##--fonction Réinitialiser -----##
        def initialiser():

            self.txt_f.delete(0, END)
            self.txt_a.delete(0, END)
            self.txt_b.delete(0, END)
            self.txt_n.delete(0, END)
            self.txt_f.focus_set()

        ##----- Création des boutons -----##
        self.bouton1 = tk.Button(self, text='Calculer', width='15', bg='light slate blue', font=(
            'calibri', 10, 'bold',), borderwidth='4', command=self.plot)
        self.bouton1.grid(row=6, column=4, pady=10, padx=55)

        self.bouton = tk.Button(self, text='Rénitialiser', width='12', bg='light slate blue', font=(
            'calibri', 10, 'bold'), borderwidth='4', command=initialiser)
        self.bouton.grid(row=9, column=6, pady=10, padx=5)

        self.boutonQ = tk.Button(self, text='Quitter', width='12', bg='light slate blue', font=(
            'calibri', 10, 'bold'), borderwidth='4', command=self.destroy)
        self.boutonQ.grid(row=9, column=7, pady=10, padx=5)

        # grphe
        self.fig = Figure(figsize=(4, 3))
        self.a = self.fig.add_subplot(111)
        self.a.set_title("Graphe de f", fontsize=16)
        self.a.set_ylabel("y=f(x)", fontsize=14)
        self.a.set_xlabel("x", fontsize=14)
        self.a.set_facecolor("gray")
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(column=4, row=7, columnspan=34)

        self.canvas.draw()

    def plot(self):

        self.f = lambda x: eval(self.txt_f.get())
        self.a.grid(True)
        methode = self.listeCombo.get()
        print(methode)
        if methode == ' Methode des trapèzes':
            self.Trapezoidal(self.f)

        elif methode == ' Point Milieux':
            self.Milieu(self.f)
        elif methode == ' Méthode des rectangles':
            self.RectangleG(self.f)
        elif methode == ' Méthode de simpson':
            self.Simpson(self.f)
        else:
            print("erreur")

     # Méthode des rectangles:

    def RectangleG(self, f, resolution=1001):
        self.a_ = int(self.txt_a.get())
        self.b = int(self.txt_b.get())
        self.n = int(self.txt_n.get())
        self.x = np.linspace(self.a_, self.b, self.n+1)
        xl = self.x
        yl = f(xl)
        xlist_fine = np.linspace(self.a_, self.b, resolution)
        for i in range(self.n):
            # abscisses des sommets
            x_rect = [xl[i], xl[i], xl[i+1], xl[i+1], xl[i]]
            y_rect = [0, yl[i], yl[i], 0, 0]  # ordonnees des sommets
            self.a.plot(x_rect, y_rect, "m")
        yflist_fine = f(xlist_fine)
        self.a.plot(xlist_fine, yflist_fine)  # plot de f(x)
        self.a.plot(xl, yl, "rd")  # point support
        self.a.set_title('Methode des rectangle')
        self.a.set_ylabel(' f ( x ) ')
        self.a.set_xlabel(' x ')
        self.canvas.draw()

  # Méthode des trapèzes:
    def Trapezoidal(self, f, resolution=1001):
        self.a_ = int(self.txt_a.get())
        self.b = int(self.txt_b.get())
        self.n = int(self.txt_n.get())
        self.x = np.linspace(self.a_, self.b, self.n+1)
        xl = self.x
        yl = f(xl)
        xlist_fine = np.linspace(self.a_, self.b, resolution)
        for i in range(self.n):
            # abscisses des sommets
            x_rect = [xl[i], xl[i], xl[i+1], xl[i+1], xl[i]]
            y_rect = [0, yl[i], yl[i+1], 0, 0]  # ordonnees des sommets
            self.a.plot(x_rect, y_rect, "m")
        yflist_fine = f(xlist_fine)
        self.a.plot(xlist_fine, yflist_fine)  # plot de f(x)
        self.a.plot(xl, yl, "cs")  # point support
        self.a.set_title('Methode des trapèzes')
        self.a.set_ylabel(' f ( x ) ')
        self.canvas.draw()
    # Méthode de Simpson:

    def Simpson(self, f, resolution=1001):
        self.a_ = int(self.txt_a.get())
        self.b = int(self.txt_b.get())
        self.n = int(self.txt_n.get())
        self.x = np.linspace(self.a_, self.b, self.n+1)
        xl = self.x
        yl = f(xl)
        xlist_fine = np.linspace(self.a_, self.b, resolution)
        for i in range(self.n):  # range intervalle 0 à n
            xx = np.linspace(self.x[i], self.x[i+1], resolution)
            # pour chaque subdivisuion  on doit dessiner polynome dnc on doit aussi le subdiviser
            m = (xl[i]+xl[i+1])/2  # pt milieu
            a = xl[i]  # borne gauche
            b = xl[i+1]  # borne droite
            l0 = (xx-m)/(a-m)*(xx-b)/(a-b)
            l1 = (xx-a)/(m-a)*(xx-b)/(m-b)
            l2 = (xx-a)/(b-a)*(xx-m)/(b-m)
            P = f(a)*l0 + f(m)*l1 + f(b)*l2  # fnees des sommets
            self.a.plot(xx, P, "m")
        yflist_fine = f(xlist_fine)
        self.a.plot(xlist_fine, yflist_fine)  # plot de f(x)
        self.a.plot(xl, yl, "wp")  # point support
        self.a.set_title('Methode des simpson')
        self.a.set_ylabel(' f ( x ) ')
        self.a.set_xlabel(' x ')
        self.canvas.draw()

        # Méthode des Points Milieux :

    def Milieu(self, f, resolution=1001):
        self.a_ = int(self.txt_a.get())
        self.b = int(self.txt_b.get())
        self.n = int(self.txt_n.get())
        self.x = np.linspace(self.a_, self.b, self.n+1)
        xl = self.x
        yl = f(xl)
        xlist_fine = np.linspace(self.a_, self.b, resolution)
        for i in range(self.n):
            self.m = (xl[i]+xl[i+1])/2
            # abscisses des sommets
            x_rect = [xl[i], xl[i], xl[i+1], xl[i+1], xl[i]]
            # ord # ordonnees des sommets
            y_rect = [0, f(self.m), f(self.m), 0, 0]
            self.a.plot(x_rect, y_rect, "m")
        yflist_fine = f(xlist_fine)
        self.a.plot(xlist_fine, yflist_fine)  # plot de f(x)
        self.a.plot(self.m, f(self.m), "y*")
        # self.a.plot(xl, yl,"cs")#point support
        self.a.set_title('Methode des milieu')
        self.a.set_ylabel(' f ( x ) ')
        self.a.set_xlabel(' x ')
        self.canvas.draw()


if __name__ == "__main__":
    app = Application()
    app.title("Intégration numérique")
    app.geometry("700x650")
    app.resizable(width=False, height=False)
    app.configure(bg='lavender')

    ##----- Programme principal -----##
    app.mainloop()  # Boucle d'attente des événements
