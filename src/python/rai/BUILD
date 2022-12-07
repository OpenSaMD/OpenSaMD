python_sources(name="lib", sources=["**/*.py"])
python_sources(name="types", sources=["**/*.pyi"])

python_distribution(
    name="rai-packaged",
    dependencies=[
        ":lib",
        ":resources",
    ],
    sdist=True,
    wheel=True,
    provides=python_artifact(
        name="rai",
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
        "rai/py.typed",
    ],
)
