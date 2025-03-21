import typer

from kueuer.benchmarks.kubectl import benchmark, launcher, plot

app = typer.Typer()
app.add_typer(benchmark.app, name="benchmark")
app.add_typer(launcher.app, name="launch")
app.add_typer(plot.app, name="plot")

if __name__ == "__main__":
    app()
