# PDF Playbook

`pdf-playbook` creates premium, actionable developer handbooks with a dark technology visual system, callout tables, code blocks, fixed AgentBroko branding, and a legal responsibility notice.

## Interactive generation

```bash
agentbroko pdf-playbook --output guide.pdf \
  --extra-question "What product URL should appear?" \
  --extra-question "What must the reader accomplish?"
```

The generator asks for a title, audience, core promise, and each optional question. Generated PDFs may be sold or reused by their creator.

## Automated generation

```bash
pdf-playbook --non-interactive \
  --title "AgentRouter + Cline AI Credits Developer Playbook" \
  --audience "Developers new to AgentRouter and Cline" \
  --topic "Claim AI credits, connect Cline, and improve your coding workflow" \
  --output agentrouter-cline-guide.pdf
```

## Free-edition branding

The free edition always displays `AgentBroko by Broke Innovation`, the AgentBroko project URL, and this notice:

> AgentBroko is a platform for generating documents. Users are solely responsible for the content they create, publish, sell, or otherwise use.

`--remove-branding` is reserved for a future premium edition and currently exits with an error.

## Content responsibility

Users must verify time-sensitive claims, prices, promotions, availability, laws, and third-party terms before publication. AgentBroko does not validate or endorse generated content.
