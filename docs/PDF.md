# PDF skill guide

The `pdf` skill handles common local PDF inspection tasks without cloud services.

## Commands

```bash
agentbroko pdf info report.pdf
agentbroko pdf text report.pdf
agentbroko pdf text report.pdf --output report.txt
agentbroko pdf render report.pdf --output report-pages --dpi 180
```

`info` uses Poppler's `pdfinfo`, `text` uses the optional `pypdf` package, and `render` uses Poppler's `pdftoppm` to create PNG page previews. Rendering is useful for checking layout rather than relying on extracted text alone.

## Install optional dependencies

```bash
python -m pip install pypdf
```

Install Poppler separately:

- Windows: install a Poppler build and add its `bin` folder to PATH.
- macOS: `brew install poppler`
- Debian/Ubuntu: `sudo apt install poppler-utils`

The skill preserves source PDFs and writes extracted text or rendered pages only where you specify. Do not commit private documents or generated page images.

