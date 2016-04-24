#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
import numpy
from tkinter import Tk, Frame, Button, Scale, HORIZONTAL, Label, LEFT, CENTER, FLAT, GROOVE, filedialog, Entry

def explicit_euler(xs, h, y0, f, **derivatives):
    """Explicit Euler"""
    ys = [y0]
    for k in range(len(xs)):
        next_y = ys[k] + f(xs[k], ys[k]) * h
        ys.append(next_y)

    return ys[:-1]

def implicit_euler(xs, h, y0, f, **derivatives):
    """Implicit Euler"""
    ys = [y0]
    for k in range(len(xs) - 1):
        subsidiary_y = ys[k] + f(xs[k], ys[k]) * h
        next_y = ys[k] + f(xs[k + 1], subsidiary_y) * h
        ys.append(next_y)

    return ys

def cauchy(xs, h, y0, f, **derivatives):
    """Cauchy"""
    ys = [y0]
    for k in range(len(xs) - 1):
        subsidiary_y = ys[k] + f(xs[k], ys[k]) * h / 2
        next_y = ys[k] + f(xs[k] + h / 2, subsidiary_y) * h
        ys.append(next_y)

    return ys

def euler_with_recount(xs, h, y0, f, **derivatives):
    """Euler with recount"""
    ys = [y0]
    for k in range(len(xs) - 1):
        subsidiary_y = ys[k] + f(xs[k], ys[k]) * h
        next_y = ys[k] + (f(xs[k], ys[k]) + f(xs[k], subsidiary_y)) * h / 2
        ys.append(next_y)

    return ys

def runge_kutta(xs, h, y0, f, **derivatives):
    """Runge-Kutta 4th"""
    ys = [y0]
    for k in range(len(xs)):
        k1 = h * f(xs[k], ys[k])
        k2 = h * f(xs[k] + h / 2, ys[k] + k1 / 2)
        k3 = h * f(xs[k] + h / 2, ys[k] + k2 / 2)
        k4 = h * f(xs[k] + h, ys[k] + k3)

        next_y = ys[k] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        ys.append(next_y)

    return ys[:-1]

def extrapolation_adams(xs, h, y0, f, **derivatives):
    """Extra Adams (k=2)"""
    ys = [y0, y0 + h * f(xs[0], y0)]
    for k in range(1, len(xs)):
        next_y = ys[k] + (
             3.0/2.0 * f(xs[k], ys[k]) - 1.0/2.0 * f(xs[k - 1], ys[k - 1])
        ) * h
        ys.append(next_y)

    return ys[:-1]

def taylor_3(xs, h, y0, f, df_x, df_y, **derivatives):
    """Taylor 3rd"""
    ys = [y0]
    for k in range(0, len(xs)):
        next_y = ys[k] + f(xs[k], ys[k])*h + (
             df_x(xs[k], ys[k]) + df_y(xs[k], ys[k])*f(xs[k], ys[k])
        ) * (h ** 2) / 2
        ys.append(next_y)

    return ys[:-1]

def taylor_4(xs, h, y0, f, df_x, df_y, df_xx, df_yy, df_xy, **derivatives):
    """Taylor 4rd"""
    ys = [y0]
    for k in range(len(xs)):
        second_summand = f(xs[k], ys[k]) * h
        third_summand = (
            df_x(xs[k], ys[k]) + df_y(xs[k], ys[k]) * f(xs[k], ys[k])
        ) * (h ** 2) / 2
        fourth_summand = (
             df_xx(xs[k], ys[k]) + 2 * f(xs[k], ys[k]) * df_xy(xs[k], ys[k]) +
             df_yy(xs[k], ys[k]) * (f(xs[k], ys[k]) ** 2) +
             df_y(xs[k], ys[k]) * (
                 df_x(xs[k], ys[k]) + df_y(xs[k], ys[k]) * f(xs[k], ys[k]))
        ) * (h ** 3) / 3
        next_y = ys[k] + second_summand + third_summand + fourth_summand
        ys.append(next_y)

    return ys[:-1]
	
task = {
        'y0': 				0.1,
        'f': 				lambda x, y: 30 * y * (x - 0.2) * (x - 0.7),
        'df_x': 			lambda x, y: y * (60 * x - 27),
        'df_xx': 			lambda x, y: y * 60,
        'df_y': 			lambda x, y: 30 * (x - 0.7) * (x - 0.2),
        'df_yy': 			lambda x, y: 0,
        'df_xy': 			lambda x, y: 60 * x - 27,
        'original_func': 	lambda x: 0.1 * math.exp(x * (10 * x * x - 13.5 * x + 4.2)),
}

methods = [
    (taylor_3, 'g^-'),
    (taylor_4, 'gs-'),
	(runge_kutta, 'yd-'),
	(extrapolation_adams, 'ko-'),
	(cauchy, 'b8-'),
	(implicit_euler, 'r--'),
    (explicit_euler, 'r8-'),
    (euler_with_recount, 'rs-'),
]

def Paint(numberOfPoints):
    plt.close()
    x_points = numpy.linspace(0, 1, numberOfPoints)
    for method, color in methods:
        plt.plot(x_points, method(x_points, 1 / (numberOfPoints + 1), **task), color, label=method.__doc__)
    plt.plot(x_points, list(map(task['original_func'], x_points)), 'b*-', label='Original')

    legend = plt.legend(loc='upper left', shadow=True, fontsize='x-large')
    legend.get_frame().set_facecolor('#00FF00')

    mng = plt.get_current_fig_manager()

    mng.window.state('zoomed')
    plt.show()

def main():

	window = Tk()
	window.title('A. Dobrunov')
	window.resizable(width=False, height=False)
	color1 = 'lightgreen'
	frame = Frame(window, bg=color1)
	frame.pack()
	Label(frame, text="Laborarbeit № 1 , Variante № 1\n", justify=CENTER, font=("Helvetica", 12), bd=10, bg=color1).pack()
	Label(frame, text="\n Punkte:", justify=CENTER, font=("Helvetica", 12), bd=0, bg=color1).pack()
	e = Entry(frame, bd = 2)
	e.pack()
	Label(frame, text='\n', bg=color1).pack()
	button = Button(frame, text="Ausführen", font=("Helvetica", 12), bg='white', command=lambda: Paint(int(e.get())))
	button.pack()
	window.mainloop()
	
if __name__ == "__main__":
	main()