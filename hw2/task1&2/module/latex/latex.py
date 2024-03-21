latex_row_elems_separator = ' & '
latex_row_endl            = ' \\\\'
latex_row_separator       = '\n\\hline\n'
latex_cs_separator        = '|'

latex_table_format = """\\begin{{table}}
\\caption{{Auto generated table}}
\\centering
\\begin{{tabular}}{{{cs}}}
{rows}
\\end{{tabular}}
\\end{{table}}
"""

latex_image_format = """\\begin{{figure}}
\\caption{{Auto generated image}}
\\centering
\\includegraphics[width=0.5\\textwidth]{{\"{image}\"}}
\\end{{figure}}
"""

latex_document_format = """\\documentclass[a4paper,11pt]{{article}}
\\usepackage{{graphicx}}
\\usepackage{{geometry}}
\\geometry{{left=25mm,right=25mm,%
bindingoffset=0mm, top=20mm,bottom=20mm}}
\\linespread{{1.9}}
\\begin{{document}}
{table}
{image}
\\end{{document}}
"""


def generate_latex_table(table):
    if table is None:
        return ""
    global latex_row_elems_separator
    global latex_row_endl
    global latex_row_separator
    global latex_cs_separator
    global latex_table_format

    columns_ct = len(table[0])
    cs = latex_cs_separator + latex_cs_separator.join(['c'] * columns_ct) + latex_cs_separator
    rows= latex_row_separator + latex_row_separator.join(map(lambda row: f'{latex_row_elems_separator.join(map(str, row))}{latex_row_endl}', table)) + latex_row_separator
    return latex_table_format.format(cs = cs, rows = rows)


def generate_latex_image(image):
    if image is None:
        return ""
    global latex_image_format
    return latex_image_format.format(image = image)


def generate_latex(table = None, image = None):
    return latex_document_format.format(
        table = generate_latex_table(table),
        image = generate_latex_image(image)
    )
