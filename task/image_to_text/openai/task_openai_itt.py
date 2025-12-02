import base64
from pathlib import Path

from task._utils.constants import API_KEY, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl


def start() -> None:
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    deployment_name = "gpt-4-vision-preview" 
    dialModelClient = DialModelClient(endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT, deployment_name=deployment_name, api_key=API_KEY)
    dialModelClient.get_completion(
        messages=[
            ContentedMessage(
                role=Role.USER,
                content=[
                    TxtContent(
                        text="Analyze this image:", 
                    ),
                    ImgContent(
                        image_url=ImgUrl(
                            url=f"data:image/png;base64,{base64_image}"
                        )
                    )
                ]
            )
        ]
    )


start()