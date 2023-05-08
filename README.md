# Duplicated Classes Finder

A Python script to find Java classes present in multiple .jar and .war files within a directory, along with their locations. The script generates an HTML report with a modern interface that allows users to filter the results and switch between two views: grouping by class or by file.

## Features

- Search for .jar and .war files in a given directory
- Recursively search for nested .jar files inside .jar and .war files
- Filter out files and directories based on regex patterns
- Generate an HTML report with a modern interface using Bootstrap
- Filter the results in the HTML report
- Group duplications by class or by file in the HTML report
- Display generation time, script execution parameters, and execution time in the report

## Usage

1. Clone the repository:

```bash
git clone https://github.com/rfm4j/DuplicatedClassesFinder.git
```

2. Navigate to the cloned repository:

```bash
cd DuplicatedClassesFinder
```

3. Run the script:

```bash
python duplicatedCasspathFinder.py --dir=/path/to/sample_repository --exclude=".hidden" --exclude="another_pattern"
```

Replace `/path/to/sample_repository` with the path to the directory containing .jar and .war files you want to analyze. You can exclude directories or files using the `--exclude` option, which can be provided multiple times with different regex patterns.

4. Open the generated HTML report (`report.html` by default) in a web browser to view the results.
