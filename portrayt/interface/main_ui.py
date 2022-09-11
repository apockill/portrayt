from pathlib import Path
from typing import Any

import gradio as gr

from portrayt import configuration, generators, renderers


class MainApp:
    def __init__(
        self,
        configuration_path: Path,
        cache_root_path: Path,
        render_type: renderers.RendererType,
        port: int,
    ):
        self._config = configuration.Configuration.parse_file(configuration_path)
        self._config_path = configuration_path
        self._cache_root_path = cache_root_path
        self._server_port = port

        # Create a renderer with the current configuration
        self._renderer = renderers.RENDERER_TYPES[render_type](
            self._get_current_generator(), params=self._config.renderer
        )

        # Create the settings server UX
        self._app = self._create_ui()

    def _create_ui(self) -> gr.Blocks:
        with gr.Blocks(title="Portrayt") as app:
            gr.Markdown("# 🖼️ Configure your Portrayt")
            gr.Markdown("## 💻 Currently Displayed")
            gr.Image(value=lambda: self._renderer.current_image)

            gr.Markdown("## ⚙️ Settings")
            with gr.Box():
                self._create_general_settings_ui()

            gr.Markdown("## ✨ Current Prompt Settings ")
            with gr.Tabs():
                with gr.TabItem("Image Variations"):
                    self._create_generate_variations_ui()

        return app

    def _create_general_settings_ui(self) -> None:
        portrait_height = gr.Number(
            lambda: self._config.portrait_height, label="Frame Height", precision=0
        )
        portrait_width = gr.Number(
            lambda: self._config.portrait_width, label="Frame Width", precision=0
        )
        seed = gr.Number(lambda: self._config.seed, label="Seed", precision=0)
        seconds_between_images = gr.Number(
            lambda: self._config.renderer.seconds_between_images,
            label="Seconds between images",
        )

        result = gr.Label(label="")
        save_button = gr.Button("Save Settings")
        save_button.click(
            self._on_general_settings_saved,
            inputs=[portrait_height, portrait_width, seed, seconds_between_images],
            outputs=result,
        )

    def _create_generate_variations_ui(self) -> None:
        prompt_config = self._config.prompt_generate_variations

        prompt_text = gr.Textbox(lambda: prompt_config.prompt, label="Prompt")
        num_variations = gr.Number(
            lambda: prompt_config.num_variations,
            label="Number of variations",
            precision=0,
        )

        result = gr.Label(label="")
        save_button = gr.Button("Save and Render")
        save_button.click(
            self._on_generate_variations_saved,
            inputs=[prompt_text, num_variations],
            outputs=result,
        )

    def _on_generate_variations_saved(self, prompt: str, num_variations: int) -> str:
        """Run when the user saves new configuration for PromptGenerateVariations"""
        self._config.current_prompt_type = configuration.PromptGenerateVariations.__name__
        self._config.prompt_generate_variations.prompt = prompt
        self._config.prompt_generate_variations.num_variations = num_variations

        return self.update_config()

    def _on_general_settings_saved(
        self,
        portrait_height: int,
        portrait_width: int,
        seed: int,
        seconds_between_images: int,
    ) -> str:
        self._config.portrait_width = portrait_width
        self._config.portrait_height = portrait_height
        self._config.seed = seed
        self._config.renderer.seconds_between_images = seconds_between_images

        return self.update_config(render=False)

    def update_config(self, render: bool = True) -> str:
        """Save the current data model and run any API tasks
        :param render: If true, the generator will re-render images
        :return: The success/fail message
        """
        self._config_path.write_text(self._config.json(indent=4))

        generator = self._get_current_generator()

        if render:
            try:
                generator.generate()
            except Exception as e:
                return f"Failed to generate images:\n {e}"

        # Update the renderer so it knows about the new generator
        self._renderer.update_generator(generator)

        return "Settings saved successfully!"

    def _get_current_generator(self) -> generators.BaseGenerator[Any]:
        """Instantiate the current generator based on configuration"""
        if self._config.current_prompt_type == configuration.PromptGenerateVariations.__name__:
            parameters = self._config.prompt_generate_variations
            generator = generators.VariationGenerator
        else:
            raise ValueError(f"Unknown prompt type {self._config.current_prompt_type}")
        return generator(
            params=parameters,
            cache_dir=self._cache_root_path,
            height=self._config.portrait_height,
            width=self._config.portrait_width,
            seed=self._config.seed,
        )

    def launch(self) -> None:
        self._app.launch(server_port=self._server_port, server_name="0.0.0.0")

    def close(self) -> None:
        self._app.close()
