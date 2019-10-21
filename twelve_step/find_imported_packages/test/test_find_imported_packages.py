from twelve_step.find_imported_packages.find_imported_packages import (
    find_imported_packages_in_imports,
)
import unittest

DIRECTORY = "directory"
A_FILE_NAME = f"a/path/{DIRECTORY}"

PACKAGE_1 = "package_1"
PACKAGE_2 = "package_2"
IMPORT_1 = f"from {PACKAGE_1}.class import class"
IMPORT_2 = f"from {PACKAGE_1}.{PACKAGE_2}.class_2 import class_2"


class FindImportedPackagesTest(unittest.TestCase):
    def test_whenFindingImportedPackages_thenAllPackagesAreFound(self):
        packages = find_imported_packages_in_imports(A_FILE_NAME, [IMPORT_1, IMPORT_2])[
            1
        ]

        self.assertIn(PACKAGE_1, packages)
        self.assertIn(PACKAGE_2, packages)

    def test_givenImportDirectlyFromPackage_whenFindingImportedPackages_thenPackageIsPackage(
        self
    ):
        import_line = f"from {DIRECTORY} import class"

        packages = find_imported_packages_in_imports(A_FILE_NAME, [import_line])[1]

        self.assertIn(DIRECTORY, packages)

    def test_whenFindingImportedPackages_thenFileIsKeptInMapping(self):
        file = find_imported_packages_in_imports(A_FILE_NAME, [IMPORT_1, IMPORT_2])[0]

        self.assertEqual(A_FILE_NAME, file)
