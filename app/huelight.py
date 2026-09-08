import requests
from time import sleep
from pathlib import Path
import urllib3
import yaml

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_config(path: str) -> dict:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise
    except Exception:
        raise

class HueLight:
    def __init__(
        self, 
        api_key: str, 
        light_id: str,
        light_name: str, 
        base_url: str
    ):
        self.api_key = api_key
        self.light_id = light_id
        self.base_url = base_url
        self.light_name = light_name

        self.light_endpoint = f"{self.base_url}/{self.light_id}" 

    def __repr__(self):
        return f"<id: {self.light_id}; name: {self.light_name}>"

    def _set_on_state(self, light_on: bool) -> bool:
        response = requests.put(
            self.light_endpoint,
            json={"on":{"on":light_on}},
            headers={
                "hue-application-key": self.api_key
            }, 
            verify=False
        )
        response.raise_for_status()
        data = response.json()

        return response.ok and not data["errors"]

    def is_on(self) -> bool | None:
        response = requests.get(
            self.light_endpoint,
            headers={
                "hue-application-key": self.api_key
            }, 
            verify=False
        )
        response.raise_for_status()

        result = response.json()
        data = result.get('data', [])

        if not data:
            return None

        if result.get("errors"):
            return None

        return data[0]['on']['on']
        
    def turn_on(self):
        return self._set_on_state(True)

    def turn_off(self):
        return self._set_on_state(False)


if __name__ == "__main__":
    import yaml
    current_folder = Path(__file__).parent
    config_path = current_folder / "secrets" / "config.yml"

    config = read_config(config_path)
    api = config["general"]["api"]
    url = config["general"]["url"]
    lamp_id = config["lamps"]["hue_play_2"]

    light1 = HueLight(api, lamp_id, url)

    light1.turn_on()
    status = light1.is_on()
    print(f"Lampe ist {'eingeschaltet' if status else "ausgeschaltet"}")

    sleep(5)

    light1.turn_off()
    status = light1.is_on()
    print(f"Lampe ist {'eingeschaltet' if status else "ausgeschaltet"}")
