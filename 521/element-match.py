#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>

import argparse
import itertools

import numpy as np
import matplotlib.pyplot as pl
import pandas as pd
import scipy.integrate

colors = [
    '#e41a1c',
    '#377eb8',
    '#4daf4a',
    '#984ea3',
    '#ff7f00',
    '#ffff33',
    '#a65628',
]

colors = [
'#a6cee3',
'#1f78b4',
'#b2df8a',
'#33a02c',
'#fb9a99',
'#e31a1c',
'#fdbf6f',
'#ff7f00',
'#cab2d6',
'#6a3d9a',
'#b15928',
]

linestyles = [
    'solid',
    'dashed',
]

def lorentz_peak(x, mean, width, area, offset):
    return area / np.pi * width/2 / ((x - mean)**2 + (width/2)**2) + offset

def load_lines():
    filename = 'Daten/generiesb.dat'
    data = pd.read_csv(filename, header=0, delim_whitespace=True)

    return data

def get_peaks():
    return np.loadtxt('Daten/Langzeit_Peaks.dat')

def main():
    options = _parse_args()

    messwerte = np.loadtxt('_build/langzeit.tsv')

    messwerte = messwerte[messwerte[:, 0] > 200]

    print(messwerte.shape)

    peaks = get_peaks()

    lines = load_lines()

    pad = 2

    elements = list(set(lines['Nuclide']))
    print(elements)

    fig = pl.figure()
    ax = fig.add_subplot(1, 1, 1)

    results = {}

    m = 0

    attr_iter = itertools.product(linestyles, colors)

    exclude = [
            '11-Na-22',
            '21-Sc-46',
            '25-Mn-54',
            '25-Mn-56',
            '27-Co-56',
            '27-Co-58',
            '27-Co-60',
            '30-Zn-65',
            '31-Ga-66',
            '36-Kr-85',
            '38-Sr-85',
            '41-Nb-95',
            '44-Ru-106',
            '45-Rh-106',
            '55-Cs-134',
            '67-Ho-166',
            '88-Ra-224',
    ]

    for element in elements:
        if element in exclude:
            continue

        selection = lines['Nuclide'] == element
        selected = lines[selection]

        x = messwerte[:, 0]
        y = np.zeros(x.shape)

        for id, energy, delta_energy, sigma_val, sigma_err, nuclide in selected.itertuples():
            y += lorentz_peak(x, energy, 1.5, sigma_val, 0)


        self_integral = scipy.integrate.simps(y, x)
        overlap = y * messwerte[:, 1]
        overlap_integral = scipy.integrate.simps(overlap, x)

        matchness = overlap_integral / self_integral

        if matchness >= +0:
            linestyle, color = next(attr_iter)
            ax.plot(x, y / self_integral, label=nuclide, color=color, linestyle=linestyle, linewidth=4)

        results[element] = matchness

        m = max(m, np.max(y))



    ax.legend(loc='best')

    m2 = np.max(messwerte[:, 1])

    print('m', m)
    print('m2', m2)
    scale = ax.get_ylim()[1] / m2
    print('Scale', scale)

    ax.plot(x, messwerte[:, 1] * scale, alpha=0.3, color='black')

    ax.grid(True)
    ax.margins(.05)
    fig.tight_layout()
    fig.show()
    input()
    fig.savefig('test.pdf')

    results_sorted = sorted([(matchness, element) for element, matchness in results.items()])

    for matchness, element in results_sorted:
        print('{:5s} {:+.10f}'.format(element, matchness))



    for peak in peaks[:2]:
        print(peak)

        selection = (lines['E(gamma)'] < (peak + pad)) & (lines['E(gamma)'] > (peak - pad))
        selected = lines[selection]

        sorted_ = selected.sort_values(by='P', ascending=False)

        print(sorted_)

        break

        for id, iso, z, energy, i1, i2, i3 in selected.itertuples():
            print(iso, energy)

            selection2 = lines['Nuclide'] == iso
            selected2 = lines[selection2]

            print(selected2)

        print()


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    options = parser.parse_args()

    return options

if __name__ == '__main__':
    main()
