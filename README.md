# Student Learning Analytics📊🖥️

**A practical application of the data-analysis skills developed through PCAD certification 📃 .**

This project examines study-time categories, recorded absences and final grades through a complete exploratory workflow: data validation, descriptive statistics, SQL queries, visualization and evidence-based interpretation.

## The question

**What patterns appear in student learning data, and how much can we reasonably conclude from them?**

The analysis uses 649 Portuguese-course records from the UCI Student Performance dataset. It compares reported study-time groups, separates two schools, and checks whether selected correlations change when zero final grades are excluded in a sensitivity analysis.

![Study-time categories and final grades](results/studytime_grades.png)

## Selected findings

| Measure | Result |
|---|---:|
| Records analyzed | 649 |
| Mean final grade | 11.91 / 20 |
| Median final grade | 12 / 20 |
| Study-time category vs final grade, Spearman ρ | 0.275 |
| Absences vs final grade, Spearman ρ | −0.159 |

The highest study-time category is not the group with the highest mean grade. Its sample size is only 35. This makes group size, uncertainty and context essential to the interpretation.

## What the project includes

- **Data quality audit:** required columns, missingness, full-row duplicates, category validity and numeric ranges.
- **Transparent preparation:** normalized labels and numeric types; preserved valid zero grades and matching selected profiles.
- **Exploratory analysis:** distributions, grouped means and medians, rank correlations and separate-school summaries.
- **Uncertainty and sensitivity:** row-bootstrap intervals and a clearly labeled analysis excluding zero final grades.
- **SQL analysis:** SQLite aggregation with a lookup-table join and a parameterized school filter, checked against Pandas.


## View the results

![School comparison](results/school_comparison.png)



## Analytical decisions

The source has no missing values in the inspected file, so no imputation is performed. All records are retained. Matching selected profiles do not establish duplicate students because the file lacks a unique student identifier. Study-time codes are treated as ordered categories, not exact hours. Zero final grades remain in the main analysis.

Bootstrap intervals resample records within each displayed group, using 2,000 draws and a fixed seed. They assume exchangeability within groups, do not account for school clustering, and should not be interpreted as representative population intervals. No causal effect or significance claim is made.

Previous-period grades are included for descriptive comparison. A strong G2–G3 correlation does not make G2 available before the course begins. No prediction model or intervention is evaluated here.

## Data attribution

 **Student Performance** [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5TG7T](https://doi.org/10.24432/C5TG7T).

Dataset license: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

