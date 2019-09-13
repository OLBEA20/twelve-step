with open("version.txt", "r+") as version_file:
    version = version_file.readline().replace("\n", "")
with open("version.txt", "w+") as version_file:
    version_parts = version.split(".")
    patch = version_parts[-1]
    version_parts[-1] = str(int(patch) + 1)
    version_file.write(".".join(version_parts))
