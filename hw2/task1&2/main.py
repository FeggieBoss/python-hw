from module import generate_latex

# task2 import
import subprocess

path_to_artifacts      = '../artifacts'
path_to_task1_artifact = f'{path_to_artifacts}/task1'
path_to_task2_artifact = f'{path_to_artifacts}/task2'
path_to_image          = '../../PNG_transparency_demonstration_1.png' # local path from 'artifacts/task2'

def task1(table):
    with open(f'{path_to_task1_artifact}/task1.tex', 'w') as task1tex:
        task1tex.write(generate_latex(table = table))

def task2(table, image):
    with open(f'{path_to_task2_artifact}/task2.tex', 'w') as task2tex:
        task2tex.write(generate_latex(table = table, image = image))

def generate_pdf():
    subprocess.run([
        'pdflatex',                                     # CMD
        '-interaction=batchmode',                       # interaction (batchmode hides most of the stdout/cerr)
        f'-output-directory={path_to_task2_artifact}/', # output-directory
        f'{path_to_task2_artifact}/task2.tex'           # input-file
    ], check = True)

if __name__ == "__main__":
    # 5x5 table    
    table55 = [[f'(row={i}, col={j})' for j in range(5)] for i in range(5)]
    task1(table55)

    # png image from PNG — Википедия    
    image = path_to_image
    task2(table55, image)

    # generating pdf for task2
    generate_pdf()
