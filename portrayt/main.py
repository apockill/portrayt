from argparse import ArgumentParser
from pathlib import Path

from portrayt.configuration import Configuration, PromptGenerateVariations, RendererParams
from portrayt.interface import MainApp
from portrayt.renderers import RendererType


def main() -> None:
    parser = ArgumentParser(description="Run the main portrayt server and display")
    parser.add_argument(
        "-d",
        "--data-directory",
        type=Path,
        default=".portrayt-state",
        help="Where to store portrayt configuration and cached images",
    )
    parser.add_argument(
        "-r",
        "--renderer",
        required=True,
        type=RendererType,
        help=f"What type of renderer to use. Valid values are: {[v.value for v in RendererType]}",
    )
    parser.add_argument("-p", "--port", type=int, default=80)
    args = parser.parse_args()

    # Create necessary files and directories for usage
    data_dir: Path = args.data_directory.absolute()
    data_dir.mkdir(parents=True, exist_ok=True)
    config_path = data_dir / "portrayt-config.json"
    if not config_path.is_file():
        config = Configuration(
            current_prompt_type=PromptGenerateVariations.__name__,
            prompt_generate_variations=PromptGenerateVariations(
                prompt="Robots rights protest, colorized vintage newspaper scan",
                num_variations=10,
            ),
            renderer=RendererParams(seconds_between_images=30),
            portrait_width=768,
            portrait_height=512,
            seed=1337,
        )
        config_path.write_text(config.json())

    app = MainApp(
        configuration_path=config_path,
        cache_root_path=data_dir,
        render_type=args.renderer,
        port=args.port,
    )
    app.launch()

    app.close()


if __name__ == "__main__":
    main()
