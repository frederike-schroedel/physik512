# Copyright © 2013-2015 Martin Ueding <dev@martin-ueding.de>
# Licensed under The MIT License

number = 525

all_eps := $(wildcard Daten/*.GZ)
all_pdf := $(all_eps:Daten/%.GZ=_build/%.png)

all: $(all_pdf)

.PRECIOUS: %.png %.pdf

_build:
	mkdir -p _build

_build/%.ps: Daten/%.GZ _build
	gzip -d -c $< > $@

%-temp.pdf : %.ps
	ps2pdf $< $@

%-000.ppm: %-temp.pdf
	pdfimages $< $(@:-000.ppm=)

%.png: %-000.ppm
	convert $< -rotate 90 -negate $@

%.pdf : %-temp2.pdf
	pdfcrop $< $@

all: $(all_pdf)

include ../makefile.in
