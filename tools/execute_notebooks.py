"""Execute every notebook cell in IPython and save real captured outputs.

Uses an in-process IPython shell: no local kernel sockets are required.
The shared snapshot contains the computed tables and embedded figures.
"""
from pathlib import Path
import os
import subprocess
import sys
import nbformat
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from IPython.utils.capture import capture_output

root = Path(__file__).resolve().parents[1]


def execute_one(name):
    os.chdir(root)
    os.environ["QUANTUM_LABS_STATIC_RUN"] = "1"
    shell = TerminalInteractiveShell.instance()
    shell.run_line_magic("matplotlib", "inline")
    notebook = nbformat.read(root / name, as_version=4)
    count = 0
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        count += 1
        with capture_output(stdout=True, stderr=True, display=True) as captured:
            result = shell.run_cell(cell.source, store_history=False)
        if result.error_before_exec or result.error_in_exec:
            raise RuntimeError(f"{name}, code cell {count} failed:\n{captured.stdout}\n{captured.stderr}")
        outputs = []
        if captured.stdout:
            outputs.append(nbformat.v4.new_output("stream", name="stdout", text=captured.stdout))
        if captured.stderr:
            outputs.append(nbformat.v4.new_output("stream", name="stderr", text=captured.stderr))
        for rich in captured.outputs:
            outputs.append(nbformat.v4.new_output("display_data", data=rich.data, metadata=rich.metadata))
        cell.outputs = outputs
        cell.execution_count = count
    notebook.metadata["execution_method"] = "Sequential in-process IPython execution"
    notebook.metadata["language_info"] = {"name": "python", "version": sys.version.split()[0]}
    nbformat.validate(notebook)
    nbformat.write(notebook, root / name)
    print(f"Executed {count} code cells: {name}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute_one(sys.argv[1])
    else:
        for name in ["student_learning_analysis.ipynb"]:
            subprocess.run([sys.executable, __file__, name], check=True)
