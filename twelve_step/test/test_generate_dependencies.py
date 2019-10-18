import unittest
from typing import List, Tuple

from twelve_step.test.resource import TEST_PROJECT_DIRECTORY
from twelve_step.exclude_packages_factory import construct_exclude_packages
from twelve_step.generate_dependencies import generate_dependencies

A_DEPENDENCIES = ("A", ["ABC", "abstractmethod"])
B_DEPENDENCIES = ("B", ["A", "D"])
C_DEPENDENCIES = ("C", ["A"])
D_DEPENDENCIES = ("D", ["ABC", "abstractmethod"])


class GenerateDependenciesTest(unittest.TestCase):
    def test_whenGeneratingDependencies_thenDependenciesAreGenerated(self):
        excluded_pakcages = construct_exclude_packages(["typing"])
        project_path = f"{TEST_PROJECT_DIRECTORY}/test-project"

        dependencies = generate_dependencies(project_path, excluded_pakcages)

        self.assertDependenciesCorrectlyGenerated(dependencies)

    def assertDependenciesCorrectlyGenerated(
        self, dependencies: List[Tuple[str, List[str]]]
    ):
        self.assertIn(A_DEPENDENCIES, dependencies)
        self.assertIn(B_DEPENDENCIES, dependencies)
        self.assertIn(C_DEPENDENCIES, dependencies)
        self.assertIn(D_DEPENDENCIES, dependencies)
