from argparse import ArgumentParser
from pathlib import Path

from portrayt.configuration import Configuration, PromptGenerateVariations
from portrayt.interface import MainApp


def main() -> None:
    parser = ArgumentParser(description="Run the main portrayt server and display")
    parser.add_argument(
        "-d",
        "--data-directory",
        type=Path,
        default=".portrayt-state",
        help="Where to store portrayt configuration and cached images",
    )
    args = parser.parse_args()

    # Create necessary files and directories for usage
    data_dir: Path = args.data_directory
    data_dir.mkdir(parents=True, exist_ok=True)
    config_path = data_dir / "portrayt-config.json"
    if not config_path.is_file():
        config = Configuration(
            current_prompt_type=PromptGenerateVariations.__name__,
            prompt_generate_variations=PromptGenerateVariations(
                prompt="Robots rights protest, vintage associated press photo",
                num_variations=10,
            ),
            portrait_width=640,
            portrait_height=400,
        )
        config_path.write_text(config.json())

    app = MainApp(configuration_path=config_path, cache_root_path=data_dir)
    app.launch()


if __name__ == "__main__":
    main()
