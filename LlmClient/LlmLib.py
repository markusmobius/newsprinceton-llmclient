import asyncio
import grpc
import uuid
from .message_pb2 import SimpleMessage # Your protobuf messages
from .message_pb2_grpc import MessagesStub  # Your gRPC service stub
from ChunkWriter import ChunkWriter  # Utility for writing chunks
import os
from Models import Chat, Embedding
import json
import time

class GrpcConnection:
    """
    Owns ONE shared gRPC channel.
    You can create many client sessions (streams) on this channel.
    """

    def __init__(self):
        self.channel = grpc.aio.secure_channel(
            os.environ["LLM_SERVER_URL"],
            grpc.ssl_channel_credentials()
        )
        self.stub = MessagesStub(self.channel)

    async def close(self):
        await self.channel.close()


class BidirectionalClient:
    """
    A single streaming message client that:
        - connects automatically when created
        - manages its own streams
        - has its own heartbeat
    """

    def __init__(self, engineType: str, connection : GrpcConnection):
        # no await here!
        self.engineType = engineType
        self.conn = connection
        self.stub = connection.stub

        self.guid = uuid.uuid4().hex

        self.is_connected = False

        self.call = None
        self.heartbeat_call = None

        self._msg_future = None
        self._heartbeat_future = None

        self._heartbeat_task = None

    # ----------------------------------------
    # FACTORY METHOD (async init)
    # ----------------------------------------
    @classmethod
    async def create(cls, engineType: str, connection : GrpcConnection):
        """
        Async factory method that constructs AND connects a session.
        """
        self = cls(engineType, connection)
        await self._connect()
        return self

    # ----------------------------------------
    # STREAM READERS
    # ----------------------------------------
    async def _read_call_stream(self):
        async for msg in self.call:
            if self._msg_future and not self._msg_future.done():
                self._msg_future.set_result(msg)

    async def _read_heartbeat_stream(self):
        async for msg in self.heartbeat_call:
            if self._heartbeat_future and not self._heartbeat_future.done():
                self._heartbeat_future.set_result(msg)

    # ----------------------------------------
    # MAIN CONNECT LOGIC
    # ----------------------------------------
    async def _connect(self):
        if self.is_connected:
            return

        # open two independent streaming RPCs
        self.call = self.stub.BidirectionalMessage()
        self.heartbeat_call = self.stub.BidirectionalMessage()

        # start background readers
        asyncio.create_task(self._read_call_stream())
        asyncio.create_task(self._read_heartbeat_stream())

        # handshake
        hello = SimpleMessage(mtype=self.engineType, payload=self.guid.encode())
        res = await self.send_receive(hello)

        self.from_scratch = (res.mtype == "fresh")
        print("session:", "first-time" if self.from_scratch else "reused")

        # start heartbeat
        await self.heartbeat_call.write(
            SimpleMessage(mtype="__heartbeat__", payload=self.guid.encode())
        )
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        self.is_connected = True

        writer=ChunkWriter()
        writer.write_str(os.environ["LLM_USER_CODE"])
        await self.send_receive(SimpleMessage(mtype="__initengine__", payload=writer.close()))


    # ----------------------------------------
    # HEARTBEAT LOOP
    # ----------------------------------------
    async def _heartbeat_loop(self):
        while True:
            await self.heartbeat_call.write(
                SimpleMessage(mtype="__heartbeat__", payload=self.guid.encode())
            )
            await asyncio.sleep(10)

    # ----------------------------------------
    # SEND/RECEIVE HELPERS
    # ----------------------------------------
    async def send_receive(self, message):
        loop = asyncio.get_running_loop()
        self._msg_future = loop.create_future()

        await self.call.write(message)
        return await self._msg_future


    async def close(self):
        if self._heartbeat_task:
            self._heartbeat_task.cancel()

        if self.call:
            await self.call.done_writing()

        if self.heartbeat_call:
            await self.heartbeat_call.done_writing()

class LlmClient:

    def __init__(self, connection : GrpcConnection):
        self.connection = connection

    async def connect(self):
        self.client = await BidirectionalClient.create("llm",self.connection)
    
    async def SendSurely(self, message):
        while True:
            try:
                response = await self.client.send_receive(message)
                return response.payload.decode()
            except Exception as e:
                print(f"Error during Ask: {e}. Retrying...")
                time.sleep(5)


    async def Ask(self, chat : Chat, tags : list[str], cache_only : bool = False, retries: int = -1):
        writer=ChunkWriter()
        writer.write_str(chat.getJSON())
        writer.write_str(json.dumps(tags))
        if cache_only:
            writer.write_int(1)
        else:
            writer.write_int(0)
        writer.write_int(retries)
        return await self.SendSurely(SimpleMessage(mtype="ask", payload=writer.close()))

    async def AskMany(self, chats : list[Chat], tags : list[str], retries: int = -1):
        writer=ChunkWriter()
        writer.write_str(json.dumps(chats, default=lambda obj: obj.getJSON(), indent=4))
        writer.write_str(json.dumps(tags))
        writer.write_int(retries)        
        return await self.SendSurely(SimpleMessage(mtype="askmany", payload=writer.close()))

    async def Embed(self, input : Embedding, tags : list[str], cache_only : bool = False, retries: int = -1):
        writer=ChunkWriter()
        writer.write_str(input.getJSON())
        writer.write_str(json.dumps(tags))
        if cache_only:
            writer.write_int(1)
        else:
            writer.write_int(0)
        writer.write_int(retries)
        return await self.SendSurely(SimpleMessage(mtype="embed", payload=writer.close()))

    async def AskMany(self, inputs : list[Embedding], tags : list[str], retries: int = -1):
        writer=ChunkWriter()
        writer.write_str(json.dumps(inputs, default=lambda obj: obj.getJSON(), indent=4))
        writer.write_str(json.dumps(tags))
        writer.write_int(retries)        
        return await self.SendSurely(SimpleMessage(mtype="embedmany", payload=writer.close()))


class LlmFactory:
    def __init__(self):
        self.connection = GrpcConnection()

    async def create_client(self):
        client = LlmClient(self.connection)
        await client.connect()
        return client
