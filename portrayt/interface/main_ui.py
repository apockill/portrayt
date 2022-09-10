from pathlib import Path
from typing import Any

import gradio as gr

from portrayt import configuration, generators


class MainApp:
    def __init__(self, configuration_path: Path, cache_root_path: Path):
        self._config_path = configuration_path
        self._cache_root_path = cache_root_path

        self._config = configuration.Configuration.parse_file(configuration_path)
        self._app = self._create_ui()

    def _create_ui(self) -> gr.Blocks:
        with gr.Blocks(title="Portrayt") as app:
            gr.Markdown("# 🖼️ Configure your Portrayt 💻")
            with gr.Tabs():
                with gr.TabItem("Image Variations"):
                    self._create_generate_variations_ui()

        return app

    def _create_generate_variations_ui(self) -> None:
        prompt_config = self._config.prompt_generate_variations

        prompt_text = gr.Textbox(label="Prompt", value=lambda: prompt_config.prompt)
        num_variations = gr.Number(
            label="Number of variations", value=lambda: prompt_config.num_variations
        )
        result = gr.Label(label="Output")
        save_button = gr.Button("Save")
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
        self.update_config()

        return "Portrait updated successfully!"

    def update_config(self) -> None:
        """Save the current data model and run any API tasks"""
        self._config_path.write_text(self._config.json(indent=4))

        generator = self._get_current_generator()
        generator.generate()

    def _get_current_generator(self) -> generators.BaseGenerator[Any]:
        """Instantiate the current generator based on configuration"""
        if self._config.current_prompt_type == configuration.PromptGenerateVariations.__name__:
            parameters = self._config.prompt_generate_variations
            generator = generators.VariationGenerator(parameters, self._cache_root_path)
        else:
            raise ValueError(f"Unknown prompt type {self._config.current_prompt_type}")
        return generator


    def launch(self) -> None:
        self._app.launch()
