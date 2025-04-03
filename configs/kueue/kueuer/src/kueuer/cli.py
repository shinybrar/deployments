import typer

from kueuer.benchmarks import benchmark, k8s, plot

app = typer.Typer()
app.add_typer(benchmark.benchmark_cli, name="benchmark")
app.add_typer(k8s.app, name="jobs")
app.add_typer(plot.app, name="plot")

if __name__ == "__main__":
    app()
