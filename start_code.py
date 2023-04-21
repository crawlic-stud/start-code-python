from pathlib import Path
import os


proj_name = input("Input project name: ")
proj_path = Path.cwd() / proj_name
print(f"Creating project in {proj_path}")
proj_path.mkdir(exist_ok=True)


src_path = proj_path / "src"
src_path.mkdir(exist_ok=True)

(src_path / "main.py").write_text('''

if __name__ == "__main__":
    ...
''')

(proj_path / "requirements.txt").touch()
(proj_path / ".gitignore").write_text('''venv
.env
__pycache__
''')
(proj_path / ".env").touch()
(proj_path / ".env.example").touch()

(proj_path / "Dockerfile").write_text("""FROM python:3.10.8

ADD src/main.py .

COPY requirements.txt /tmp/requirements.txt
COPY . .

RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "src/main.py"]""")

(proj_path / "docker-compose.yml").write_text("""version: "3"
services:
  prod:
    build:
      context: .
      dockerfile: ./Dockerfile
    container_name: container-name
""")

(proj_path / "README.md").write_text(f"# {proj_name}")


print("Done.")
yes_or_no = input("Open in VS Code? [y/n]")
if yes_or_no.lower() == "y":
    os.system(f"code {proj_path}")
