# The Evolutionary Map of the Entire Universe — LaTeX Project

## Files
- `main.tex` — main manuscript with embedded TikZ figures
- `references.bib` — BibLaTeX reference database
- `simulation.py` — proof-of-concept chiral field integration

## Compilation

### Method 1: xelatex + biber (recommended)
```bash
xelatex main
biber main
xelatex main
xelatex main
