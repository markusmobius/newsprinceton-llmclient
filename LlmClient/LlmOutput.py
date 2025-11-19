from dataclasses import dataclass

@dataclass
class RunMetaData:
    RunTime : str
    RunTimeSeconds : float
    PromptTokens : int
    CompletionTokens : int
    TotalTokens : int
    def __init__(self, RunTime : str, RunTimeSeconds : float, PromptTokens : int, CompletionTokens : int, TotalTokens : int):
        self.RunTime = RunTime
        self.RunTimeSeconds = RunTimeSeconds
        self.PromptTokens = PromptTokens
        self.CompletionTokens = CompletionTokens
        self.TotalTokens = TotalTokens

@dataclass
class CachedEntry:
    UserName: str
    OriginalTags: list[str]
    ChatAnswer: str
    Embedding: list[float]
    RuntimeData : RunMetaData
    def __init__(self, UserName: str, OriginalTags: list[str], ChatAnswer: str, Embedding: list[float], RuntimeData : RunMetaData):
        self.UserName = UserName
        self.OriginalTags = OriginalTags
        self.ChatAnswer = ChatAnswer
        self.Embedding = Embedding
        self.RuntimeData = RuntimeData

@dataclass
class LlmOutput:
    answer : CachedEntry
    answerReference : str
    error : str
    isCached : bool
    def __init__(self, answer : CachedEntry, answerReference : str, error : str, isCached : bool):
        self.answer = answer
        self.answerReference = answerReference
        self.error = error
        self.isCached = isCached

@dataclass
class LlmSimpleOutput:
    answer : CachedEntry
    error : str    
    def __init__(self, answer : CachedEntry, error : str):
        self.answer = answer
        self.error = error

