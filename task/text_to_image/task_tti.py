import asyncio
from datetime import datetime

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"

async def _save_images(attachments: list[Attachment]):
    # TODO:
    async with DialBucketClient(
        api_key=API_KEY,
        base_url=DIAL_URL,
    ) as bucketClient:
        for attachment in attachments:
            image_data = await bucketClient.get_file(attachment.url)
            file_name = f"{datetime.now()}.png"

            with open(file_name, 'wb') as image_file:
                image_file.write(image_data)
            
            print(f"Image saved: {file_name}")
    

def start() -> None:
    # TODO:
    dialClient = DialModelClient (
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT, 
        deployment_name='dall-e-3',
        api_key=API_KEY)
    user_input = 'Sunny day on Bali'

    ai_message = dialClient.get_completion(
        messages=[Message(role=Role.USER, content=user_input)],
        custom_fields={
            "size": Size.square,
            "style": Style.vivid,
            "quality": Quality.hd,
        }
    )

    if custom_content := ai_message.custom_content:
        if attachments := custom_content.attachments:
            asyncio.run(_save_images(attachments))


start()
