python_sources(name="lib", sources=["**/*.py"])

python_distribution(
    name="plugins-packaged",
    dependencies=[
        ":lib",
        ":resources",
    ],
    sdist=True,
    wheel=True,
    provides=python_artifact(
        name="opensamdpantsplugins",
    ),
    generate_setup=False,
)

resources(
    name="resources",
    sources=[
        "LICENSE",
        "README.md",
        "pyproject.toml",
    ],
)
