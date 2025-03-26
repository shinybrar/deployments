import typer

from kueuer.benchmarks import benchmark, launch, plot

app = typer.Typer()
app.add_typer(benchmark.app, name="benchmark")
app.add_typer(launch.app, name="launch")
app.add_typer(plot.app, name="plot")

if __name__ == "__main__":
    app()
