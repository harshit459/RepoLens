from backend.app.code_analysis.python_analyzer import analyze_python_file

results = analyze_python_file("sample_code.py")

for item in results:
    print(item)
