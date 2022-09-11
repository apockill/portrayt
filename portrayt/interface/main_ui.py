from pathlib import Path
from typing import Any

import gradio as gr

from portrayt import configuration as schemas
from portrayt import generators, renderers


class MainApp:
    def __init__(
        self,
        configuration_path: Path,
        cache_root_path: Path,
        render_type: renderers.RendererType,
        port: int,
    ):
        self._config = schemas.Configuration.parse_file(configuration_path)
        self._config_path = configuration_path
        self._cache_root_path = cache_root_path
        self._server_port = port

        self._schema_mappings = {
            schemas.PromptGenerateVariations.__name__: (
                self._config.prompt_generate_variations,
                generators.VariationGenerator,
            ),
            schemas.PromptInterpolationAnimation.__name__: (
                self._config.prompt_interpolation_animation,
                generators.InterpolationAnimationGenerator,
            ),
        }
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

            gr.Markdown("## ✨ Prompt Settings ")
            with gr.Tabs():
                with gr.TabItem("Image Variations"):
                    self._create_generate_variations_ui()
                with gr.TabItem("Prompt Interpolation"):
                    self._create_generate_interpolation_ui()

        return app

    def _create_general_settings_ui(self) -> None:
        current_prompt_type = gr.Dropdown(
            value=lambda: self._config.current_prompt_type,
            choices=[k for k in self._schema_mappings.keys()],
            label="Current Prompt Type",
        )
        seconds_between_images = gr.Number(
            lambda: self._config.renderer.seconds_between_images,
            label="Seconds between images",
        )
        clear_results_between = gr.Checkbox(
            lambda: self._config.clear_results_between_images,
            label="Clear previous images when a new prompt is added",
        )
        portrait_height = gr.Number(
            lambda: self._config.portrait_height, label="Frame Height", precision=0
        )
        portrait_width = gr.Number(
            lambda: self._config.portrait_width, label="Frame Width", precision=0
        )
        seed = gr.Number(lambda: self._config.seed, label="Seed", precision=0)

        result = gr.Label(label="")
        save_button = gr.Button("Save Settings")
        save_button.click(
            self._on_general_settings_saved,
            inputs=[
                current_prompt_type,
                seconds_between_images,
                clear_results_between,
                portrait_height,
                portrait_width,
                seed,
            ],
            outputs=result,
        )

    def _create_generate_variations_ui(self) -> None:
        prompt_config = self._config.prompt_generate_variations

        prompt_text = gr.Textbox(lambda: prompt_config.prompt, label="Prompt")
        num_variations = gr.Number(
            lambda: prompt_config.num_variations,
            label="Number of Variations",
            precision=0,
        )

        result = gr.Label(label="")
        save_button = gr.Button("Save and Render")
        save_button.click(
            self._on_generate_variations_saved,
            inputs=[prompt_text, num_variations],
            outputs=result,
        )

    def _create_generate_interpolation_ui(self) -> None:
        prompt_config = self._config.prompt_interpolation_animation

        prompt_start = gr.Textbox(lambda: prompt_config.prompt_start, label="Prompt Start")
        prompt_end = gr.Textbox(lambda: prompt_config.prompt_end, label="Prompt End")
        prompt_strength = gr.Textbox(lambda: prompt_config.prompt_strength, label="Prompt Strength")
        num_animation_frames = gr.Number(
            lambda: prompt_config.num_animation_frames,
            label="Number of Animation Frames",
            precision=0,
        )
        seamless_loop = gr.Checkbox(lambda: prompt_config.seamless_loop, label="Seamless Loop")

        result = gr.Label(label="")
        save_button = gr.Button("Save and Render")
        save_button.click(
            self._on_interpolation_settings_saved,
            inputs=[prompt_start, prompt_end, prompt_strength, num_animation_frames, seamless_loop],
            outputs=result,
        )

    def _on_generate_variations_saved(self, prompt: str, num_variations: int) -> str:
        """Run when the user saves new configuration for PromptGenerateVariations"""
        self._config.current_prompt_type = schemas.PromptGenerateVariations.__name__
        self._config.prompt_generate_variations.prompt = prompt
        self._config.prompt_generate_variations.num_variations = num_variations

        return self.update_config()

    def _on_general_settings_saved(
        self,
        current_prompt_type: str,
        seconds_between_images: int,
        clear_results_between: bool,
        portrait_height: int,
        portrait_width: int,
        seed: int,
    ) -> str:
        self._config.current_prompt_type = current_prompt_type
        self._config.renderer.seconds_between_images = seconds_between_images
        self._config.clear_results_between_images = clear_results_between
        self._config.portrait_width = portrait_width
        self._config.portrait_height = portrait_height
        self._config.seed = seed

        return self.update_config(render=False)

    def _on_interpolation_settings_saved(
        self,
        prompt_start: str,
        prompt_end: str,
        prompt_strength: float,
        num_animation_frames: int,
        seamless_loop: bool,
    ) -> str:
        self._config.current_prompt_type = schemas.PromptInterpolationAnimation.__name__
        self._config.prompt_interpolation_animation.prompt_start = prompt_start
        self._config.prompt_interpolation_animation.prompt_end = prompt_end
        self._config.prompt_interpolation_animation.prompt_strength = prompt_strength
        self._config.prompt_interpolation_animation.num_animation_frames = num_animation_frames
        self._config.prompt_interpolation_animation.seamless_loop = seamless_loop
        return self.update_config()

    def update_config(self, render: bool = True) -> str:
        """Save the current data model and run any API tasks
        :param render: If true, the generator will re-render images
        :return: The success/fail message
        """
        self._config_path.write_text(self._config.json(indent=4))

        generator = self._get_current_generator()

        if render:
            try:
                generator.generate(clear_previous=self._config.clear_results_between_images)
            except Exception as e:
                return f"Failed to generate images:\n {e}"

        # Update the renderer so it knows about the new generator
        self._renderer.update_generator(generator)

        return "Settings saved successfully!"

    def _get_current_generator(self) -> generators.BaseGenerator[Any]:
        """Instantiate the current generator based on configuration"""
        parameters, generator = self._schema_mappings[self._config.current_prompt_type]

        return generator(  # type: ignore
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
        gr.close_all()
