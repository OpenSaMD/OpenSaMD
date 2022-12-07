python_distribution(
    name="rai-packaged",
    dependencies=[
        "src/python/rai/rai:lib",
        "src/python/rai/rai:resources",
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
    sources=["LICENSE", "LICENSE.ADDITIONAL-TERMS", "README.md", "pyproject.toml"],
)
