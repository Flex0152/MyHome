from huelight import HueLight, read_config
from nicegui import ui
from pathlib import Path


current_path = Path(__file__).parent
config = read_config(current_path / "secrets" / "config.yml")


lights = [
    HueLight(
        api_key=config["general"]["api"],
        light_id=light["id"],
        light_name=light["name"],
        base_url=config["general"]["url"]
    )
    for light in config["lights"]
]


ui.label("Hue Control")

for light in lights:
    with ui.card():
        ui.label(light.light_name)
        status = ui.label()

        def update_status(light=light, status=status):
            is_on = light.is_on()

            if is_on is None:
                status.set_text("Unbekannt")
            elif is_on:
                status.set_text("An")
            else:
                status.set_text("Aus")

        def turn_on(light=light, update_status=update_status):
            light.turn_on()
            update_status()

        def turn_off(light=light, update_status=update_status):
            light.turn_off()
            update_status()

        update_status()

        ui.timer(5, update_status)

        with ui.row():
            ui.button("Ein", on_click=turn_on)
            ui.button("Aus", on_click=turn_off)

ui.run(host="0.0.0.0", port=8081)