"""Create a portable analysis notebook using the same implementation as the CLI."""
from pathlib import Path
import nbformat as nbf

root = Path(__file__).resolve().parents[1]
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
source = (root/"analysis.py").read_text().split("# NOTEBOOK_BOUNDARY")[0]
cells = [
    md("""# Student Learning Analytics
**A practical application of the data-analysis skills developed through PCAD certification.**

Explore study-time categories, school absences and final grades using a reproducible workflow: validate → describe → compare → communicate.

**بالعربي:** ندرس العلاقات الموجودة في البيانات، مع التفريق بين الارتباط والسببية، ومراجعة حجم كل مجموعة قبل تفسير متوسطها.

This notebook uses the Portuguese-course file from the UCI Student Performance dataset. It is an independent practice project, not an official PCAD assessment."""),
    code("""# If needed in Colab, uncomment and run:
# %pip install numpy==2.3.5 pandas==2.2.3 matplotlib==3.10.8 scipy==1.17.0
from pathlib import Path
from IPython.display import display, Image
import sys
print('Python:', sys.version.split()[0])"""),
    md("""## 1. Data source and questions
1. How are final grades and absences distributed?
2. How do final-grade averages vary across reported study-time categories?
3. Does separating the two schools change the picture?
4. How sensitive are selected correlations to recorded zero final grades?

Data attribution: Cortez, P. (2008), [Student Performance, UCI](https://doi.org/10.24432/C5TG7T), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This is an existing historical dataset, not data collected for this project.

The next cell uses the included CSV. If the notebook is uploaded alone to Colab, it downloads that file from UCI. No third-party credentials are needed."""),
    code("""DATA_PATH = Path('data/raw/student-por.csv')
if not DATA_PATH.exists():
    import urllib.request, zipfile, io
    url = 'https://archive.ics.uci.edu/static/public/320/student+performance.zip'
    archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url, timeout=30).read()))
    inner = zipfile.ZipFile(io.BytesIO(archive.read('student.zip')))
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_bytes(inner.read('student-por.csv'))
print('Input ready:', DATA_PATH)"""),
    md("## 2. Reusable analysis functions\nThis cell contains the same functions as `analysis.py`. Run it once; subsequent cells inspect the outputs step by step."),
    code(source),
    md("""## 3. Validate before interpreting
Selected variables: school, study-time category, absences, and grades G1/G2/G3. Check required fields, categories, integer values and allowed ranges. Preserve zero grades and matching selected profiles.

**قرار مهم:** تشابه صفّين بعد اختيار عدد قليل من الأعمدة لا يثبت أنهما لنفس الطالب. لا نحذفهما دون دليل."""),
    code("""result = run_analysis(DATA_PATH, 'results', seed=42)
display(result['audit'])
display(result['data'].describe(include='all'))"""),
    md("## 4. Start with distributions\nA mean alone hides the shape of the data. Recorded zero grades stay in the main analysis."),
    code("display(Image(filename='results/distributions.png'))"),
    md("""## 5. Compare groups, including uncertainty
Study time is an **ordered category**, not an exact number of hours. Show group size and grade distribution summaries alongside means.

The intervals below are 95% percentile intervals from 2,000 row-bootstrap resamples per group. They assume exchangeable records within groups and do not account for school-level clustering. They should not be read as national population estimates."""),
    code("""display(result['groups'])
display(Image(filename='results/studytime_grades.png'))
display(result['school_groups'])
display(Image(filename='results/school_comparison.png'))"""),
    md("""## 6. SQL cross-check
The SQL version joins a category lookup, groups records and computes means. The same numbers are checked against Pandas. The school filter uses parameters rather than formatting values into SQL text."""),
    code("""display(sql_summary(result['data']))
display(sql_summary(result['data'], school='GP'))
np.testing.assert_allclose(result['sql'].mean_grade, result['groups'].mean_grade)
print('SQL and Pandas means agree.')"""),
    md("""## 7. Relationships and sensitivity
Spearman correlation measures ranked association. It fits ordinal study-time categories without pretending the codes are equally spaced hours. It does not establish causation.

G2 is a previous-period grade. A strong relationship with G3 would not justify calling it a before-course predictor. Removing zero final grades here is an explicit sensitivity check, not a claim that zero means missing."""),
    code("""display(Image(filename='results/correlations.png'))
display(result['sensitivity'])
display(result['summary'])"""),
    md("""## 8. Interpretation
The higher study-time categories generally have higher mean grades than the lowest category in this sample, but the highest category does not have the highest mean. The >10-hour category has only 35 records.

**بالعربي:** لا نقول إن عدد ساعات معين يضمن درجة أعلى. هذه بيانات رصدية من مدرستين، وقد تختلف المجموعات في عوامل أخرى. النتائج لا تصف طلاب السعودية أو أثر مجتمع تعليمي جديد.

The full report is saved to `results/report.html`, with charts embedded so it opens offline. `results/FINDINGS.md` provides a compact, reproducible written summary.

## Extensions
- Inspect each school separately using `sql_summary`.
- Compare medians with means. Which conclusion becomes more cautious?
- Explain why deleting zero grades changes the study population.
- Design a future learning-activity evaluation that collects only necessary information.

Reference for the skills applied: [Python Institute PCAD syllabus](https://pythoninstitute.org/pcad-exam-syllabus). The project practices selected objectives; it does not claim complete syllabus coverage."""),
]
nb=nbf.v4.new_notebook(cells=cells,metadata={"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python"}})
nbf.write(nb, root/'student_learning_analysis.ipynb')
print('Built notebook.')
