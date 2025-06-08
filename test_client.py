import logging
import httpx
from typing import Any
from uuid import uuid4

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest


base_url = 'http://localhost:9999'

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)  # Get a logger instance
    
    async with httpx.AsyncClient() as httpx_client:
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
            # agent_card_path uses default, extended_agent_card_path also uses default
        )
        
        _public_card = await resolver.get_agent_card()
        logger.info(
            _public_card.model_dump_json(indent=2, exclude_none=True)
        )
        final_agent_card_to_use = _public_card
        logger.info(
            '\nUsing PUBLIC agent card for client initialization (default).'
        )
        
        # initialize A2AClient with the public agent card
        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=final_agent_card_to_use,
        )
        logger.info('A2AClient initialized successfully.')
        
        # Example usage of the client
        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': 'Hello World!'}
                ],
                'messageId': uuid4().hex,
            }
        }
        
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**send_message_payload)
        )
        
        response = await client.send_message(request)
        print(response.model_dump(mode='json', exclude_none=True))
        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())