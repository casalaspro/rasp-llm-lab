namespace llm_api.Configuration
{
    public static class HttpClientConfig
    {
        public static IServiceCollection AddLlmCoreHttpClient(
        this IServiceCollection services,
        IConfiguration configuration)
        {
            var llmCoreUrl = configuration["LlmCore:BaseUrl"]
                ?? throw new Exception("Missing LlmCore:BaseUrl configuration");

            services.AddHttpClient("LlmCore", client =>
            {
                client.BaseAddress = new Uri(llmCoreUrl);
            });

            return services;
        }
    }
}
