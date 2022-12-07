python_sources(
    name="lib",
    dependencies=[":resources"],
    overrides={
        "version.py": {"dependencies": ["src/python/rai/_version:resources"]},
    },
)

python_distribution(
    name="rai-packaged",
    dependencies=[
        ":lib",
        ":resources",
    ],
    sdist=True,
    wheel=True,
    provides=setup_py(
        name="rai",
        description="",
    ),
)

resources(name="resources", sources=["py.typed"])
