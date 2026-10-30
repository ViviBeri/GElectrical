"""Regression tests for generator slack-bus options."""

from gelectrical.elementmodel.generator import Generator


def test_generator_slack_options_default_to_non_slack():
    generator = Generator()

    assert generator.fields["slack"]["value"] is False
    assert generator.fields["slack_weight"]["value"] == 1.0

    model = generator.get_power_model("generator-1")
    params = model[0][2]

    assert params["slack"] is False
    assert params["slack_weight"] == 1.0


def test_generator_slack_options_are_passed_to_power_model():
    generator = Generator()
    generator.fields["slack"]["value"] = True
    generator.fields["slack_weight"]["value"] = 2.5

    model = generator.get_power_model("generator-1")
    params = model[0][2]

    assert params["slack"] is True
    assert params["slack_weight"] == 2.5
