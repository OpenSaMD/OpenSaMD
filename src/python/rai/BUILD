python_sources(
    dependencies=[":resources"],
    overrides={
        "__main__.py": {"dependencies": ["src/python/pants/bin:pants_loader"]},
        "version.py": {"dependencies": ["src/python/pants/_version:resources"]},
    },
)

python_distribution(
    name="rai-packaged",
    dependencies=[":lib"],
    wheel=True,
    sdist=True,
    provides=setup_py(
        name="rai",
        description="",
    ),
)