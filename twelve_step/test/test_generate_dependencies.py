import unittest
from typing import List, Tuple

from twelve_step.test.resource import TEST_PROJECT_DIRECTORY
from twelve_step.exclude_packages_factory import construct_exclude_packages
from twelve_step.generate_dependencies import (
    generate_class_dependencies,
    generate_packages_dependencies,
)

A_DEPENDENCIES = ("A", ["ABC", "abstractmethod"])
B_DEPENDENCIES = ("B", ["A", "D"])
C_DEPENDENCIES = ("C", ["A"])
D_DEPENDENCIES = ("D", ["ABC", "abstractmethod"])

TEST_PROJECT_DEPENDENCIES = ("test-project", ["package_2", "subpackage_2"])
PACKAGE_1_DEPENDENCIES = ("package_1", ["abc"])
PACKAGE_2_DEPENDENCIES = ("package_2", ["package_1"])
SUBPACKAGE_2_DEPENDENCIES = ("subpackage_2", ["package_1"])


class GenerateDependenciesTest(unittest.TestCase):
    def test_whenGeneratingClassDependencies_thenClassDependenciesAreGenerated(self):
        excluded_pakcages = construct_exclude_packages(["typing"])
        project_path = f"{TEST_PROJECT_DIRECTORY}/test-project"

        dependencies = generate_class_dependencies(project_path, excluded_pakcages)

        self.assertClassDependenciesCorrectlyGenerated(dependencies)

    def assertClassDependenciesCorrectlyGenerated(
        self, dependencies: List[Tuple[str, List[str]]]
    ):
        self.assertIn(A_DEPENDENCIES, dependencies)
        self.assertIn(B_DEPENDENCIES, dependencies)
        self.assertIn(C_DEPENDENCIES, dependencies)
        self.assertIn(D_DEPENDENCIES, dependencies)

    def test_whenGeneratingPackagesDependencies_thenPackagesDependenciesAreGenerated(
        self
    ):
        excluded_pakcages = construct_exclude_packages(["typing"])
        project_path = f"{TEST_PROJECT_DIRECTORY}/test-project"

        dependencies = generate_packages_dependencies(project_path, excluded_pakcages)

        self.assertPackagesDependenciesAreCorrectlyGenerated(dependencies)

    def assertPackagesDependenciesAreCorrectlyGenerated(
        self, dependencies: List[Tuple[str, List[str]]]
    ):
        self.assertIn(TEST_PROJECT_DEPENDENCIES, dependencies)
        self.assertIn(PACKAGE_1_DEPENDENCIES, dependencies)
        self.assertIn(PACKAGE_2_DEPENDENCIES, dependencies)
        self.assertIn(SUBPACKAGE_2_DEPENDENCIES, dependencies)
