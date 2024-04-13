import os
import pmd
import csv
from git import Repo

def cloner_repo(url, chemin_destination):
  Repo.clone_from(url, chemin_destination)

def analyser_projet(chemin_projet, nom_projet):
  # Configurez les règles PMD
  regles = pmd.PMDConfiguration()
  regles.rule_sets = "rulesets/java/quickstart.xml"

  # Analysez le projet
  rapport = pmd.Report.run(chemin_projet, config=regles)

  # Extrayez les informations sur les code smells
  smells = []
  for violation in rapport.violations:
    smells.append({
      "fichier": violation.filename,
      "ligne": violation.beginline,
      "type": violation.rule.name,
      "gravite": violation.priority.name,
      "description": violation.message
    })

  # Créez le dossier du projet dans le dataset
  os.makedirs(f"dataset/{nom_projet}", exist_ok=True)

  # Enregistrez les données dans un fichier CSV
  with open(f"dataset/{nom_projet}/smells.csv", "w", newline="") as fichier_csv:
    writer = csv.DictWriter(fichier_csv, fieldnames=smells[0].keys())
    writer.writeheader()
    writer.writerows(smells)

def main():
  # Liste des URLs des repositories
  urls_repos = [
    "https://github.com/user/repo1.git",
    "https://github.com/user/repo2.git",
    # ...
  ]

  # Chemin de base pour cloner les repositories
  chemin_base = "dataset"

  # Cloner les repositories et analyser les projets
  for i, url_repo in enumerate(urls_repos):
    nom_projet = f"projet_{i+1}"
    chemin_projet = f"{chemin_base}/{nom_projet}"
    cloner_repo(url_repo, chemin_projet)
    analyser_projet(chemin_projet, nom_projet)

if __name__ == "__main__":
  main()