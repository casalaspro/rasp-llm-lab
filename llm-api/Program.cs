using llm_api.Configuration;
using llm_api.Endpoints;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddLlmCoreHttpClient(builder.Configuration);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddLlmCoreHttpClient(builder.Configuration);

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.MapGet("/", () => "Hello from llm-api in Docker!");

app.MapChatEndpoints();

app.Run();
