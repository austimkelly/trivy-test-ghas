import json
import toml

def find_package_line(package_name, pyproject_content):
    parsed_toml = toml.loads(pyproject_content)
    dependencies = parsed_toml.get('tool', {}).get('poetry', {}).get('dependencies', {})
    
    if package_name not in dependencies:
        return None

    lines = pyproject_content.split('\n')
    for i, line in enumerate(lines):
        if package_name in line:
            return i + 1  # Line numbers start at 1

    return None

# Load the SARIF report
with open('../trivy-results.sarif', 'r') as f:
    sarif_report = json.load(f)

# Load the pyproject.toml file
with open('../pyproject.toml', 'r') as f:
    pyproject_content = f.read()

# Go through each result in the SARIF report
for run in sarif_report['runs']:
    for result in run['results']:
        # Extract the package name from the artifactLocation.uri field
        uri = result['locations'][0]['physicalLocation']['artifactLocation']['uri']
        package_name = uri.split('/')[-2].split('-')[0]

        # Find the line number in the pyproject.toml file
        line_number = find_package_line(package_name, pyproject_content)

        # Update the SARIF report with the line number
        if line_number is not None:
            result['locations'][0]['physicalLocation']['region']['startLine'] = line_number
            result['locations'][0]['physicalLocation']['region']['endLine'] = line_number
            result['locations'][0]['physicalLocation']['artifactLocation']['uri'] = 'pyproject.toml'

# Save the updated SARIF report
with open('updated_report.sarif', 'w') as f:
    json.dump(sarif_report, f, indent=2)