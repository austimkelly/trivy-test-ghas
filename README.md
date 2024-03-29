# trivy-test-ghas
testing trivy with GHAS

Trivy is a comprehensive vulnerability scanner that can scan OS packages and language-specific packages. For Python, Trivy scans installed packages, not the `pyproject.toml` or `requirements.txt` files directly.

When you build a Docker image, the Python packages specified in your pyproject.toml file get installed into the Docker image. Trivy then scans these installed packages in the Docker image for known vulnerabilities.

# Running from cmd-line

Assuming you check out the repo, have Docker installed, and have the trivy image available, you can run the following command to scan the repo:

```bash
docker build -t test_tag .
```

then to test with trivy:

```bash
trivy image --format template --template "@/contrib/sarif.tpl" --output trivy-results.sarif --severity CRITICAL,HIGH test_tag
```

The results can be found in the [trivy-results.sarif](./trivy-results.sarif) file.

# Running from trivy Action

You can either create a PR to "main" or run the action manually in the [trivy action](https://github.com/austimkelly/trivy-test-ghas/actions/workflows/trivy.yml) 

# Limitations of Trivy Docker scanning with GHAS

* Trivy does not scan the `pyproject.toml` or `requirements.txt` files directly. It scans the installed packages in the Docker image.
* The file and line locations provided are in the Docker build cache (see [locations: array in the SARIF output](https://github.com/austimkelly/trivy-test-ghas/blob/develop/trivy-results.sarif#L622)]). The file and line information won't be reachable by the SARIF parser in GHAS.
* When running from a Github action, the only code alerts displayed are when you filter the code results on a PR #. This is something no developer would ever do in a normal workflow. For example, see this filter on PR #1: https://github.com/austimkelly/trivy-test-ghas/security/code-scanning?query=is%3Aopen+branch%3Amain+pr%3A1+
* Code checks in the SARIF updload will never succeed unless the referenced file in the SARIF is part of the pull request. GHAS code scanning needs a file and line number to provide an annotations to block the PR. This doesn't mean the alert won't get reported, it just won't interrupt the developer workflow and prevent a PR merge.
* You will likely get duplicate entries between Trivy and Dependabot. While dependabot can group and resolve multiple vulnerabity classes, Trivy will require alerts to be dismissed one at a time. Additoinally, code scanning right now does not creeate PRs. Additionally, it doens't look like 3rd party scanning tools will get the use of AI suggestions to fix vulnerabities like CodeQL will [reference](https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/about-autofix-for-codeql-code-scanning) 

# A line mapper test

Can we map the discovered vulnerabilities in the Trivy output from the Docker build artifacts and map them back to an original `requirements.txt` or `pyproject.toml` file? Here's a quick hack to test this out. The `line_mapper.py` script is hard-coded to the locations of the `pyproject.toml` and `trivy-reusults.sarif` files at the repo root.

1. PWD should be the root of this repository.
2. `pip install toml`
3. `python3 line_mapper.py`
4. Open up [updated_report.sarif](./updated_report.sarif) to see the output.

It can be done, but how reliably? In this one small test and a cursory check, it appears to be fairly reliable.

# Running the line mapper from a GHAS action

See [trivy-line-adjust.yml](./.github/workflows/trivy-line-adjust.yml) for an example of how to run the line mapper from a GHAS action. The action will run the line mapper and then upload the results to the PR as a check.

![line mapper action](./img/mapped-line-num.png)

