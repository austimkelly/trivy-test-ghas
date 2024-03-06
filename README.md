# trivy-test-ghas
testing trivy with GHAS

Trivy is a comprehensive vulnerability scanner that can scan OS packages and language-specific packages. For Python, Trivy scans installed packages, not the pyproject.toml or requirements.txt files directly.

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