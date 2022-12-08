python_sources(name="lib", sources=["**/*.py"])

python_distribution(
    name="raicontours-packaged",
    dependencies=[
        ":lib",
        ":resources",
    ],
    sdist=True,
    wheel=True,
    provides=python_artifact(
        name="raicontours",
    ),
    generate_setup=False,
)

resources(
    name="resources",
    sources=[
        "LICENSE",
        "LICENSE.ADDITIONAL-TERMS",
        "README.md",
        "pyproject.toml",
        "raicontours/py.typed",
    ],
)
