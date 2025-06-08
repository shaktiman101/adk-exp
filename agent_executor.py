from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

class HelloWorldAgent:
    """Hello world agent"""
    
    async def invoke(self) -> str:
        return "Hello World!"
    
class HelloWorldAgentExecutor(AgentExecutor):
    """Executor for the HelloWorldAgent"""
    
    def __init__(self) -> None:
        super().__init__()
        self.agent = HelloWorldAgent()
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        result = await self.agent.invoke()
        event_queue.enqueue_event(new_agent_text_message(result))
        
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("Cancel not supported for HelloWorldAgentExecutor")
