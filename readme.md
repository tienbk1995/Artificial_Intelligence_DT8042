# How to Run – AI Lab 2

## 1. Prerequisites

Install the following software:

- Python 3.10 or newer
- Git (if cloning the repository)

## 2. Download the project

Clone the repository:

```bash
git clone <repository-url>
```

Or download and extract the project ZIP file.

Open the project root folder (`All_Lab`) in VS Code or a terminal.

## 3. Create a virtual environment

Open a terminal in the project root and execute:

**Windows (PowerShell):**

```powershell
python -m venv .venv
```

## 4. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents script execution, use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 5. Install dependencies

With the virtual environment activated:

```bash
python -m pip install -r requirements.txt
```

The required packages are listed in `requirements.txt`.

## 6. Run Task 1

From the project root (`All_Lab`), execute:

```powershell
python -m Lab_2.Task_1.Task_1_b.Test_Task_1b
```

To run Task 1a:

```powershell
python -m Lab_2.Task_1.Task_1_a.Test_Task_1
```

## 7. Expected output

The program will:

- Generate a random map containing the H-shaped obstacle.
- Execute the implemented search algorithms.
- Compare path lengths, total costs, and expanded nodes.
- Calculate average performance metrics across the experiments.
- Display performance graphs.
- Export the results to an Excel file, if Excel export is enabled.

## Notes

- Do not submit the local `.venv` directory.
- Keep `requirements.txt` in the project root.
- Run the commands from the `All_Lab` project root directory.
