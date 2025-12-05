namespace llm_api.Contracts
{
    public record ChatRequest(string Message);
    public record ChatResponse(string Reply);
    public record LlmCoreResponse(string Completion);
}
