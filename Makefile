PYTHON ?= python3

.PHONY: validate paper clean

validate:
	$(PYTHON) scripts/validate.py
	$(PYTHON) scripts/test_validator.py

paper:
	@if command -v latexmk >/dev/null 2>&1; then \
		cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex; \
	else \
		cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex && \
		bibtex main && \
		pdflatex -interaction=nonstopmode -halt-on-error main.tex && \
		pdflatex -interaction=nonstopmode -halt-on-error main.tex; \
	fi

clean:
	@if command -v latexmk >/dev/null 2>&1; then cd paper && latexmk -C main.tex; fi
	rm -f paper/main.aux paper/main.bbl paper/main.blg paper/main.fdb_latexmk
	rm -f paper/main.fls paper/main.log paper/main.out paper/main.pdf
	rm -f paper/main.synctex.gz paper/main.toc
