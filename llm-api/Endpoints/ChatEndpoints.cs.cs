using llm_api.Contracts;

namespace llm_api.Endpoints
{
    public static class ChatEndpoints
    {
        public static IEndpointRouteBuilder MapChatEndpoints(this IEndpointRouteBuilder app)
        {
            app.MapPost("/chat", HandleChat)
               .WithName("Chat")
               .WithOpenApi();
            return app;
        }

        private static async Task<ChatResponse> HandleChat(
            ChatRequest req,
            IHttpClientFactory httpClientFactory)
        {
            var client = httpClientFactory.CreateClient("LlmCore");

            var payload = new { prompt = req.Message };

            var response = await client.PostAsJsonAsync("generate", payload);
            response.EnsureSuccessStatusCode();

            var llmCoreResponse = await response.Content.ReadFromJsonAsync<LlmCoreResponse>();

            var reply = llmCoreResponse?.Completion ?? "[errore: risposta vuota da llm-core]";

            return new ChatResponse(reply);
        }
    }
}
