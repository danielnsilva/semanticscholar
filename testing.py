from semanticscholar import SemanticScholar

api_key = "M7YnOUDkmO66RVRQIXJOv7HRI70WSlAN7kfD3Y8M"
sch = SemanticScholar(api_key=api_key)

releases = sch.get_available_releases()
print(releases)
latest_release = sch.get_release(releases[0])

for dataset in latest_release.datasets:
    print(dataset.name)
    print(dataset.description)
    print(dataset.README)
    print("--------------------------------")