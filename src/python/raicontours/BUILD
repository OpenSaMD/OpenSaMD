python_distribution(
    name="raicontours-packaged",
    dependencies=[
        "src/python/raicontours/raicontours:lib",
        "src/python/raicontours/raicontours:resources",
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
    sources=["LICENSE", "LICENSE.ADDITIONAL-TERMS", "README.md", "pyproject.toml"],
)
