from stack import Stack
from copy import deepcopy
import click


class Wizard:
    def __init__(self, steps):
        if not steps:
            raise ValueError("Wizard needs at least one step")
        self.steps = steps
        self.current_index = 0
        self.history = Stack()
        self.form_data = {}

    def current_step(self):
        return self.steps[self.current_index]

    def set_step_data(self, **data):
        """Update data for the current step in memory."""
        step = self.current_step()
        if step not in self.form_data:
            self.form_data[step] = {}
        self.form_data[step].update(data)

    def get_step_data(self, step_name=None):
        """Get data for a step (or current step if not provided)."""
        step = step_name or self.current_step()
        return deepcopy(self.form_data.get(step, {}))

    def next(self):
        if self.current_index >= len(self.steps) - 1:
            click.secho("You are already at the last step.", fg="yellow")
            return
        self.history.push(self.current_index)
        self.current_index += 1

    def back(self):
        if self.history.isempty():
            click.secho("No previous step in history.", fg="yellow")
            return
        self.current_index = self.history.pop()

    def status(self):
        click.echo("-" * 44)
        click.secho("Current wizard status", bold=True, fg="cyan")
        click.echo(f"Step: {self.current_step()} (index {self.current_index})")
        click.echo(f"Step data: {self.get_step_data()}")
        click.echo("-" * 44)


@click.command()
def run_wizard():
    step_fields = ["name", "last name", "city", "address", "phone"]
    wizard = Wizard(step_fields)

    click.echo("=" * 50)
    click.secho("REGISTRATION WIZARD", bold=True, fg="cyan")
    click.echo("=" * 50)
    click.secho("Type 'back' to return to the previous step.\n", fg="bright_black")

    while True:
        field = wizard.current_step()
        current_value = wizard.get_step_data().get(field)

        step_number = wizard.current_index + 1
        total_steps = len(wizard.steps)

        click.echo("-" * 50)
        click.secho(f"Step {step_number}/{total_steps}", fg="blue", bold=True)
        click.echo(f"Field: {field}")

        prompt_text = "Value"
        if current_value:
            prompt_text += f" [{current_value}]"

        value = click.prompt(prompt_text, default=current_value or "", show_default=False).strip()

        if value.lower() == "back":
            wizard.back()
            continue

        if not value:
            click.secho("This field is required.", fg="red")
            continue

        wizard.set_step_data(**{field: value})

        if wizard.current_index == len(wizard.steps) - 1:
            break
        wizard.next()

    click.echo("\n" + "=" * 50)
    click.secho("SUMMARY", bold=True, fg="green")
    click.echo("=" * 50)

    label_width = max(len(step) for step in wizard.steps)
    for step in wizard.steps:
        step_data = wizard.get_step_data(step)
        click.echo(f"{step.ljust(label_width)} : {step_data.get(step, '')}")

    click.echo("=" * 50)


if __name__ == "__main__":
    run_wizard()