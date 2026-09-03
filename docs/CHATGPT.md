# ChatGPT Integration

AgentBroko can be connected to ChatGPT as a Custom GPT Action. The action calls the deployed REST API to generate structured Video Forge project blueprints and list available skills.

## Deploy first

Deploy this repository to Vercel or another public HTTPS host. The default contract assumes:

```text
https://agentbroko.vercel.app/openapi.json
```

If you use another domain, update the `servers.url` value in `api/index.py` before deploying.

## Configure a Custom GPT Action

1. Open the GPT builder in ChatGPT.
2. Create or edit a GPT and open **Actions**.
3. Choose **Import from URL**.
4. Enter your deployed `https://YOUR-DOMAIN/openapi.json` URL.
5. Select **No authentication** for the current public API.
6. Add instructions such as:

   > Use AgentBroko for video production planning. For a new video, call `generateVideoProject` with the user's brief. Explain that the response is a project blueprint and SRT captions, not a rendered MP4. Use `listSkills` when the user asks what AgentBroko can do. Do not claim that an external desktop editor is bundled.

## Available actions

- `generateVideoProject`: creates a structured project blueprint and subtitle file from a prompt.
- `listSkills`: returns the discoverable AgentBroko skill registry.
- `checkHealth`: checks whether the deployment is available.

The API does not upload user media or render an MP4 in the hosted action. For local rendering, use the npm/Python CLI and Video Forge skill. For existing-footage editing, use the optional Video Edit workflow and any explicitly connected external editor.

## Compatibility manifest

The deployment also exposes `/.well-known/ai-plugin.json` for older plugin discovery tooling. Current ChatGPT integrations should use Custom GPT Actions and the OpenAPI URL above.

## Security and limits

The current API is unauthenticated and should be treated as a public demo/action endpoint. Before production use, add authentication, rate limiting, request size limits, and an explicit privacy policy appropriate to your deployment.